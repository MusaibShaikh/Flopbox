import React, { useState } from 'react';
import { TextField, Button, Container, Typography } from '@mui/material';
import { uploadFile } from '../api';
import { useAuth } from '../context/AuthContext';

interface FileUploadProps {
  onUploadSuccess: () => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [comment, setComment] = useState('');
  const { user } = useAuth();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (file && user) {
      try {
        await uploadFile(file, user, comment);
        onUploadSuccess(); // Trigger the callback after a successful upload
      } catch (error) {
        console.error('Upload failed:', error);
      }
    }
  };

  return (
    <Container>
      <Typography variant="h6">Upload New File</Typography>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <TextField label="Comment" fullWidth value={comment} onChange={(e) => setComment(e.target.value)} />
        <Button type="submit" variant="contained" color="primary">Upload</Button>
      </form>
    </Container>
  );
};

export default FileUpload;
