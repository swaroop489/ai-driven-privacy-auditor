import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import { getSystemStats, getGlobalViolations } from '../services/adminService';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [stats, setStats] = useState(null);
    const [violations, setViolations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (user && user.role !== 'admin') {
            navigate('/dashboard'); // Redirect non-admins
            return;
        }

        const fetchData = async () => {
            try {
                const [statsData, violationsData] = await Promise.all([
                    getSystemStats(),
                    getGlobalViolations()
                ]);
                setStats(statsData);
                setViolations(violationsData);
            } catch (error) {
                console.error("Failed to fetch admin data", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [user, navigate]);

    if (loading) {
        return <div className="flex h-screen items-center justify-center bg-gray-900 text-white">Loading Admin Panel...</div>;
    }

    return (
        <div className="flex h-screen bg-gray-900 text-white">
            <Sidebar />
            <main className="flex-1 p-8 md:ml-64 overflow-y-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold">Admin Dashboard</h1>
                    <p className="text-gray-400">System overview and compliance monitoring.</p>
                </header>

                {/* Stats Grid */}
                {stats && (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
                            <h3 className="text-gray-400 text-sm font-medium">Total Users</h3>
                            <p className="text-3xl font-bold mt-2">{stats.userCount}</p>
                        </div>
                        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
                            <h3 className="text-gray-400 text-sm font-medium">Total Uploads</h3>
                            <p className="text-3xl font-bold mt-2">{stats.uploadCount}</p>
                        </div>
                        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
                            <h3 className="text-gray-400 text-sm font-medium">Violations Detected</h3>
                            <p className="text-3xl font-bold mt-2 text-yellow-500">{stats.violationCount}</p>
                        </div>
                        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
                            <h3 className="text-gray-400 text-sm font-medium">High Risk Blocks</h3>
                            <p className="text-3xl font-bold mt-2 text-red-500">{stats.highRiskCount}</p>
                        </div>
                    </div>
                )}

                {/* Recent Violations Table */}
                <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
                    <div className="p-6 border-b border-gray-700">
                        <h3 className="text-lg font-bold">Recent Violations</h3>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm text-gray-400">
                            <thead className="bg-gray-700/50 text-gray-200 uppercase font-medium">
                                <tr>
                                    <th className="px-6 py-4">Date</th>
                                    <th className="px-6 py-4">User</th>
                                    <th className="px-6 py-4">Type</th>
                                    <th className="px-6 py-4">Severity</th>
                                    <th className="px-6 py-4">Action</th>
                                    <th className="px-6 py-4">Details</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {violations.map((v) => (
                                    <tr key={v._id} className="hover:bg-gray-700/30 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {new Date(v.createdAt).toLocaleDateString()}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {v.upload?.user?.email || 'Unknown'}
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="px-2 py-1 bg-gray-700 rounded text-xs">{v.type}</span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded text-xs font-bold ${v.severity === 'HIGH' ? 'bg-red-500/10 text-red-400' :
                                                    v.severity === 'MEDIUM' ? 'bg-yellow-500/10 text-yellow-400' :
                                                        'bg-green-500/10 text-green-400'
                                                }`}>
                                                {v.severity}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            {v.action === 'BLOCK' ? '🚫 Blocked' : '⚠️ Warned'}
                                        </td>
                                        <td className="px-6 py-4 w-64 truncate" title={v.text}>
                                            {v.maskedText || v.text?.substring(0, 30) + '...'}
                                        </td>
                                    </tr>
                                ))}
                                {violations.length === 0 && (
                                    <tr>
                                        <td colSpan="6" className="px-6 py-12 text-center text-gray-500">
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
