export async function uploadVideoToServer(videoFile) {
  try {
    const formData = new FormData();
    formData.append('image', videoFile);

    const response = await fetch('https://pets.onet.cool/postImage', {
      method: 'POST',
      body: formData
    });

    const videoBlob = await response.blob();
    const videoBlobUrl = URL.createObjectURL(videoBlob);
    console.log('Video uploaded:', videoBlobUrl);
    return videoBlobUrl;
  } catch (error) {
    console.error('Error uploading video:', error);
    throw error;
  }
}
