import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';




    const Home = () => {
        const navigate = useNavigate();

        return (
            <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-teal-500 selection:text-white">
                {/* Decorative Background Elements */}
                <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
                    <div className="absolute top-[-10%] left-[-10%] w-[40rem] h-[40rem] bg-indigo-200/40 rounded-full blur-3xl mix-blend-multiply" />
                    <div className="absolute bottom-[-10%] right-[-10%] w-[40rem] h-[40rem] bg-teal-200/40 rounded-full blur-3xl mix-blend-multiply" />
                </div>

                {/* Main Content */}
                <div className="relative z-10">

                    {/* Navigation */}
                    <Navbar />

                    {/* Hero Section */}
                    <section className="container mx-auto px-6 py-20 md:py-32 text-center">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 backdrop-blur-sm mb-8 animate-fade-in-up shadow-sm">
                            <span className="w-2 h-2 rounded-full bg-teal-500 animate-pulse" />
                            <span className="text-xs font-bold text-teal-700 uppercase tracking-wide">AI-Powered Protection</span>
                        </div>

                        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 leading-tight text-slate-900">
                            Stop Data Leaks <br className="hidden md:block" />
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-600 via-indigo-600 to-purple-600">
                                Before They Happen
                            </span>
                        </h1>

                        <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto mb-12 leading-relaxed">
                            Automatically detect and block sensitive PII in text and images (IDs, Phone Numbers, Locations) using advanced NLP and OCR technologies.
                        </p>

                        <div className="flex flex-col md:flex-row gap-4 justify-center items-center">
                            <button className="px-8 py-4 bg-slate-900 text-white rounded-full font-bold text-lg hover:bg-slate-800 transition-all transform hover:scale-105 shadow-xl shadow-slate-900/10">
                                Start Auditing Now
                            </button>
                            <button className="px-8 py-4 bg-white text-slate-700 border border-slate-200 backdrop-blur-sm rounded-full font-semibold text-lg hover:bg-slate-50 transition-all shadow-sm">
                                View Documentation
                            </button>
                        </div>

                        {/* Hero Visual/Stats */}
                        <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
                            <div className="p-4 rounded-2xl bg-white/60 border border-slate-200 backdrop-blur-sm shadow-sm">
                                <div className="text-2xl font-bold text-slate-900">99.9%</div>
                                <div className="text-sm text-slate-500">Accuracy</div>
                            </div>
                            <div className="p-4 rounded-2xl bg-white/60 border border-slate-200 backdrop-blur-sm shadow-sm">
                                <div className="text-2xl font-bold text-slate-900">&lt;1s</div>
                                <div className="text-sm text-slate-500">Latency</div>
                            </div>
                            <div className="p-4 rounded-2xl bg-white/60 border border-slate-200 backdrop-blur-sm shadow-sm">
                                <div className="text-2xl font-bold text-slate-900">24/7</div>
                                <div className="text-sm text-slate-500">Monitoring</div>
                            </div>
                            <div className="p-4 rounded-2xl bg-white/60 border border-slate-200 backdrop-blur-sm shadow-sm">
                                <div className="text-2xl font-bold text-slate-900">GDPR</div>
                                <div className="text-sm text-slate-500">Compliant</div>
                            </div>
                        </div>
                    </section>

                    {/* Features Section */}
                    <section id="features" className="container mx-auto px-6 py-24 border-t border-slate-200">
                        <div className="text-center mb-16">
                            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-slate-900">Powerful Detection Capabilities</h2>
                            <p className="text-slate-600 max-w-xl mx-auto">Our multi-layered AI approach ensures deeper inspection of your content stream.</p>
                        </div>

                        <div className="grid md:grid-cols-3 gap-8">
                            {/* Feature 1 */}
                            <div className="group p-8 rounded-3xl bg-white border border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                                <div className="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-indigo-600 transition-colors duration-300">
                                    <span className="text-3xl group-hover:text-white transition-colors">🧠</span>
                                </div>
                                <h3 className="text-xl font-bold mb-3 text-slate-900 group-hover:text-indigo-600 transition-colors">NLP Context Analysis</h3>
                                <p className="text-slate-500 leading-relaxed group-hover:text-slate-600">
                                    Goes beyond regex. Our NLP models understand context to accurately identify names, addresses, and medical data even in unstructured text.
                                </p>
                            </div>

                            {/* Feature 2 */}
                            <div className="group p-8 rounded-3xl bg-white border border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                                <div className="w-14 h-14 bg-teal-50 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-teal-500 transition-colors duration-300">
                                    <span className="text-3xl group-hover:text-white transition-colors">📷</span>
                                </div>
                                <h3 className="text-xl font-bold mb-3 text-slate-900 group-hover:text-teal-600 transition-colors">OCR Image Scanning</h3>
                                <p className="text-slate-500 leading-relaxed group-hover:text-slate-600">
                                    Extracts text from screenshots, scanned documents, and ID cards to find hidden PII that standard text filters miss.
                                </p>
                            </div>

                            {/* Feature 3 */}
                            <div className="group p-8 rounded-3xl bg-white border border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                                <div className="w-14 h-14 bg-purple-50 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-purple-600 transition-colors duration-300">
                                    <span className="text-3xl group-hover:text-white transition-colors">🛡️</span>
                                </div>
                                <h3 className="text-xl font-bold mb-3 text-slate-900 group-hover:text-purple-600 transition-colors">Real-Time Alerts</h3>
                                <p className="text-slate-500 leading-relaxed group-hover:text-slate-600">
                                    Instant notifications for admins with severity grading. Automatically block high-risk posts before they go public.
                                </p>
                            </div>
                        </div>
                    </section>

                    {/* How it works */}
                    <section id="how-it-works" className="py-24 bg-slate-50/50 relative overflow-hidden border-t border-slate-200">
                        <div className="container mx-auto px-6 relative z-10">
                            <div className="text-center mb-16">
                                <h2 className="text-3xl md:text-4xl font-bold mb-4 text-slate-900">How It Works</h2>
                                <p className="text-slate-600">Seamless integration into your workflow.</p>
                            </div>

                            <div className="flex flex-col md:flex-row items-center justify-center gap-8 relative">
                                {/* Connecting Line (Desktop) */}
                                <div className="hidden md:block absolute top-1/2 left-20 right-20 h-0.5 bg-gradient-to-r from-slate-200 via-teal-500/50 to-slate-200 -z-10" />

                                {/* Step 1 */}
                                <div className="relative text-center w-full md:w-1/3 p-6 group">
                                    <div className="w-20 h-20 mx-auto bg-white border-4 border-slate-100 rounded-full flex items-center justify-center text-3xl mb-6 z-10 relative shadow-md group-hover:scale-110 transition-transform">
                                        📤
                                    </div>
                                    <h4 className="text-lg font-bold mb-2 text-slate-900">1. Upload</h4>
                                    <p className="text-sm text-slate-500">Users upload text or images via the platform.</p>
                                </div>

                                {/* Step 2 */}
                                <div className="relative text-center w-full md:w-1/3 p-6 group">
                                    <div className="w-20 h-20 mx-auto bg-white border-4 border-teal-50 rounded-full flex items-center justify-center text-3xl mb-6 shadow-xl shadow-teal-500/10 z-10 relative group-hover:scale-110 transition-transform">
                                        ⚡
                                    </div>
                                    <h4 className="text-lg font-bold mb-2 text-teal-600">2. Scan & Analyze</h4>
                                    <p className="text-sm text-slate-500">AI engines process data instantly for PII patterns.</p>
                                </div>

                                {/* Step 3 */}
                                <div className="relative text-center w-full md:w-1/3 p-6 group">
                                    <div className="w-20 h-20 mx-auto bg-white border-4 border-slate-100 rounded-full flex items-center justify-center text-3xl mb-6 z-10 relative shadow-md group-hover:scale-110 transition-transform">
                                        🔔
                                    </div>
                                    <h4 className="text-lg font-bold mb-2 text-slate-900">3. Action</h4>
                                    <p className="text-sm text-slate-500">Safe content is posted; violations are flagged locally.</p>
                                </div>
                            </div>
                        </div>
                    </section>

                    {/* Footer */}
                    <footer className="py-12 border-t border-slate-200 bg-white text-center text-slate-500 text-sm">
                        <p>&copy; {new Date().getFullYear()} AI-Driven Privacy Auditor. Built for safety.</p>
                    </footer>

                </div>
            </div>
        );
    };

    export default Home;
