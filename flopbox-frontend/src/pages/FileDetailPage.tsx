import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Typography, Button } from '@mui/material';
import { downloadFile } from '../api';
import axios from 'axios';

interface FileDetail {
  Id: string;
  Filename: string;
  FileType: string;
  Comment?: string;
  UploadDate: string;
}

const FileDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [file, setFile] = useState<FileDetail | null>(null);

  useEffect(() => {
    const fetchFileDetails = async () => {
      try {
        const response = await axios.get(`/file/${id}`);
        setFile(response.data);
      } catch (error) {
        console.error('Error fetching file details:', error);
      }
    };
    fetchFileDetails();
  }, [id]);

  const handleDownload = async () => {
    try {
      const response = await downloadFile(id!);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', file?.Filename || 'file');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  if (!file) {
    return <Typography>Loading file details...</Typography>;
  }

  return (
    <Container>
      <Typography variant="h4">File Details</Typography>
      <Typography variant="h6">Filename: {file.Filename}</Typography>
      <Typography variant="body1">File Type: {file.FileType}</Typography>
      {file.Comment && <Typography variant="body1">Comment: {file.Comment}</Typography>}
      <Typography variant="body2">Uploaded on: {new Date(file.UploadDate).toLocaleDateString()}</Typography>
      <Button variant="contained" color="primary" onClick={handleDownload}>
        Download File
      </Button>
    </Container>
  );
};

export default FileDetailPage;
