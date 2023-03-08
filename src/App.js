// https://bobbyhadz.com/blog/react-onclick-redirect
// 'https://via.placeholder.com/200x200?text=Profile+Image'

import './App.css';
import React, {useState, useEffect} from 'react';
import {Routes, Route, useNavigate} from 'react-router-dom';
import LoginForm from "./components/LoginForm"
import SignUpForm from "./components/SignUpForm";
import { Main } from './MainPage/Main';
import Profile from './components/Profile';
import CreatePost from './components/CreatePost'
function App() {

  const navigate = useNavigate();

  const navigateToSignIn = () => {
    navigate('/');
  };

  const navigateToSignUp = () => {
    navigate('/signup');
  };

  const [user, setUser] = useState({
    name: localStorage.getItem('name'), 
    bio: localStorage.getItem('bio'),
    image: localStorage.getItem('image') || 'https://i.stack.imgur.com/l60Hf.png',
  });

  useEffect(() => {
    const storedName = localStorage.getItem('name');
    const storedBio = localStorage.getItem('bio');
    const storedImage = localStorage.getItem('image');

    if (storedName || storedBio || storedImage) {
      setUser({
        name: storedName || '',
        bio: storedBio || '',
        image: storedImage || '',
      });
    }
  }, []);

  const handleSaveProfile = ({name, bio, image}) => {
    localStorage.setItem('name', name);
    localStorage.setItem('bio', bio);
    localStorage.setItem('image', image);

    setUser({
      name,
      bio,
      image,
    });
  };

  const handleLogin = (user) => {
    setUser(user);
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div className="App">
      <Routes>
          <Route path="/" element={<LoginForm />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/signup" element={<SignUpForm />} />
          <Route path="/main" element={<Main />} />
          <Route path="/profile" element={<Profile user={user} onSave={handleSaveProfile} />} />
          <Route path="/create" element={<CreatePost />} />
        </Routes>
    
    </div>
  );
}

export default App;
