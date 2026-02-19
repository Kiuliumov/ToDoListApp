import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./AuthProvider";
import ProtectedRoute from "./ProtectedRoute";

import Nav from "./Nav";
import Home from "./Home";
import About from "./About";
import Home from "./Home";
import Login from "./Login";

export default function App() {
  return (
    <AuthProvider>
      <Nav />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/login" element={<Login />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
      </Routes>
    </AuthProvider>
  );
}
