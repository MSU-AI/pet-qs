export async function uploadVideoToServer(videoFile) {
 try {
  const formData = new FormData();
  formData.append('image', videoFile);
  const response = await fetch('https://pets.onet.cool/postImage', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
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
