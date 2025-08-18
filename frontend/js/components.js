import React from 'https://unpkg.com/react@18/umd/react.production.min.js';

// ChatMessage component displays a single message in the chat.
const ChatMessage = ({ message }) => {
    const { role, text } = message;
    const isUser = role === 'user';
    return (
        <div className={`flex items-start mb-4 ${isUser ? 'justify-end' : ''}`}>
            <div className={`p-4 rounded-xl max-w-lg shadow-md ${isUser ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-gray-800 text-gray-200 rounded-tl-none'}`}>
                <p className="whitespace-pre-wrap">{text}</p>
            </div>
        </div>
    );
};

// LoadingIndicator component shows a typing animation when the AI is responding.
const LoadingIndicator = () => (
    <div className="flex items-start mb-4">
        <div className="p-4 rounded-xl bg-gray-800 text-gray-200">
            <div className="dot-pulse"></div>
        </div>
    </div>
);

// InputForm component for user input.
const InputForm = ({ prompt, onPromptChange, onSendMessage, isLoading }) => (
    <footer className="fixed bottom-0 left-0 right-0 p-4 bg-gray-950 flex items-center justify-center">
        <form onSubmit={(e) => { e.preventDefault(); onSendMessage(); }} className="flex w-full max-w-4xl space-x-2">
            <input
                type="text"
                value={prompt}
                onChange={(e) => onPromptChange(e.target.value)}
                className="flex-grow p-3 rounded-full bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
                placeholder="Type your prompt here..."
                disabled={isLoading}
            />
            <button
                type="submit"
                className="p-3 rounded-full bg-indigo-600 text-white w-12 h-12 flex items-center justify-center hover:bg-indigo-700 transition-colors disabled:opacity-50"
                disabled={isLoading}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
            </button>
        </form>
    </footer>
);

// SettingsPanel component for tone, genre, and mode selection.
const SettingsPanel = ({ mode, onModeChange, settings, onSettingsChange }) => (
    <div className="flex flex-col space-y-4 p-4 bg-gray-800 rounded-xl shadow-inner mb-4">
        <h2 className="text-xl font-bold text-white">Story Settings</h2>

        {/* Mode Toggle */}
        <div className="flex items-center justify-between">
            <span className="text-gray-400">AI Mode:</span>
            <div className="flex space-x-2 bg-gray-700 p-1 rounded-full">
                <button
                    onClick={() => onModeChange('censored')}
                    className={`px-4 py-2 rounded-full font-medium transition-colors ${mode === 'censored' ? 'bg-indigo-600 text-white' : 'bg-transparent text-gray-400 hover:text-white'}`}
                >
                    Censored
                </button>
                <button
                    onClick={() => onModeChange('uncensored')}
                    className={`px-4 py-2 rounded-full font-medium transition-colors ${mode === 'uncensored' ? 'bg-indigo-600 text-white' : 'bg-transparent text-gray-400 hover:text-white'}`}
                >
                    Uncensored
                </button>
            </div>
        </div>

        {/* Tone and Genre Selection */}
        <div className="flex space-x-4">
            <div className="flex-1">
                <label className="text-gray-400 block mb-1">Tone</label>
                <select
                    value={settings.tone}
                    onChange={(e) => onSettingsChange({ ...settings, tone: e.target.value })}
                    className="w-full p-2 rounded-lg bg-gray-700 border border-gray-600 text-gray-200 focus:outline-none focus:border-indigo-500"
                >
                    <option>Fantasy</option>
                    <option>Sci-Fi</option>
                    <option>Horror</option>
                    <option>Comedy</option>
                </select>
            </div>
            <div className="flex-1">
                <label className="text-gray-400 block mb-1">Genre</label>
                <select
                    value={settings.genre}
                    onChange={(e) => onSettingsChange({ ...settings, genre: e.target.value })}
                    className="w-full p-2 rounded-lg bg-gray-700 border border-gray-600 text-gray-200 focus:outline-none focus:border-indigo-500"
                >
                    <option>Adventure</option>
                    <option>Mystery</option>
                    <option>Survival</option>
                    <option>Epic</option>
                </select>
            </div>
        </div>
    </div>
);

// Define a simple modal for user alerts, since window.alert is not permitted
const Modal = ({ title, message, onClose }) => {
    return (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
            <div className="bg-gray-800 p-6 rounded-lg shadow-xl max-w-sm w-full">
                <h3 className="text-xl font-bold text-white mb-4">{title}</h3>
                <p className="text-gray-300 mb-4">{message}</p>
                <div className="flex justify-end">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};

export { ChatMessage, LoadingIndicator, InputForm, SettingsPanel, Modal };
