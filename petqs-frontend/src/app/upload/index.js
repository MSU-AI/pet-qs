export async function uploadVideoToServer(videoFile) {
 try {
   const formData = new FormData();
   formData.append('image', videoFile);

   const response = await fetch('https://pets.onet.cool/postImage', {
     method: 'POST',
     body: formData
   });

   // Check the response headers for the 'Emotion' value
   const emotion = response.body
   console.log(`Emotion: ${emotion}`);
   console.log(`Response status: ${response.status}`);
   console.log(`Response body: ${response.body}`);
   console.log(`Response body text: ${response.body.text()}`);

   if (!response.ok) {
     throw new Error(`HTTP error ${response.status}`);
   }

   return emotion;
 } catch (error) {
   console.error('Error uploading video:', error);
   throw error;
 }
}
