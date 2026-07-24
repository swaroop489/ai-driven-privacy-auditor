import React, { useState } from 'react';

const FileUpload = ({ onUpload, loading }) => {
    const [text, setText] = useState('');
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            if (selectedFile.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onloadend = () => {
                    setPreview(reader.result);
                };
                reader.readAsDataURL(selectedFile);
            } else {
                setPreview(null);
            }
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onUpload({ text, file });
    };

    return (
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
            <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center">
                <svg className="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                Start New Audit
            </h3>

            <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">
                        Text Content (Optional)
                    </label>
                    <textarea
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Paste text here to scan for PII..."
                        className="w-full h-32 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-slate-800 placeholder-slate-400 resize-none transition-all shadow-inner"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">
                        Upload Media (Image, Audio, Video)
                    </label>
                    <div className="flex items-center justify-center w-full">
                        <label className="flex flex-col items-center justify-center w-full h-48 border-2 border-slate-300 border-dashed rounded-xl cursor-pointer hover:bg-indigo-50 hover:border-indigo-400 transition-all group bg-slate-50">
                            <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                {preview ? (
                                    <img src={preview} alt="Preview" className="max-h-36 rounded-lg object-contain shadow-sm" />
                                ) : (
                                    <>
                                        <svg className="w-10 h-10 mb-4 text-slate-400 group-hover:text-indigo-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                        </svg>
                                        <p className="mb-2 text-sm text-slate-600 group-hover:text-slate-800">
                                            <span className="font-semibold">Click to upload</span> or drag and drop
                                        </p>
                                        <p className="text-xs text-slate-500">PNG, JPG, MP3, WAV, MP4, MOV</p>
                                    </>
                                )}
                            </div>
                            <input type="file" className="hidden" onChange={handleFileChange} accept="image/*, audio/*, video/*" />
                        </label>
                    </div>
                    {file && (
                        <div className="mt-3 text-sm text-slate-600 flex items-center justify-between bg-slate-100 px-3 py-2 rounded-lg">
                            <span className="font-medium truncate mr-4">Selected: {file.name}</span>
                            <button type="button" onClick={() => { setFile(null); setPreview(null); }} className="text-red-500 hover:text-red-700 font-semibold">Remove</button>
                        </div>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={loading || (!text && !file)}
                    className={`w-full py-3.5 px-4 bg-indigo-600 text-white font-bold rounded-xl shadow-md hover:bg-indigo-700 hover:shadow-lg transition-all ${(loading || (!text && !file)) ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                >
                    {loading ? (
                        <div className="flex items-center justify-center">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Scanning Data...
                        </div>
                    ) : 'Run Security Scan'}
                </button>
            </form>
        </div>
    );
};

export default FileUpload;
