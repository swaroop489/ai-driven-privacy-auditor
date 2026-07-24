import React from 'react';

const ViolationItem = ({ violation }) => {
    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'HIGH':
                return 'bg-red-50 text-red-700 border-red-200';
            case 'MEDIUM':
                return 'bg-amber-50 text-amber-700 border-amber-200';
            case 'LOW':
                return 'bg-indigo-50 text-indigo-700 border-indigo-200';
            default:
                return 'bg-slate-100 text-slate-700 border-slate-200';
        }
    };

    return (
        <div className="flex items-start p-4 bg-white rounded-xl border border-slate-200 shadow-sm transition-all hover:shadow-md">
            <div className={`flex-shrink-0 w-2 h-2 mt-2 rounded-full ${violation.severity === 'HIGH' ? 'bg-red-500' :
                    violation.severity === 'MEDIUM' ? 'bg-amber-500' : 'bg-indigo-500'
                }`} />

            <div className="ml-4 flex-1">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-bold text-slate-800">
                        Type: <span className="font-semibold text-slate-600">{violation.type}</span>
                    </span>
                    <span className={`px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md border ${getSeverityColor(violation.severity)}`}>
                        {violation.severity}
                    </span>
                </div>

                <div className="mt-1">
                    <p className="text-sm text-slate-600">
                        <span className="font-mono bg-slate-50 border border-slate-200 px-1.5 py-0.5 rounded text-slate-700 font-medium">
                            {violation.maskedText || violation.text}
                        </span>
                    </p>
                </div>

                <div className="mt-3 flex items-center text-xs text-slate-400 font-medium">
                    <span>Confidence: {(violation.confidence * 100).toFixed(1)}%</span>
                </div>
            </div>
        </div>
    );
};

export default ViolationItem;
