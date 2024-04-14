"use client"
import { useRouter } from 'next/navigation';
import { useState } from 'react';

import { uploadVideoToServer } from './index';

const Upload = () => {
  const router = useRouter();
  const [videoFile, setVideoFile] = useState(null);
  const [videoURL, setVideoURL] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [imageURL, setImageURL] = useState(null);
  const [confirmed, setConfirmed] = useState(false);
  const [emotion, setEmotion] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file.type.startsWith('video')) {
      setVideoFile(file);
      const url = URL.createObjectURL(file);
      setVideoURL(url);
    } else if (file.type.startsWith('image')) {
      setImageFile(file);
      const url = URL.createObjectURL(file);
      setImageURL(url);
    }
  };

  const handleConfirm = async () => {
  setConfirmed(true);
  if (videoFile) {
    setEmotion(await uploadVideoToServer(videoFile));
  }
}; 

  return (
    <div className="bg-[#181818] h-screen">
      <div className="relative flex flex-col items-center justify-center h-full">
        <div className="max-w-lg w-full relative">
          {!confirmed && (
            <h1 className="text-3xl font-bold mb-4 text-center text-white">Upload</h1>
          )}
          <div className="mb-4 relative" style={{ width: "100%", height: "360px", backgroundColor: (videoURL || imageURL) ? "#181818" : "#E5E7EB", position: "relative" }}>
            {(!videoURL && !imageURL) && (
              <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center">
                <p className="text-gray-300">No file selected</p>
              </div>
            )}
            {(videoURL || imageURL) && (
              <>
                {videoURL && (
                  <div className="mx-auto">
                    <video controls className="mx-auto" style={{ width: "100%" }}>
                      <source src={videoURL} type={videoFile.type} />
                      Your browser does not support the video tag.
                    </video>
                    {!confirmed && (
                      <button onClick={handleConfirm} className="absolute bottom-0 left-0 right-0 mx-auto mb-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Confirm
                      </button>
                    )}
                  </div>
                )}
                {imageURL && (
                  <div className="mx-auto">
                    <img src={imageURL} alt="Uploaded image" style={{ maxWidth: "100%", maxHeight: "100%" }} />
                    {!confirmed && (
                      <button onClick={handleConfirm} className="absolute bottom-0 left-0 right-0 mx-auto mb-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Confirm
                      </button>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        <div className="flex flex-col flex gap-8 justify-center items-center">
          {confirmed && (
            <div className="flex items-center justify-center">
              <h1 className="text-white font-bold">Confirmed! Wait a bit for a response.</h1>
            </div>
          )}
          {!confirmed && (
            <input type="file" onChange={handleFileUpload} className={`mb-4 ${videoURL || imageURL ? 'hidden' : ''} rounded text-white`} />
          )}
          {emotion && (
            <div className="flex items-center justify-center">
              <h1 className="text-6xl text-white font-bold">{emotion}</h1>
            </div>
          )}
      </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;
