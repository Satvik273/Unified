const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.static('public'));
app.use('/uploads', express.static('uploads')); // Serve uploaded files

// Store files locally in 'uploads/' directory
app.post('/upload', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).send({ message: 'No file uploaded.' });

  // Optionally rename the file to include a timestamp
  const destDir = path.join(__dirname, 'uploads');
  const destFileName = `${Date.now()}_${req.file.originalname}`;
  const destPath = path.join(destDir, destFileName);

  fs.rename(req.file.path, destPath, (err) => {
    if (err) {
      console.error('File save error:', err);
      return res.status(500).send({ message: 'File save failed.' });
    }
    res.send({ message: 'File uploaded and saved locally!', path: `uploads/${destFileName}` });
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));