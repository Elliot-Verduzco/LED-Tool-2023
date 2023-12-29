// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Register from './Register';
import Login from './Login';
import Home from './Home';
import UserPortal from './UserPortal';

function App() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    {/* Navigation Links */}
                    <nav>
                        <Link to="/">Home</Link> | {" "}
                        <Link to="/register">Register</Link> | {" "}
                        <Link to="/login">Login</Link>
                        {isLoggedIn && <Link to="/portal">User Portal</Link>}
                    </nav>

                    {/* Route Configuration */}
                    <Routes>
                        <Route exact path="/" element={<Home />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/portal" element={isLoggedIn ? <UserPortal /> : <Navigate to="/login" />} />
                    </Routes>
                </header>
            </div>
        </Router>
    );
}

export default App;