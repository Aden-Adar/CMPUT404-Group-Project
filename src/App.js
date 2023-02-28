// https://bobbyhadz.com/blog/react-onclick-redirect

import logo from './logo.svg';
import './App.css';
import SignInForm from "./components/SignInForm";
import SignUpForm from "./components/SignUpForm";
import {Routes, Route, useNavigate} from 'react-router-dom';

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
    </div>
  );
}

export default App;
