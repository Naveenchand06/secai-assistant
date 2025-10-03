import React, { useState } from 'react';
import ExpandableSection from './ExpandableSection';

interface ScanResult {
    id: string;
    status: string;
    message: string;
    human_readable: string;
    risk_analysis: string;
    solutions: string;
    scan_data: any;
    created_at: string;
}

interface ExpandableScanResultCardProps {
    scanResult: ScanResult;
    formatDate: (dateString: string) => string;
}

const ExpandableScanResultCard: React.FC<ExpandableScanResultCardProps> = ({ scanResult, formatDate }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const toggleExpanded = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div className="border-2 border-gray-200 rounded-lg hover:border-2 hover:border-violet-500 transition-all duration-200">
            <div
                className="flex justify-between items-center p-4 cursor-pointer bg-white rounded-lg"
                onClick={toggleExpanded}
            >
                <h3 className="text-lg font-medium text-gray-900">
                    Scan Result #{scanResult.id}
                </h3>
                <div className="flex items-center">
                    <span className="text-sm text-gray-500 mr-2">
                        {scanResult.created_at ? formatDate(scanResult.created_at) : 'Unknown date'}
                    </span>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className={`h-5 w-5 text-gray-500 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                </div>
            </div>

            {isExpanded && (
                <div className="p-4 bg-gray-50 border-t border-gray-200 rounded-b-lg">
                    <ExpandableSection
                        title="Summary"
                        content={scanResult.human_readable}
                        isMarkdown={true}
                    />

                    <ExpandableSection
                        title="Risk Analysis"
                        content={scanResult.risk_analysis}
                        isMarkdown={true}
                    />

                    <ExpandableSection
                        title="Solutions"
                        content={scanResult.solutions}
                        isMarkdown={true}
                    />

                    <ExpandableSection
                        title="Raw Scan Data"
                        content={JSON.stringify(scanResult.scan_data, null, 2)}
                        isMarkdown={false}
                    />
                </div>
            )}
        </div>
    );
};

export default ExpandableScanResultCard;
