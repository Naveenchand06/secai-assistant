import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LandingScreen: React.FC = () => {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const handleCreateProject = () => {
        navigate('/create-project');
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-extrabold text-gray-900 mb-4">
                        Welcome to SecAI Assistant
                    </h1>
                    <p className="text-xl text-gray-600 mb-8">
                        Your project has been successfully created!
                    </p>
                    <div className="flex justify-center space-x-4">
                        <button
                            onClick={handleCreateProject}
                            className="py-3 px-6 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition duration-300 shadow-lg hover:shadow-xl"
                        >
                            Create Another Project
                        </button>
                        <button
                            onClick={handleLogout}
                            className="py-3 px-6 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 shadow-lg hover:shadow-xl"
                        >
                            Logout
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="bg-white p-6 rounded-xl shadow-lg bg-gradient-to-br from-white to-gray-50 transition duration-300 hover:shadow-xl">
                        <div className="text-indigo-600 mb-4">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                        </div>
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">Security Analysis</h3>
                        <p className="text-gray-600">
                            Upload your code for comprehensive security scanning
                        </p>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-lg bg-gradient-to-br from-white to-gray-50 transition duration-300 hover:shadow-xl">
                        <div className="text-indigo-600 mb-4">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                            </svg>
                        </div>
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">AI Recommendations</h3>
                        <p className="text-gray-600">
                            Get intelligent suggestions to improve your code security
                        </p>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-lg bg-gradient-to-br from-white to-gray-50 transition duration-300 hover:shadow-xl">
                        <div className="text-indigo-600 mb-4">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                            </svg>
                        </div>
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">Project Management</h3>
                        <p className="text-gray-600">
                            Track and manage your security analysis projects
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LandingScreen;
