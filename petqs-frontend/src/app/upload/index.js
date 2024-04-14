export async function uploadVideoToServer(videoFile) {
 try {
  const formData = new FormData();
  formData.append('image', videoFile);
  const response = await fetch('https://pets.onet.cool/postImage', {
    method: 'POST',
    body: formData,
    mode: 'no-cors',
  });

  return response;
} catch (error) {
  console.error('Error uploading video:', error);
} 
}
