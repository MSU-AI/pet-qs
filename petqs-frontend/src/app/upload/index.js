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
    console.log('error code: ', response);
    const errorText = await response.text();
    console.error('Server response:', errorText);
    console.error(`Network response was not ok: ${errorText}`);
  }

  const data = await response.json();
  console.log('Server response:', data);
} catch (error) {
  console.error('Error uploading video:', error);
} 
}
