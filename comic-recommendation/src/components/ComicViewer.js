import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ComicViewer = () => {
  const [comic, setComic] = useState(null);
  const userId = 101;  // Hardcoded user ID for now

  useEffect(() => {
    fetchComic();
  }, []);

  const fetchComic = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/get_comic`, {
        params: { user_id: userId }
      });
      console.log("Comic fetched:", response.data);
      setComic(response.data);
    } catch (error) {
      console.error('Error fetching comic:', error);
    }
  };

  const submitFeedback = async (reward) => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/submit_feedback`, {
        user_id: userId,
        comic_id: comic.id,  // Adjust based on your comic data structure
        reward
      });
      console.log("Feedback submitted:", response.data);
      fetchComic();
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  if (!comic) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{comic.title}</h1>
      <img src={comic.image_url} alt={comic.title} />
      <p>{comic.description}</p>
      <button onClick={() => submitFeedback(1)}>Like</button>
      <button onClick={() => submitFeedback(0)}>Dislike</button>
    </div>
  );
};

export default ComicViewer;
