import React, { useState } from 'react';
import axios from 'axios';
import { Container, Typography, TextField, Button, Box, CircularProgress } from '@mui/material';

function App() {
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [aiRequest, setAiRequest] = useState('');
  const [generatedText, setGeneratedText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('/', {
        title: title,
        summary: summary,
        ai_request: aiRequest,
      });
      setGeneratedText(response.data.generated_text);
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" align="center" gutterBottom>
        小説煽り文生成
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <TextField
          label="タイトル"
          fullWidth
          margin="normal"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <TextField
          label="あらすじ"
          fullWidth
          multiline
          rows={4}
          margin="normal"
          value={summary}
          onChange={(e) => setSummary(e.target.value)}
          required
        />
        <TextField
          label="AIへの要望"
          fullWidth
          multiline
          rows={4}
          margin="normal"
          value={aiRequest}
          onChange={(e) => setAiRequest(e.target.value)}
          required
        />
        <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
          生成
        </Button>
      </Box>
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <CircularProgress />
        </Box>
      )}
      {generatedText && (
        <Box sx={{ mt: 3, p: 2, backgroundColor: '#f1f1f1', borderRadius: '4px' }}>
          <Typography variant="h6" gutterBottom>
            生成された煽り文:
          </Typography>
          <Typography dangerouslySetInnerHTML={{ __html: generatedText }}></Typography>
        </Box>
      )}
    </Container>
  );
}

export default App;
