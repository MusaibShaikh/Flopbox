import React, { useState } from 'react';
import { TextField, Button, Typography, Container } from '@mui/material';
import { loginUser } from '../api';

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await loginUser(username, password);
      console.log(response.data);
      // Redirect to file list page or store token
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4">Sign In</Typography>
      <form onSubmit={handleSubmit}>
        <TextField label="Username" fullWidth value={username} onChange={(e) => setUsername(e.target.value)} />
        <TextField label="Password" type="password" fullWidth value={password} onChange={(e) => setPassword(e.target.value)} />
        <Button type="submit" variant="contained" color="primary" fullWidth>Sign In</Button>
      </form>
    </Container>
  );
};

export default LoginForm;
