import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import FileUpload from '../components/FileUpload';
import ViolationItem from '../components/ViolationItem';
import ChatBox from '../components/ChatBox';
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
        <div className="flex flex-col min-h-screen bg-slate-50 text-slate-800 font-sans">
            <div className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-50">
                <Navbar />
            </div>

            <main className="flex-1 overflow-y-auto relative z-0">
                <div className="p-8 max-w-7xl mx-auto space-y-8">
                    <header className="mb-2">
                        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
                            Audit Dashboard
                        </h1>
                        <p className="text-slate-500 mt-2 text-lg">
                            Secure your content with AI-powered privacy auditing.
                        </p>
                    </header>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Left Column: Upload */}
                        <div>
                            <FileUpload onUpload={handleUpload} loading={loading} />
                        </div>

                        {/* Right Column: Results & Chat */}
                        <div className="flex flex-col space-y-6">
                            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                                <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center">
                                    <svg className="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                    Scan Results
                                </h3>

                                {error && (
                                    <div className="p-4 rounded-xl bg-red-50 border border-red-100 text-red-600 mb-4 shadow-sm">
                                        {error}
                                    </div>
                                )}

                                {!scanResult && !loading && !error && (
                                    <div className="flex flex-col items-center justify-center h-[300px] border-2 border-dashed border-slate-200 rounded-xl text-slate-400 bg-slate-50/50">
                                        <svg className="w-16 h-16 mb-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        <p className="font-medium">Results will appear here</p>
                                    </div>
                                )}

                                {scanResult && (
                                    <div className={`rounded-xl border p-6 transition-all duration-300 ${scanResult.action === 'BLOCK' ? 'bg-red-50 border-red-200' :
                                        scanResult.action === 'WARN' ? 'bg-amber-50 border-amber-200' :
                                            'bg-emerald-50 border-emerald-200'
                                        }`}>
                                    <div className="flex items-center justify-between mb-6">
                                        <div>
                                                <h4 className="text-lg font-bold text-slate-800">
                                                    Status: <span className={
                                                        scanResult.action === 'BLOCK' ? 'text-red-600' :
                                                            scanResult.action === 'WARN' ? 'text-amber-600' :
                                                                'text-emerald-600'
                                                    }>{scanResult.action}</span>
                                                </h4>
                                                <p className="text-sm text-slate-500 mt-1 font-medium">
                                                    Found {scanResult.violationCount} potential violations
                                                </p>
                                            </div>
                                            <div className={`p-3 rounded-full shadow-sm ${scanResult.action === 'BLOCK' ? 'bg-red-100 text-red-600' :
                                                scanResult.action === 'WARN' ? 'bg-amber-100 text-amber-600' :
                                                    'bg-emerald-100 text-emerald-600'
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

                                        <div className="space-y-3 mt-4">
                                            {scanResult.violations?.map((violation, index) => (
                                                <ViolationItem key={index} violation={violation} />
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>

                            <ChatBox />
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default UserDashboard;
