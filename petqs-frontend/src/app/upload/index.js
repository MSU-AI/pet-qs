export async function uploadVideoToServer(videoFile) {
 try {
  const formData = new FormData();
  formData.append('image', videoFile);
  const response = await fetch('https://pets.onet.cool/postImage', {
    method: 'POST',
    body: formData,
    mode: 'no-cors',
  });

  console.log('form data:', response.formData());
  console.log('response', response);
  console.log('response.body', response.body);
  return response.body;
} catch (error) {
  console.error('Error uploading video:', error);
} 
}
