// https://bobbyhadz.com/blog/react-onclick-redirect
// 'https://via.placeholder.com/200x200?text=Profile+Image'

import './App.css';
import React, {useState, useEffect} from 'react';
import {Routes, Route, useNavigate} from 'react-router-dom';
import SignInForm from "./components/SignInForm";
import SignUpForm from "./components/SignUpForm";
import { Main } from './MainPage/Main';
import Profile from './components/Profile';

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

  return (
    <div className="App">
      <Routes>
          <Route path="/" element={<SignInForm />} />
          <Route path="/createaccount" element={<SignUpForm />} />
          <Route path="/main" element={<Main />} />
          <Route path="/profile" element={<Profile user={user} onSave={handleSaveProfile} />} />
        </Routes>
    
    </div>
  );
}

export default App;
