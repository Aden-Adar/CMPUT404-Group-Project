// https://bobbyhadz.com/blog/react-onclick-redirect
// https://i.stack.imgur.com/l60Hf.png

import './App.css';
import React, {useState} from 'react';
import {Routes, Route, useNavigate} from 'react-router-dom';
import LoginForm from "./components/LoginForm"
import SignUpForm from "./components/SignUpForm";
import { Main } from './MainPage/Main';
import Profile from './components/Profile';
import CreatePost from './components/CreatePost';
import Followers from './components/Followers';

function App() {
  
  const current_author = JSON.parse(window.localStorage.getItem("Author"));
  const AUTHOR_ID = current_author.id;

  const [user, setUser] = useState({
    name: current_author.displayName,
    bio: 'I am a social media app',
    image: current_author.profileImage,
  });


  const handleSaveProfile = ({name, bio, image}) => {
    let profileData = { 
    "type": "author",
    "id": AUTHOR_ID,
    "url": AUTHOR_ID,
    "host": window.location.hostname,
    "displayName": name,
    "github": "",
    "profileImage": image
    };
    fetch(AUTHOR_ID, {method: 'PUT', headers: {'Content-Type': 'application/json'},
    body:JSON.stringify(profileData)
    })
    setUser({...user, name, bio, image});
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
        <Route path="/followers" element={<Followers />} />
    </Routes>
    </div>
  );
}
export default App;
