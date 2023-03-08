// https://bobbyhadz.com/blog/react-onclick-redirect
// https://i.stack.imgur.com/l60Hf.png

import './App.css';
import React, {useState, useEffect} from 'react';
import {Routes, Route, useNavigate} from 'react-router-dom';
import LoginForm from "./components/LoginForm"
import SignUpForm from "./components/SignUpForm";
import { Main } from './MainPage/Main';
import Profile from './components/Profile';
import CreatePost from './components/CreatePost';
import { setUserId, getUserId } from './components/userID';


function App() {

  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const data = {"username": username,"password": password};
  fetch('/service/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      window.location.href = '/main';
      console.log(data);
      const userid = getUserId();
      console.log(userid);
    });

  const userid = getUserId();
  console.log(userid)

  const navigate = useNavigate();

  const navigateToSignIn = () => {
    navigate('/');
  };

  const navigateToSignUp = () => {
    navigate('/signup');
  };

  const [user, setUser] = useState({
    name: 'Social.ly',
    bio: 'I am a social media app',
    image: 'https://i.stack.imgur.com/l60Hf.png',
  });


  const handleSaveProfile = ({name, bio, image}) => {
    setUser({...user, name, bio, image});
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
