// https://bobbyhadz.com/blog/react-onclick-redirect

import logo from './logo.svg';
import './App.css';
import SignInForm from "./components/SignInForm";
import SignUpForm from "./components/SignUpForm";
import {Routes, Route, useNavigate} from 'react-router-dom';
import { Main } from './MainPage/Main'

function App() {

  const navigate = useNavigate();

  const navigateToSignIn = () => {
    navigate('/');
  };

  const navigateToSignUp = () => {
    navigate('/signup');
  };

  return (
    <div className="App">
      <Routes>
          <Route path="/" element={<SignInForm />} />
          <Route path="/signup" element={<SignUpForm />} />
        </Routes>
      < Main />
    </div>
  );
}

export default App;
