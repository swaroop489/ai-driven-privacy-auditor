import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    return (
        <header className="container mx-auto px-6 py-6 flex justify-between items-center relative z-20">
            <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
                <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-indigo-600 rounded-lg flex items-center justify-center shadow-md">
                    <span className="text-white font-bold text-lg">🛡️</span>
                </div>
                <span className="text-xl font-bold tracking-tight text-slate-900">Privacy<span className="text-teal-600">Auditor</span></span>
            </div>

            <nav className="hidden md:flex gap-8 text-sm font-medium text-slate-600">
                <a href="/#features" className="hover:text-teal-600 transition-colors">Features</a>
                <a href="/#how-it-works" className="hover:text-teal-600 transition-colors">How it Works</a>
                <a href="/#about" className="hover:text-teal-600 transition-colors">About</a>
            </nav>

            <div className="flex gap-4 items-center">
                {!user ? (
                    <>
                        <button onClick={() => navigate('/login')} className="hidden md:block px-4 py-2 text-sm font-medium text-slate-600 hover:text-teal-600 transition-colors">
                            Log In
                        </button>
                        <button onClick={() => navigate('/register')} className="px-5 py-2 text-sm font-medium bg-gradient-to-r from-teal-500 to-indigo-600 text-white rounded-full hover:shadow-lg hover:shadow-teal-500/25 transition-all transform hover:-translate-y-0.5">
                            Register
                        </button>
                    </>
                ) : (
                    <>
                        <button onClick={() => navigate('/dashboard')} className="hidden md:block px-5 py-2 text-sm font-medium bg-gradient-to-r from-teal-500 to-indigo-600 text-white rounded-full hover:shadow-lg hover:shadow-teal-500/25 transition-all transform hover:-translate-y-0.5">
                            Internal System
                        </button>

                        <div className="relative">
                            <button
                                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                                className="w-10 h-10 rounded-full bg-slate-200 border-2 border-white shadow-sm flex items-center justify-center hover:shadow-md transition-all focus:outline-none"
                            >
                                <span className="text-xl">👤</span>
                            </button>

                            {isDropdownOpen && (
                                <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-100 overflow-hidden transform origin-top-right transition-all animate-fade-in-up">
                                    <div className="px-4 py-3 bg-slate-50 border-b border-slate-100">
                                        <p className="text-sm font-bold text-slate-900 truncate">{user.name}</p>
                                        <p className="text-xs text-slate-500 truncate">{user.email}</p>
                                    </div>
                                    <div className="py-1">
                                        <button
                                            onClick={() => {
                                                logout();
                                                setIsDropdownOpen(false);
                                                navigate('/');
                                            }}
                                            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors flex items-center gap-2"
                                        >
                                            <span>🚪</span> Logout
                                        </button>
                                    </div>
                                </div>
                            )}
                        </div>
                    </>
                )}
            </div>
        </header>
    );
};

export default Navbar;
