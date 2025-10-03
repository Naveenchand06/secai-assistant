import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import ExpandableScanResultCard from './ExpandableScanResultCard';
import { Copy } from 'lucide-react';

interface APIKey {
    key: string;
    created_at: string;
    expires_at: string;
    is_active: boolean;
}

interface Project {
    project_id: string;
    project_name: string;
    project_description: string;
    created_at: string;
    api_keys: APIKey[];
}

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

const ProjectDetailsScreen: React.FC = () => {
    const { projectId } = useParams<{ projectId: string }>();
    const [project, setProject] = useState<Project | null>(null);
    const [apiKeys, setApiKeys] = useState<APIKey[]>([]);
    const [scanResults, setScanResults] = useState<ScanResult[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();
    const { token } = useAuth();

    useEffect(() => {
        if (projectId) {
            fetchProjectDetails();
            fetchApiKeys();
            fetchScanResults();
        }
    }, [projectId]);

    const fetchScanResults = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/projects/${projectId}/scan-results`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setScanResults(data);
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to fetch scan results');
            }
        } catch (err) {
            setError('An error occurred while fetching scan results');
        }
    };

    const fetchProjectDetails = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/projects/${projectId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setProject(data);
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to fetch project details');
                navigate('/projects');
            }
        } catch (err) {
            setError('An error occurred while fetching project details');
            navigate('/projects');
        } finally {
            setLoading(false);
        }
    };

    const fetchApiKeys = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/projects/${projectId}/api-keys`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setApiKeys(data);
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to fetch API keys');
            }
        } catch (err) {
            setError('An error occurred while fetching API keys');
        }
    };

    const handleBack = () => {
        navigate('/projects');
    };

    const formatDate = (dateString: string) => {
        // return new Date(dateString).toLocaleDateString();
        return new Date(dateString).toLocaleString();
    };

    const handleCopy = (text: string) => {
        navigator.clipboard.writeText(text);
    };

    const isApiKeyExpired = (expiresAt: string) => {
        return new Date(expiresAt) < new Date();
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl mx-auto">
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl mx-auto">
                    <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg mb-6">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <div className="ml-3">
                                <p className="text-sm text-red-700">{error}</p>
                            </div>
                        </div>
                    </div>
                    <button
                        onClick={handleBack}
                        className="py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 shadow-lg hover:shadow-xl"
                    >
                        Back to Projects
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <button
                        onClick={handleBack}
                        className="py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition duration-300 shadow-lg hover:shadow-xl"
                    >
                        ← Back to Projects
                    </button>

                    <h1 className="text-3xl font-extrabold text-gray-900">Project Details</h1>

                    <Link
                        to={`/projects/${projectId}/api-keys`}
                        className="py-2 px-2 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 shadow-lg hover:shadow-xl"
                    >
                        Manage API Keys
                    </Link>
                </div>


                {project && (
                    <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">{project.project_name}</h2>
                        <p className="text-gray-900 mb-2 flex items-center gap-2">
                            <span className="font-bold">Project ID:</span> {project.project_id}
                            <button
                                onClick={() => handleCopy(project.project_id)}
                                className="text-gray-500 hover:text-gray-700 focus:outline-none"
                                aria-label="Copy Project ID"
                            >
                                <Copy size={16} />
                            </button>
                        </p>
                        <p className="text-gray-600 mb-4">{project.project_description || 'No description provided'}</p>
                        <div className="text-sm text-gray-500">
                            Created: {project.created_at ? formatDate(project.created_at) : 'Unknown date'}
                        </div>
                    </div>
                )}

                {success && (
                    <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded-lg mb-6">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <div className="ml-3">
                                <p className="text-sm text-green-700">{success}</p>
                            </div>
                        </div>
                    </div>
                )}

                {error && !loading && (
                    <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg mb-6">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <div className="ml-3">
                                <p className="text-sm text-red-700">{error}</p>
                            </div>
                        </div>
                    </div>
                )}

                <div className="bg-white p-6 rounded-xl shadow-lg">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-2xl font-bold text-gray-900">Scan Results</h2>
                        <button
                            onClick={fetchScanResults}
                            className="text-indigo-600 hover:text-indigo-800 focus:outline-none"
                            aria-label="Refresh scan results"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                        </button>
                    </div>

                    {scanResults.length === 0 ? (
                        <div className="text-center py-8">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <p className="text-gray-500">No Docker scan results available for this project yet.</p>
                        </div>
                    ) : (
                        <div className="space-y-6">
                            {[...scanResults].reverse().map((scanResult) => (
                                <ExpandableScanResultCard
                                    key={scanResult.id}
                                    scanResult={scanResult}
                                    formatDate={formatDate}
                                />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProjectDetailsScreen;
