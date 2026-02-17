import React, { useState } from 'react';
import axios from 'axios';
import './AuthComponent.css';

const API_URL = "https://revolution-backend.vercel.app/api";

const AuthComponent = ({ onAuthSuccess }) => {
    const [isLogin, setIsLogin] = useState(false);
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        const endpoint = isLogin ? 'login' : 'signup';
        try {
            const res = await axios.post(`${API_URL}/auth/${endpoint}`, formData);
            if (res.data.user_id) {
                localStorage.setItem('lux_user_id', res.data.user_id);
                onAuthSuccess(res.data.user_id);
            }
        } catch (err) {
            console.error("Auth failed", err);
            alert(isLogin ? "Login failed. Check credentials." : "Signup failed.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="lux-auth-container">
            <div className="lux-auth-card">
                <h2 className="lux-auth-title">{isLogin ? 'Member Login' : 'Join the Revolution'}</h2>
                <p className="lux-auth-subtitle">[V3.1] {isLogin ? 'Verify your identity to proceed.' : 'Identify yourself to enter the new era.'}</p>

                <form onSubmit={handleSubmit} className="lux-auth-form">
                    <div className="lux-input-group">
                        <input
                            type="email"
                            placeholder="Email Identifier"
                            required
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        />
                    </div>
                    <div className="lux-input-group">
                        <input
                            type="password"
                            placeholder="Access Key"
                            required
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        />
                    </div>

                    <button type="submit" className="lux-auth-btn" disabled={isLoading}>
                        {isLoading ? 'Processing...' : (isLogin ? 'Enter' : 'Initialize')}
                    </button>
                </form>

                <div className="lux-auth-toggle">
                    {isLogin ? "New to the Revolution?" : "Already recognized?"}{" "}
                    <span onClick={() => setIsLogin(!isLogin)}>
                        {isLogin ? 'Register Identity' : 'Secure Login'}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default AuthComponent;
