import logo from './logo.svg';
import './App.css';
import SignInForm from "./components/SignInForm"
import SignUpForm from "./components/SignUpForm"

function App() {
  return (
    <div className="App">
      <SignInForm></SignInForm>
      <SignUpForm></SignUpForm>
    </div>
  );
}

export default App;
