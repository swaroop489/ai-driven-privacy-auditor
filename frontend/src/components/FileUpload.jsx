import React, { useState } from 'react';

const FileUpload = ({ onUpload, loading }) => {
    const [text, setText] = useState('');
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            // Create preview if it's an image
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
        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-6 shadow-xl">
            <h3 className="text-xl font-semibold text-white mb-6">Start New Audit</h3>

            <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                    <label className="block text-sm font-medium text-gray-400 mb-2">
                        Text Content (Optional)
                    </label>
                    <textarea
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Paste text here to scan for PII..."
                        className="w-full h-32 px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-gray-500 resize-none transition-all duration-200"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-400 mb-2">
                        Upload Image (Optional)
                    </label>
                    <div className="flex items-center justify-center w-full">
                        <label className="flex flex-col items-center justify-center w-full h-48 border-2 border-gray-700 border-dashed rounded-xl cursor-pointer hover:bg-gray-800/50 hover:border-blue-500/50 transition-all duration-300 group">
                            <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                {preview ? (
                                    <img src={preview} alt="Preview" className="max-h-36 rounded-lg object-contain" />
                                ) : (
                                    <>
                                        <svg className="w-10 h-10 mb-4 text-gray-500 group-hover:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                        </svg>
                                        <p className="mb-2 text-sm text-gray-400 group-hover:text-gray-300">
                                            <span className="font-semibold">Click to upload</span> or drag and drop
                                        </p>
                                        <p className="text-xs text-gray-500">PNG, JPG, JPEG</p>
                                    </>
                                )}
                            </div>
                            <input type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
                        </label>
                    </div>
                    {file && (
                        <div className="mt-2 text-sm text-gray-400 flex items-center justify-between">
                            <span>Selected: {file.name}</span>
                            <button type="button" onClick={() => { setFile(null); setPreview(null); }} className="text-red-400 hover:text-red-300">Remove</button>
                        </div>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={loading || (!text && !file)}
                    className={`w-full py-3.5 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 transform hover:-translate-y-0.5 transition-all duration-200 ${(loading || (!text && !file)) ? 'opacity-50 cursor-not-allowed transform-none' : ''
                        }`}
                >
                    {loading ? (
                        <div className="flex items-center justify-center">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Scanning...
                        </div>
                    ) : 'Run Security Scan'}
                </button>
            </form>
        </div>
    );
};

export default FileUpload;
