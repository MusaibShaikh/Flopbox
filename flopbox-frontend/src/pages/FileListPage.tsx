import React, { useEffect, useState } from 'react';
import { Container, Typography, List, ListItem, Button } from '@mui/material';
import { fetchFiles, deleteFile } from '../api';
import { useAuth } from '../context/AuthContext';
import FileUpload from '../components/FileUpload';
import { Link } from 'react-router-dom';

interface File {
  Id: string;
  Filename: string;
  FileType: string;
  Comment?: string;
}

const FileListPage: React.FC = () => {
  const [files, setFiles] = useState<File[]>([]);  
  const { user } = useAuth(); 

  useEffect(() => {
    const getFiles = async () => {
      try {
        const response = await fetchFiles(user!); 
        setFiles(response.data);
      } catch (error) {
        console.error('Error fetching files:', error);
      }
    };
    if (user) getFiles();
  }, [user]);

  const handleDelete = async (fileId: string) => {
    try {
      await deleteFile(fileId);
      setFiles(files.filter((file) => file.Id !== fileId));
    } catch (error) {
      console.error('Error deleting file:', error);
    }
  };

  return (
    <Container>
      <Typography variant="h4">Your Files</Typography>
      <FileUpload onUploadSuccess={() => {
        const getFiles = async () => {
          const response = await fetchFiles(user!);
          setFiles(response.data);
        };
        getFiles();
      }} />
      <List>
        {files.map((file) => (
          <ListItem key={file.Id}>
            <Typography>{file.Filename}</Typography>
            <Button component={Link} to={`/files/${file.Id}`} color="primary">View</Button>
            <Button onClick={() => handleDelete(file.Id)} color="secondary">Delete</Button>
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default FileListPage;
