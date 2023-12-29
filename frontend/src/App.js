// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import Register from './Register';
import Login from './Login';
import Home from './Home'; // Assume you have a Home component

function App() {
    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    {/* Navigation Links */}
                    <nav>
                        <Link to="/">Home</Link> | {" "}
                        <Link to="/register">Register</Link> | {" "}
                        <Link to="/login">Login</Link>
                    </nav>

                    {/* Route Configuration */}
                    <Routes>
                        <Route exact path="/" element={Home} />
                        <Route path="/register" element={Register} />
                        <Route path="/login" element={Login} />
                    </Routes>
                </header>
            </div>
        </Router>
    );
}

export default App;
