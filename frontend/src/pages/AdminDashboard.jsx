import React, { useEffect, useRef, useState } from 'react';
import Navbar from '../components/Navbar';
import { getSystemStats, getGlobalViolations } from '../services/adminService';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { submitFalsePositiveFeedback } from '../utils/feedbackApi';

const AdminDashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [stats, setStats] = useState(null);
    const [violations, setViolations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [connectionState, setConnectionState] = useState('connecting');
    const [ipName, setIpName] = useState('');
    const [ipText, setIpText] = useState('');
    const [ipStatus, setIpStatus] = useState('');
    const streamRef = useRef(null);

    const handleFingerprint = async (e) => {
        e.preventDefault();
        try {
            setIpStatus('Fingerprinting...');
            const token = localStorage.getItem('token');
            const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
            const res = await fetch(`${apiBase}/admin/fingerprint`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
                body: JSON.stringify({ name: ipName, text: ipText })
            });
            if (res.ok) {
                setIpStatus('Success! Document Fingerprinted.');
                setIpName(''); setIpText('');
                setTimeout(() => setIpStatus(''), 3000);
            } else {
                setIpStatus('Error generating fingerprint.');
            }
        } catch (err) {
            setIpStatus('Error connecting to backend.');
        }
    };

    const handleFalsePositive = async (violation) => {
        try {
            await submitFalsePositiveFeedback(violation.text || violation.maskedText, []);
            setViolations(prev => prev.map(v => v._id === violation._id ? { ...v, feedbackSubmitted: true } : v));
        } catch (error) {
            console.error(error);
        }
    };

    const applySnapshot = (snapshot) => {
        if (!snapshot) {
            return;
        }

        if (snapshot.stats) {
            setStats(snapshot.stats);
        }

        if (Array.isArray(snapshot.violations)) {
            setViolations(snapshot.violations);
        }
    };

    useEffect(() => {
        if (!user || user.role !== 'admin') {
            navigate('/admin/login');
            return;
        }

        const token = localStorage.getItem('token');

        const fetchData = async () => {
            try {
                const [statsData, violationsData] = await Promise.all([
                    getSystemStats(),
                    getGlobalViolations()
                ]);
                setStats(statsData);
                setViolations(violationsData);
                setConnectionState('live');
            } catch (error) {
                console.error("Failed to fetch admin data", error);
                setConnectionState('disconnected');
            } finally {
                setLoading(false);
            }
        };

        const openStream = () => {
            if (!token) {
                setConnectionState('disconnected');
                return;
            }

            const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
            const streamUrl = `${apiBase.replace(/\/$/, '')}/admin/stream?token=${encodeURIComponent(token)}`;
            const eventSource = new EventSource(streamUrl);
            streamRef.current = eventSource;

            eventSource.addEventListener('snapshot', (event) => {
                try {
                    const snapshot = JSON.parse(event.data);
                    applySnapshot(snapshot);
                    setConnectionState('live');
                    setLoading(false);
                } catch (error) {
                    console.error('Failed to parse admin snapshot', error);
                }
            });

            eventSource.addEventListener('heartbeat', () => {
                setConnectionState('live');
            });

            eventSource.addEventListener('error', () => {
                setConnectionState('reconnecting');
            });
        };

        fetchData();
        openStream();

        return () => {
            if (streamRef.current) {
                streamRef.current.close();
                streamRef.current = null;
            }
        };
    }, [user, navigate]);

    if (loading) {
        return <div className="flex h-screen items-center justify-center bg-slate-50 text-slate-800 font-sans">Loading Admin Panel...</div>;
    }

    return (
        <div className="flex flex-col min-h-screen bg-slate-50 text-slate-800 font-sans">
            <div className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-50">
                <Navbar />
            </div>
            <main className="flex-1 p-8 overflow-y-auto relative z-0">
                <header className="mb-8">
                    <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">Admin Dashboard</h1>
                    <p className="text-slate-500 mt-2 text-lg">System overview and compliance monitoring.</p>
                    <p className="text-xs uppercase tracking-[0.2em] text-indigo-500 mt-3 font-bold flex items-center">
                        <span className={`w-2 h-2 rounded-full mr-2 ${connectionState === 'live' ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`}></span>
                        Live stream: {connectionState}
                    </p>
                </header>

                {/* Stats Grid */}
                {stats && (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                            <h3 className="text-slate-500 text-sm font-bold uppercase tracking-wider">Total Users</h3>
                            <p className="text-4xl font-extrabold mt-2 text-slate-900">{stats.userCount}</p>
                        </div>
                        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                            <h3 className="text-slate-500 text-sm font-bold uppercase tracking-wider">Total Uploads</h3>
                            <p className="text-4xl font-extrabold mt-2 text-slate-900">{stats.uploadCount}</p>
                        </div>
                        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                            <h3 className="text-slate-500 text-sm font-bold uppercase tracking-wider">Violations Detected</h3>
                            <p className="text-4xl font-extrabold mt-2 text-amber-500">{stats.violationCount}</p>
                        </div>
                        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                            <h3 className="text-slate-500 text-sm font-bold uppercase tracking-wider">High Risk Blocks</h3>
                            <p className="text-4xl font-extrabold mt-2 text-red-500">{stats.highRiskCount}</p>
                        </div>
                    </div>
                )}

                {/* Intellectual Property Fingerprinting */}
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm mb-8">
                    <h3 className="text-xl font-bold text-slate-800 flex items-center mb-4">
                        <svg className="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.071 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" /></svg>
                        Confidential IP Fingerprinting 
                    </h3>
                    <form onSubmit={handleFingerprint} className="space-y-4">
                        <div>
                            <input type="text" placeholder="Document Name (e.g. Q4 Strategy)" required value={ipName} onChange={e => setIpName(e.target.value)} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-sm text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all"/>
                        </div>
                        <div>
                            <textarea placeholder="Paste confidential document text here to generate a vector fingerprint..." required value={ipText} onChange={e => setIpText(e.target.value)} className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 h-32 text-sm text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all resize-none"></textarea>
                        </div>
                        <div className="flex items-center gap-4">
                            <button type="submit" className="px-6 py-2 bg-indigo-600 text-white font-bold rounded-lg text-sm shadow-md shadow-indigo-500/30 hover:bg-indigo-700 transition-all">Generate Fingerprint</button>
                            {ipStatus && <span className="text-sm font-semibold text-emerald-600">{ipStatus}</span>}
                        </div>
                    </form>
                </div>

                {/* Recent Violations Table */}
                <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
                    <div className="p-6 border-b border-slate-200 bg-slate-50/50">
                        <h3 className="text-xl font-bold text-slate-800 flex items-center">
                            <svg className="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                            Recent Violations
                        </h3>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm text-slate-600">
                            <thead className="bg-slate-50 text-slate-500 uppercase font-bold text-[11px] tracking-wider border-b border-slate-200">
                                <tr>
                                    <th className="px-6 py-4">Date</th>
                                    <th className="px-6 py-4">User</th>
                                    <th className="px-6 py-4">Type</th>
                                    <th className="px-6 py-4">Severity</th>
                                    <th className="px-6 py-4">Action</th>
                                    <th className="px-6 py-4">Details</th>
                                    <th className="px-6 py-4">Feedback</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100 bg-white">
                                {violations.map((v) => (
                                    <tr key={v._id} className="hover:bg-slate-50/80 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap font-medium text-slate-700">
                                            {new Date(v.createdAt).toLocaleDateString()}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap font-medium text-slate-700">
                                            {v.upload?.user?.email || 'Unknown'}
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md text-xs font-semibold">{v.type}</span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider ${v.severity === 'HIGH' ? 'bg-red-50 text-red-700 border border-red-200' :
                                                v.severity === 'MEDIUM' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                                                    'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                                }`}>
                                                {v.severity}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 font-semibold">
                                            {v.action === 'BLOCK' ? <span className="text-red-600">🚫 Blocked</span> : <span className="text-amber-600">⚠️ Warned</span>}
                                        </td>
                                        <td className="px-6 py-4 w-64 truncate text-slate-500 font-mono text-xs" title={v.text}>
                                            {v.maskedText || v.text?.substring(0, 30) + '...'}
                                        </td>
                                        <td className="px-6 py-4">
                                            {v.feedbackSubmitted ? (
                                                <span className="text-emerald-600 text-xs font-bold uppercase tracking-wider">Logged ✓</span>
                                            ) : (
                                                <button 
                                                    onClick={() => handleFalsePositive(v)}
                                                    className="px-3 py-1.5 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 font-semibold rounded-md text-xs transition-colors border border-indigo-200"
                                                >
                                                    Mark False Positive
                                                </button>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                                {violations.length === 0 && (
                                    <tr>
                                        <td colSpan="7" className="px-6 py-12 text-center text-slate-500 font-medium">
                                            No violations recorded yet.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default AdminDashboard;
