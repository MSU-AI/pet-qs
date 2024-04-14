export async function uploadVideoToServer(videoFile) {
  try {
    const formData = new FormData();
    formData.append('image', videoFile);

    const response = await fetch('https://pets.onet.cool/postImage', {
      method: 'POST',
      body: formData,
      mode: 'no-cors',
    });

    if (!response.ok) {
      console.log('Error code:', response.status);
      const errorText = await response.text();
      console.error('Server response:', errorText);
      throw new Error(`Network response was not ok: ${errorText}`);
    }

    const videoBlob = await response.blob();
    const videoBlobUrl = URL.createObjectURL(videoBlob);
    return videoBlobUrl;
  } catch (error) {
    console.error('Error uploading video:', error);
    throw error;
  }
}
