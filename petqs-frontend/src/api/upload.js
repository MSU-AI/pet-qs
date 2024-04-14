import nextConnect from 'next-connect';

const handler = nextConnect();

handler.use(async (req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  await next();
});

handler.post(async (req, res) => {
  try {
    const formData = new FormData();
    formData.append('image', req.files.image[0]);

    const response = await fetch('https://pets.onet.cool/postImage', {
      method: 'POST',
      body: formData,
      mode: 'no-cors', // Set the mode to 'no-cors'
    });

    // Since the mode is 'no-cors', the response will be an opaque response,
    // which means you won't be able to access the response body or status.
    // You can still check the response status, but you won't be able to
    // parse the response body.
    console.log('Response status:', response.status);

    res.status(200).json({ message: 'Video uploaded successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default handler;
