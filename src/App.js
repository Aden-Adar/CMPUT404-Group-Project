// https://bobbyhadz.com/blog/react-onclick-redirect

import './App.css';
import SignInForm from "./components/SignInForm";
import SignUpForm from "./components/SignUpForm";
import {Routes, Route, useNavigate} from 'react-router-dom';
import { Main } from './MainPage/Main';

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
          <Route path="/createaccount" element={<SignUpForm />} />
          <Route path="/main" element={<Main />} />
        </Routes>
    
    </div>
  );
}

export default App;
