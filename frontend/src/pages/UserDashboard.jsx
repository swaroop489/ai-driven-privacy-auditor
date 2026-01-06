import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import FileUpload from '../components/FileUpload';
import ViolationItem from '../components/ViolationItem';
import { uploadContent } from '../services/uploadService';

const UserDashboard = () => {
    const [scanResult, setScanResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleUpload = async ({ text, file }) => {
        setLoading(true);
        setError(null);
        setScanResult(null);

        try {
            const formData = new FormData();
            if (text) formData.append('text', text);
            if (file) formData.append('file', file);

            const result = await uploadContent(formData);
            setScanResult(result);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.message || 'Something went wrong during the scan.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-gray-900 text-white">
            <Sidebar />

            <main className="flex-1 overflow-y-auto md:ml-64">
                <div className="p-8 max-w-7xl mx-auto">
                    <header className="mb-8">
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                            Dashboard
                        </h1>
                        <p className="text-gray-400 mt-2">
                            Secure your content with AI-powered privacy auditing.
                        </p>
                    </header>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Left Column: Upload */}
                        <div>
                            <FileUpload onUpload={handleUpload} loading={loading} />
                        </div>

                        {/* Right Column: Results */}
                        <div>
                            <h3 className="text-xl font-semibold mb-6">Scan Results</h3>

                            {error && (
                                <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 mb-4">
                                    {error}
                                </div>
                            )}

                            {!scanResult && !loading && !error && (
                                <div className="flex flex-col items-center justify-center h-[400px] border-2 border-dashed border-gray-800 rounded-2xl text-gray-500">
                                    <svg className="w-16 h-16 mb-4 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <p>Results will appear here after scanning</p>
                                </div>
                            )}

                            {scanResult && (
                                <div className={`rounded-2xl border p-6 ${scanResult.action === 'BLOCK' ? 'bg-red-900/10 border-red-500/30' :
                                    scanResult.action === 'WARN' ? 'bg-yellow-900/10 border-yellow-500/30' :
                                        'bg-green-900/10 border-green-500/30'
                                    }`}>
                                    <div className="flex items-center justify-between mb-6">
                                        <div>
                                            <h4 className="text-lg font-bold">
                                                Status: <span className={
                                                    scanResult.action === 'BLOCK' ? 'text-red-400' :
                                                        scanResult.action === 'WARN' ? 'text-yellow-400' :
                                                            'text-green-400'
                                                }>{scanResult.action}</span>
                                            </h4>
                                            <p className="text-sm text-gray-400 mt-1">
                                                Found {scanResult.violationCount} potential violations
                                            </p>
                                        </div>
                                        <div className={`p-3 rounded-full ${scanResult.action === 'BLOCK' ? 'bg-red-500/20 text-red-400' :
                                            scanResult.action === 'WARN' ? 'bg-yellow-500/20 text-yellow-400' :
                                                'bg-green-500/20 text-green-400'
                                            }`}>
                                            {scanResult.action === 'BLOCK' ? (
                                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                                            ) : scanResult.action === 'WARN' ? (
                                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                                            ) : (
                                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" /></svg>
                                            )}
                                        </div>
                                    </div>

                                    <div className="space-y-3">
                                        {scanResult.violations?.map((violation, index) => (
                                            <ViolationItem key={index} violation={violation} />
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default UserDashboard;
