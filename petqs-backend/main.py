#Module imports
from flask import Flask,json,jsonify,request,send_file, Response
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from datetime import datetime
import shutil
import uuid  
import os

#ML imports
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import deeplabcut
import joblib

#Folder to upload files
currentDir = os.getcwd()
uploadPath = os.path.join(currentDir, 'Images')
filePath = currentDir
classifierModel = os.path.join(currentDir,'models','mlp_model_3.pkl')

#Instace of flask app
app = Flask(__name__)
CORS(app)

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
        analyzevideo=False,
        createlabeledvideo=False,
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
                      ['back_right_thai','back_right_paw']],
            'skeleton_color': 'white',
            'pcutoff': 0.4,
            'dotsize': 8,
            'alphavalue': 0.5}
    deeplabcut.auxiliaryfunctions.edit_config(config_path, edits)

    #Analyze the video, export the skeleton data
    deeplabcut.analyze_videos(config_path, videoPath)
    deeplabcut.analyzeskeleton(config_path, videoPath, videotype=videoType, save_as_csv=True)
    deeplabcut.create_labeled_video(config_path,videoPath, videotype=videoType, draw_skeleton = True)

#Analyze the pose data
def analyzePose(folder):
    #Search for CSV file in subfolder
    content = os.listdir(os.path.join(uploadPath,folder))
    dataFile =''
    for files in content:
        fileType = files.split(".")[1]
        if(fileType=='csv'):
            dataFile = files
    
    #Treat data
    data = pd.read_csv(os.path.join(uploadPath,folder,dataFile))
    data = data.to_numpy()
    data = data[2:,:]
    X = data[:,1:]

    #Initialize label encoder
    label_encoder = LabelEncoder()
    label_encoder.fit(['happy','sad','angry'])

    #Load the model
    clf_loaded = joblib.load(classifierModel)

    #Pass input to model, obtain output
    y_pred = clf_loaded.predict(X)
    y_pred_text = label_encoder.inverse_transform(y_pred)

    #Iterate over all results and see which is the top choide
    array = y_pred_text #Results
    happyCounter = 0
    sadCounter = 0
    angryCounter = 0

    for elements in array:
        if(elements=='happy'):
            happyCounter+=1

        if(elements=='sad'):
            sadCounter+=1

        if(elements=='angry'):
            angryCounter+=1

    topGuess = 'bar'
    test1 = max(happyCounter,sadCounter)
    test2 = max(angryCounter,test1)


    if(happyCounter==test2):
        topGuess = 'happy'

    elif (sadCounter==test2):
        topGuess = 'sad'

    elif (angryCounter==test2):
        topGuess = 'angry'
    
    return topGuess

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
    
    #Initialization
    folder = str(uuid.uuid4())
    vidName = secure_filename(rec.filename)
    vidType = vidName.split(".")[1].strip()

    #Check file type
    accepted = ['avi','webm','flv','vob','ogg','ogv','gif','mov','qt',
                'wmv','yuv','mp4','m4p','m4v','mpg','mpeg','m2v']
    if vidType not in accepted:
        data = {"Error": "File type is not video"}
        return jsonify(data), {"Content-Type": "application/json"}
    
    #Save the image
    os.mkdir(os.path.join(uploadPath,folder))
    rec.save(os.path.join(uploadPath,folder,vidName))

    #Function calls to the model
    poseCSV = obtainPose(vidName,folder) 
    poseNN = analyzePose(folder)
    
    #Search for mp4 file in subfolder
    content = os.listdir(os.path.join(uploadPath,folder))
    vidFile =''
    for files in content:
        try:
            fileType = files.split(".")[1]
            fileName = files.split(".")[0]
            
            #DLC always returns an mp4 file
            if((fileType=='mp4') and ('DLC' in fileName)): 
                vidFile = files
        except:
            continue
  
    #Delete the subfolder when done
    redundantFolder = folder+'-pet-qs-'+datetime.today().strftime('%Y-%m-%d')
    shutil.rmtree(os.path.join(filePath,redundantFolder))
    
    #Prepare response
    respName = vidName.split(".")[0].strip()+'_labelled.mp4'
    destPath = os.path.join(uploadPath,folder,vidFile)
    #response = send_file(destPath,download_name=respName,as_attachment=False)
    
    response = Response(response=str(poseNN))
    response.headers['emotion'] = poseNN

    print(response.headers)

    return response
