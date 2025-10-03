import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

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
    const [validityDays, setValidityDays] = useState(30);
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
            const response = await fetch(`http://localhost:8000/projects/${projectId}/scan-results`, {
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
            const response = await fetch(`http://localhost:8000/projects/${projectId}`, {
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
            const response = await fetch(`http://localhost:8000/projects/${projectId}/api-keys`, {
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

    const handleCreateApiKey = async () => {
        try {
            const response = await fetch(`http://localhost:8000/projects/${projectId}/api-keys`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ validity_days: validityDays })
            });

            if (response.ok) {
                const newApiKey = await response.json();
                setApiKeys([...apiKeys, newApiKey]);
                setSuccess('API key created successfully!');
                setError('');
                // Reset validity days to default
                setValidityDays(30);
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to create API key');
                setSuccess('');
            }
        } catch (err) {
            setError('An error occurred while creating API key');
            setSuccess('');
        }
    };

    const handleDeleteApiKey = async (apiKey: string) => {
        try {
            const response = await fetch(`http://localhost:8000/projects/${projectId}/api-keys/${apiKey}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                // Remove the deleted API key from the state
                setApiKeys(apiKeys.filter(key => key.key !== apiKey));
                setSuccess('API key deleted successfully!');
                setError('');
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to delete API key');
                setSuccess('');
            }
        } catch (err) {
            setError('An error occurred while deleting API key');
            setSuccess('');
        }
    };

    const handleBack = () => {
        navigate('/projects');
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString();
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
                    <div></div> {/* Empty div for spacing */}
                </div>

                {project && (
                    <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">{project.project_name}</h2>
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

                <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">API Keys</h2>

                    <div className="mb-6">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Create New API Key</h3>
                        <div className="flex items-center space-x-4">
                            <div>
                                <label htmlFor="validity" className="block text-sm font-medium text-gray-700 mb-1">
                                    Validity (days)
                                </label>
                                <input
                                    type="number"
                                    id="validity"
                                    min="1"
                                    max="365"
                                    value={validityDays}
                                    onChange={(e) => setValidityDays(parseInt(e.target.value) || 30)}
                                    className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                            <button
                                onClick={handleCreateApiKey}
                                disabled={apiKeys.length >= 3}
                                className={`py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 shadow-lg hover:shadow-xl mt-6 ${apiKeys.length >= 3
                                    ? 'bg-gray-400 cursor-not-allowed'
                                    : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700'
                                    }`}
                            >
                                Create API Key
                            </button>
                        </div>
                        {apiKeys.length >= 3 && (
                            <p className="text-sm text-red-600 mt-2">
                                You have reached the maximum number of API keys (3) for this project. Please delete an existing key to create a new one.
                            </p>
                        )}
                    </div>

                    {apiKeys.length === 0 ? (
                        <div className="text-center py-8">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                            </svg>
                            <p className="text-gray-500">No API keys have been created for this project yet.</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {apiKeys.map((apiKey) => (
                                <div key={apiKey.key} className="border border-gray-200 rounded-lg p-4">
                                    <div className="flex justify-between items-start">
                                        <div className="flex-1">
                                            <div className="flex items-center space-x-2 mb-2">
                                                <code className="text-sm font-mono bg-gray-100 p-2 rounded flex-1 break-all">
                                                    {apiKey.key}
                                                </code>
                                            </div>
                                            <div className="grid grid-cols-2 gap-2 text-sm text-gray-600">
                                                <div>
                                                    <span className="font-medium">Created:</span> {formatDate(apiKey.created_at)}
                                                </div>
                                                <div>
                                                    <span className="font-medium">Expires:</span> {formatDate(apiKey.expires_at)}
                                                </div>
                                                <div>
                                                    <span className="font-medium">Status:</span>
                                                    <span className={`ml-2 px-2 py-1 rounded text-xs ${isApiKeyExpired(apiKey.expires_at)
                                                        ? 'bg-red-100 text-red-800'
                                                        : apiKey.is_active
                                                            ? 'bg-green-100 text-green-800'
                                                            : 'bg-yellow-100 text-yellow-800'
                                                        }`}>
                                                        {isApiKeyExpired(apiKey.expires_at) ? 'Expired' : apiKey.is_active ? 'Active' : 'Inactive'}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => handleDeleteApiKey(apiKey.key)}
                                            className="ml-4 py-1 px-3 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition duration-300 shadow hover:shadow-lg"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                <div className="bg-white p-6 rounded-xl shadow-lg">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">Docker Scan Results</h2>

                    {scanResults.length === 0 ? (
                        <div className="text-center py-8">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <p className="text-gray-500">No Docker scan results available for this project yet.</p>
                        </div>
                    ) : (
                        <div className="space-y-6">
                            {scanResults.map((scanResult) => (
                                <div key={scanResult.id} className="border border-gray-200 rounded-lg p-4">
                                    <div className="flex justify-between items-center mb-3">
                                        <h3 className="text-lg font-medium text-gray-900">Scan Result</h3>
                                        <span className="text-sm text-gray-500">
                                            {scanResult.created_at ? formatDate(scanResult.created_at) : 'Unknown date'}
                                        </span>
                                    </div>

                                    <div className="mb-4">
                                        <h4 className="font-medium text-gray-900 mb-2">Summary</h4>
                                        <p className="text-gray-700">{scanResult.human_readable}</p>
                                    </div>

                                    <div className="mb-4">
                                        <h4 className="font-medium text-gray-900 mb-2">Risk Analysis</h4>
                                        <p className="text-gray-700">{scanResult.risk_analysis}</p>
                                    </div>

                                    <div className="mb-4">
                                        <h4 className="font-medium text-gray-900 mb-2">Solutions</h4>
                                        <p className="text-gray-700">{scanResult.solutions}</p>
                                    </div>

                                    <div>
                                        <h4 className="font-medium text-gray-900 mb-2">Raw Scan Data</h4>
                                        <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                                            {JSON.stringify(scanResult.scan_data, null, 2)}
                                        </pre>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProjectDetailsScreen;
