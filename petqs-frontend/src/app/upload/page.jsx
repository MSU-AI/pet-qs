"use client"
import { useRouter } from 'next/navigation';
import { useState } from 'react';

const Upload = () => {
  const router = useRouter();
  const [videoFile, setVideoFile] = useState(null);
  const [videoURL, setVideoURL] = useState(null);
  const [confirmed, setConfirmed] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setVideoFile(file);
    const url = URL.createObjectURL(file);
    setVideoURL(url);
  };

  const handleConfirm = () => {
    setConfirmed(true);
  };

  return (
    <div className="bg-[#181818] h-screen">
      <div className="relative flex flex-col items-center justify-center h-full">
        <div className="max-w-lg w-full relative">
          <h1 className="text-3xl font-bold mb-4 text-center text-white">Upload</h1>
          <div className="mb-4 relative" style={{ width: "100%", height: "360px", backgroundColor: videoURL ? "#181818" : "#E5E7EB", position: "relative" }}>
            {!videoURL && (
              <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center">
                <p className="text-gray-300">No video selected</p>
              </div>
            )}
            {videoURL && (
              <>
                <video controls className="mx-auto" style={{ width: "100%" }}>
                  <source src={videoURL} type={videoFile.type} />
                  Your browser does not support the video tag.
                </video>
                {!confirmed && (
                  <button onClick={handleConfirm} className="absolute bottom-0 left-0 right-0 mx-auto mb-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Confirm Video
                  </button>
                )}
              </>
            )}
          </div>
          <input type="file" onChange={handleFileUpload} className={`mb-4 ${videoURL ? 'hidden' : ''} rounded`} />
        </div>
      </div>
    </div>
  );
};

export default Upload;