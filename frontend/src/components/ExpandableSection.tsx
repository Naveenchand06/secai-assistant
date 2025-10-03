import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ExpandableSectionProps {
    title: string;
    content: string;
    isMarkdown?: boolean;
}

const ExpandableSection: React.FC<ExpandableSectionProps> = ({ title, content, isMarkdown = false }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const toggleExpanded = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div className="border border-gray-200 rounded-lg p-4 mb-4">
            <div className="flex justify-between items-center cursor-pointer" onClick={toggleExpanded}>
                <h4 className="font-medium text-gray-900">{title}</h4>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className={`h-5 w-5 text-gray-500 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
                    viewBox="0 0 20 20"
                    fill="currentColor"
                >
                    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
            </div>
            {isExpanded && (
                <div className="mt-4">
                    {isMarkdown ? (
                        <div className="text-gray-700 prose prose-sm max-w-none">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {content}
                            </ReactMarkdown>
                        </div>
                    ) : (
                        <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                            {content}
                        </pre>
                    )}
                </div>
            )}
        </div>
    );
};

export default ExpandableSection;
