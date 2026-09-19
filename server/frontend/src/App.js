import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import Dealers from "./components/Dealers/Dealers";
import RegisterPanel from "./components/Register/Register";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/register" element={<RegisterPanel />} />
    </Routes>
  );
}
export default App;
