#Module imports
from flask import Flask,json,jsonify,request
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image
import deeplabcut
import shutil
import uuid  
import os

#Folder to upload files
uploadPath = r'/home/emmanuelze/Documents/Projects/pet_qs/pet_qs_backend_local/Images'
filePath = r'/home/emmanuelze/Documents/Projects/pet_qs/pet_qs_backend_local'

#Instace of flask app
app = Flask(__name__)

#Request logging function
def logger(req):
    #Data from the requests
    date = str(datetime.now())
    requester = str(request.remote_addr)
    method = str(req.method)
    path = str(req.path)

    #Log the request
    logFile = open("./requests.log" ,"a")
    logData = date+' '+requester+' '+method+' '+path+'\n'
    logFile.write(logData)
    logFile.close()

#Error logging function
def errorLog(err):
    #Data from error
    code = str(err.code)
    name = err.name
    date = str(datetime.now())

    #Log the error
    logFile = open("./requests.log" ,"a")
    logData = date+' '+'ERR'+' '+code+' '+name+'\n'
    logFile.write(logData)
    logFile.close()

#Create CSV file using DLC
def obtainPose(videoName,folder):
    #Superanimal model to be used
    supermodel_name = "superanimal_quadruped"
    pcutoff = 0.3
    videoType = videoName.split(".")[1]
    videoPath = os.path.join(uploadPath,folder,videoName)

    #Initialize project
    project_name = folder
    name = "pet-qs"

    config_path, train_config_path = deeplabcut.create_pretrained_project(
        project_name,
        name,
        [videoPath],
        videotype=videoType,
        model=supermodel_name,
        analyzevideo=True,
        createlabeledvideo=True,
        copy_videos=True, #must leave copy_videos=True
    )

    #Edit the project config.yaml file
    edits = {'skeleton': [['neck_base','tail_base'],['tail_base','tail_end'],
                      ['nose','neck_base'],['front_right_paw','back_right_paw'],
                      ['front_left_paw','back_left_paw'],['nose','left_earbase'],
                      ['left_earend','left_earbase'],['right_earend','right_earbase'],
                      ['nose','right_earbase'],['nose','left_earbase'],
                      ['lower_jaw','left_earbase'],['nose','right_earbase'],
                      ['lower_jaw','right_earbase'],['neck_base','front_left_thai'],
                      ['front_left_thai','front_left_paw'],['neck_base','front_right_thai'],
                      ['front_right_thai','front_right_paw'],['tail_base','back_left_thai'],
                      ['back_left_thai','back_left_paw'],['tail_base','back_right_thai'],
                      ['back_right_thai','back_right_paw']]}
    deeplabcut.auxiliaryfunctions.edit_config(config_path, edits)

    #Analyze the video, export the skeleton data
    deeplabcut.analyze_videos(config_path, videoPath)
    deeplabcut.analyzeskeleton(config_path, videoPath, videotype=videoType, save_as_csv=True)


#Return all HTTP errors as JSON
@app.errorhandler(HTTPException)
def handle_exception(e):
    errorLog(e)
    res = e.get_response()
    res.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    res.content_type = "application/json"
    return res

#Main route
@app.route("/", methods=['POST'])
def mainRoute():
    logger(request)

    #Prepare response
    data = {
        "data": "Pet-qs backend: main route"
    }
    return jsonify(data), {"Content-Type": "application/json"}

#Images route
@app.route("/postImage", methods=["POST"])
def postRoute():
    logger(request)

    #Extract image
    rec = request.files['image']

    #Check if empty
    if rec.filename  == '':
        data = {"Error": "No file uploaded"}
        return jsonify(data), {"Content-Type": "application/json"}
    
    #Check file type
    
    #Save the image
    folder = str(uuid.uuid4())
    vidName = secure_filename(rec.filename)
    os.mkdir(os.path.join(uploadPath,folder))
    rec.save(os.path.join(uploadPath,folder,vidName))

    #Function calls to the model
    poseCSV = obtainPose(vidName,folder)
    #Pass pose data to NN, obtain mood result


    #Delete the subfolder when done
    redundantFolder = folder+'-pet-qs-'+datetime.today().strftime('%Y-%m-%d')
    shutil.rmtree(os.path.join(filePath,redundantFolder))
    
    #Prepare response
    data = {
        "message": "received"
    }
    return jsonify(data), {"Content-Type": "application/json"}
