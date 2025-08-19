import React, { useState, useEffect, useRef } from 'https://unpkg.com/react@18/umd/react.production.min.js';
import ReactDOM from 'https://unpkg.com/react-dom@18/umd/react-dom.production.min.js';
import { initializeApp } from 'https://www.gstatic.com/firebasejs/12.1.0/firebase-app.js';
import { getAuth, signInAnonymously, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/12.1.0/firebase-auth.js';
import { getFirestore, doc, getDoc, addDoc, collection } from 'https://www.gstatic.com/firebasejs/12.1.0/firebase-firestore.js';
import { ChatMessage, LoadingIndicator, InputForm, SettingsPanel, Modal } from './components.js';

// Main application component
const App = () => {
    // State hooks for managing the application's data and UI
    const [history, setHistory] = useState([]);
    const [prompt, setPrompt] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [mode, setMode] = useState('censored'); // 'censored' or 'uncensored'
    const [settings, setSettings] = useState({ tone: 'Fantasy', genre: 'Adventure' });
    const [userId, setUserId] = useState(null);
    const [isAuthReady, setIsAuthReady] = useState(false);
    const [currentStoryId, setCurrentStoryId] = useState(null);
    const [modal, setModal] = useState({ show: false, title: '', message: '', input: false, onConfirm: null });
    const [db, setDb] = useState(null);
    const [auth, setAuth] = useState(null);

    const chatContainerRef = useRef(null);

    // Use effects to set up Firebase and handle UI state
    useEffect(() => {
        // Your web app's Firebase configuration from firebase config dungeon-gpt-web.txt
        const firebaseConfig = {
          apiKey: "AIzaSyAsXHDs6vzPsVIeGqbMO_Umk9ghLDAGw",
          authDomain: "dungeon-gpt.firebaseapp.com",
          projectId: "dungeon-gpt",
          storageBucket: "dungeon-gpt.firebasestorage.app",
          messagingSenderId: "860852884563",
          appId: "1:860852884563:web:fa4691c0d2604e9a2522a6",
          measurementId: "G-KZ1GDHFEE7"
        };
        const app = initializeApp(firebaseConfig);
        const firebaseAuth = getAuth(app);
        const firestoreDb = getFirestore(app);

        const unsubscribe = onAuthStateChanged(firebaseAuth, async (user) => {
            if (user) {
                setUserId(user.uid);
            } else {
                console.log("No user signed in. Attempting anonymous sign-in.");
                try {
                    await signInAnonymously(firebaseAuth);
                } catch (error) {
                    console.error("Error during anonymous sign-in:", error);
                }
            }
            setIsAuthReady(true);
        });

        setDb(firestoreDb);
        setAuth(firebaseAuth);

        return () => unsubscribe();
    }, []);

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [history]);

    // Handle user input to send a message to the backend
    const handleSendMessage = async () => {
        if (!prompt.trim() || isLoading) return;

        setIsLoading(true);

        const newUserMessage = {
            role: 'user',
            text: prompt
        };

        const newHistory = [...history, newUserMessage];
        setHistory(newHistory);
        setPrompt('');

        const conversationForApi = newHistory.map(msg => ({
            role: msg.role === 'user' ? 'user' : 'model',
            parts: [{ text: msg.text }]
        }));

        try {
            const isLocalDev = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost';
            const baseUrl = isLocalDev ? 'http://127.0.0.1:5000' : 'https://dungeon-gpt-heroku-6eb1a27523a3.herokuapp.com';

            const response = await fetch(`${baseUrl}/api/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    history: conversationForApi,
                    mode,
                    settings,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                const newAiMessage = { role: 'model', text: data.response };
                setHistory(prevHistory => [...prevHistory, newAiMessage]);
            } else {
                console.error("API error:", data.error);
                setModal({ show: true, title: 'API Error', message: data.error });
                setHistory(prevHistory => [...prevHistory, { role: 'model', text: `Error: ${data.error}` }]);
            }
        } catch (error) {
            console.error("Fetch error:", error);
            setModal({ show: true, title: 'Network Error', message: 'Failed to connect to the backend. Please check the server.' });
            setHistory(prevHistory => [...prevHistory, { role: 'model', text: 'Error: Failed to get a response. Network or server issue.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    // Firebase Functions
    const saveStoryToFirestore = async () => {
        if (!isAuthReady || !userId) {
            setModal({ show: true, title: 'Authentication Error', message: 'User not authenticated. Please try again.' });
            return;
        }
        if (history.length === 0) {
            setModal({ show: true, title: 'Empty Story', message: 'There is no story to save.' });
            return;
        }

        setIsLoading(true);
        try {
            // Note: The `__app_id` global variable is not available in local environments.
            // A static ID is used here for local development. You can replace this with
            // a different static ID or a dynamic one if your setup changes.
            const appId = 'dungeon-gpt-web';
            const storiesRef = collection(db, `artifacts/${appId}/users/${userId}/stories`);

            const newDocRef = await addDoc(storiesRef, {
                history: history,
                settings: settings,
                mode: mode,
                createdAt: new Date(),
                updatedAt: new Date()
            });
            setCurrentStoryId(newDocRef.id);
            setModal({ show: true, title: 'Story Saved', message: `Story saved with ID: ${newDocRef.id}` });
        } catch (error) {
            console.error("Error saving story to Firestore:", error);
            setModal({ show: true, title: 'Save Error', message: `Failed to save story: ${error.message}` });
        } finally {
            setIsLoading(false);
        }
    };

    const loadStoryFromFirestore = () => {
        setModal({
            show: true,
            title: 'Load Story',
            message: 'Enter the Story ID to load:',
            input: true,
            onConfirm: async (storyId) => {
                if (!storyId) {
                    setModal({ show: false });
                    return;
                }

                if (!isAuthReady || !userId) {
                    setModal({ show: true, title: 'Authentication Error', message: 'User not authenticated. Please try again.' });
                    return;
                }

                setIsLoading(true);
                setModal({ show: false }); // Hide the input modal
                try {
                    const appId = 'dungeon-gpt-web';
                    const storyRef = doc(db, `artifacts/${appId}/users/${userId}/stories`, storyId);

                    const storySnap = await getDoc(storyRef);

                    if (storySnap.exists()) {
                        const loadedStory = storySnap.data();
                        setHistory(loadedStory.history);
                        setSettings(loadedStory.settings);
                        setMode(loadedStory.mode);
                        setCurrentStoryId(storySnap.id);
                        setModal({ show: true, title: 'Story Loaded', message: `Story "${storyId}" loaded successfully.` });
                    } else {
                        setModal({ show: true, title: 'Not Found', message: `No story found with ID: ${storyId}` });
                    }
                } catch (error) {
                    console.error("Error loading story from Firestore:", error);
                    setModal({ show: true, title: 'Load Error', message: `Failed to load story: ${error.message}` });
                } finally {
                    setIsLoading(false);
                }
            }
        });
    };

    const newStory = () => {
        setHistory([]);
        setCurrentStoryId(null);
        setSettings({ tone: 'Fantasy', genre: 'Adventure' });
        setMode('censored');
        setModal({ show: true, title: 'New Story', message: 'Starting a new story.' });
    };

    // File I/O Functions
    const exportStory = () => {
        const storyData = { history, settings, mode };
        const dataStr = JSON.stringify(storyData, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `dungeon_gpt_story_${Date.now()}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    const importStory = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const loadedData = JSON.parse(e.target.result);
                setHistory(loadedData.history || []);
                setSettings(loadedData.settings || { tone: 'Fantasy', genre: 'Adventure' });
                setMode(loadedData.mode || 'censored');
                setModal({ show: true, title: 'Story Imported', message: 'Story successfully imported from file.' });
            } catch (error) {
                console.error("Error parsing file:", error);
                setModal({ show: true, title: 'Import Error', message: 'Failed to import file. Please ensure it is a valid JSON.' });
            }
        };
        reader.readAsText(file);
    };

    // Main render function
    return (
        <div className="flex flex-col h-screen w-full max-w-4xl mx-auto p-4 bg-gray-900 text-gray-200 antialiased">
            {modal.show && <Modal title={modal.title} message={modal.message} onClose={() => setModal({ show: false })} input={modal.input} onConfirm={modal.onConfirm} />}
            
            <header className="flex-shrink-0 flex justify-between items-center py-4 border-b border-gray-800 mb-4">
                <h1 className="text-3xl font-bold">Dungeon GPT</h1>
                <div className="flex items-center space-x-2">
                    <button
                        onClick={newStory}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                        disabled={isLoading}
                    >
                        New Story
                    </button>
                    <button
                        onClick={saveStoryToFirestore}
                        className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
                        disabled={isLoading || !isAuthReady || history.length === 0}
                    >
                        Save
                    </button>
                    <button
                        onClick={loadStoryFromFirestore}
                        className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors disabled:opacity-50"
                        disabled={isLoading || !isAuthReady}
                    >
                        Load
                    </button>
                    <button
                        onClick={exportStory}
                        className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors disabled:opacity-50"
                        disabled={isLoading || history.length === 0}
                    >
                        Export
                    </button>
                    <label className="cursor-pointer px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors disabled:opacity-50" disabled={isLoading}>
                        Import
                        <input type="file" accept=".json" className="hidden" onChange={importStory} />
                    </label>
                </div>
            </header>

            <main className="flex-grow overflow-y-auto px-4 py-2 space-y-4 mb-20" ref={chatContainerRef}>
                <SettingsPanel
                    mode={mode}
                    onModeChange={setMode}
                    settings={settings}
                    onSettingsChange={setSettings}
                />
                {history.length > 0 ? (
                    history.map((msg, index) => (
                        <ChatMessage key={index} message={{ role: msg.role, text: msg.text }} />
                    ))
                ) : (
                    <div className="text-center text-gray-500 mt-16">
                        <p>Begin your adventure by typing a prompt below!</p>
                    </div>
                )}
                {isLoading && <LoadingIndicator />}
            </main>

            <InputForm
                prompt={prompt}
                onPromptChange={setPrompt}
                onSendMessage={handleSendMessage}
                isLoading={isLoading}
            />
        </div>
    );
};

// Mount the App component to the DOM
ReactDOM.render(<App />, document.getElementById('root'));

