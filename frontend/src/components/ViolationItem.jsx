import React from 'react';

const ViolationItem = ({ violation }) => {
    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'HIGH':
                return 'bg-red-500/10 text-red-400 border-red-500/20';
            case 'MEDIUM':
                return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
            case 'LOW':
                return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
            default:
                return 'bg-gray-500/10 text-gray-400 border-gray-500/20';
        }
    };

    return (
        <div className="flex items-start p-4 bg-gray-900/50 rounded-lg border border-gray-700/50">
            <div className={`flex-shrink-0 w-2 h-2 mt-2 rounded-full ${violation.severity === 'HIGH' ? 'bg-red-500' :
                    violation.severity === 'MEDIUM' ? 'bg-yellow-500' : 'bg-blue-500'
                }`} />

            <div className="ml-4 flex-1">
                <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-200">
                        Type: {violation.type}
                    </span>
                    <span className={`px-2 py-0.5 text-xs font-medium rounded-full border ${getSeverityColor(violation.severity)}`}>
                        {violation.severity}
                    </span>
                </div>

                <div className="mt-1">
                    <p className="text-sm text-gray-400">
                        <span className="font-mono bg-gray-800 px-1 py-0.5 rounded text-gray-300">
                            {violation.maskedText || violation.text}
                        </span>
                    </p>
                </div>

                <div className="mt-2 flex items-center text-xs text-gray-500">
                    <span>Confidence: {(violation.confidence * 100).toFixed(1)}%</span>
                </div>
            </div>
        </div>
    );
};

export default ViolationItem;
