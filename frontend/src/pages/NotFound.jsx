import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
            <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600 mb-4">
                404
            </h1>
            <p className="text-xl text-gray-400 mb-8">Page Not Found</p>
            <Link
                to="/"
                className="px-6 py-3 bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
            >
                Go Home
            </Link>
        </div>
    );
};

export default NotFound;
