const { useState, useEffect } = React;

const API_URL = "http://localhost:8000";

// --- Components ---

const ProblemCard = ({ problem }) => {
    const keywords = Array.isArray(problem.keywords) ? problem.keywords : (problem.keywords || '').split(',').map(k => k.trim());
    return (
        <div className="problem-card">
            <p className="summary">{problem.summary}</p>
            <div className="keywords">
                {keywords.map(kw => <span key={kw} className="keyword">{kw}</span>)}
            </div>
            <div className="meta-info">
                <span className="author-info">
                    {problem.source === 'Reddit' ? `r/${problem.subreddit || 'subreddit'} · u/${problem.author_username}` : 'User Submission'}
                </span>
                <span className="score-badge">{problem.score} Karma</span>
            </div>
        </div>
    );
};

const EntrepreneurCard = ({ entrepreneur }) => {
    const expertiseTags = Array.isArray(entrepreneur.expertise) ? entrepreneur.expertise : (entrepreneur.expertise || '').split(',').map(e => e.trim());
    return (
        <div className="entrepreneur-card">
            <h2>{entrepreneur.name}</h2>
            <div className="organization">{entrepreneur.organization}</div>
            <p className="description">{entrepreneur.description}</p>
            <div className="expertise">
                {expertiseTags.map(tag => <span key={tag} className="expertise-tag">{tag}</span>)}
            </div>
            <button className="contact-button" onClick={() => alert(`Contact information has been requested.`)}>
                Contact
            </button>
        </div>
    );
};


// --- Main App ---

const App = () => {
    const [currentPage, setCurrentPage] = useState('problems'); // 'problems' or 'entrepreneurs'
    const [problems, setProblems] = useState([]);
    const [entrepreneurs, setEntrepreneurs] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const problemsRes = await fetch(`${API_URL}/getProblems`);
                if (!problemsRes.ok) throw new Error('Failed to fetch problems');
                const problemsData = await problemsRes.json();
                setProblems(problemsData);

                const entrepreneursRes = await fetch(`${API_URL}/getEntrepreneurs`);
                if (!entrepreneursRes.ok) throw new Error('Failed to fetch entrepreneurs');
                const entrepreneursData = await entrepreneursRes.json();
                setEntrepreneurs(entrepreneursData);

            } catch (err) {
                setError(err.message);
                console.error("Error fetching data:", err);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="app-container">
            <header className="app-header">
                <h1>Collective Problems</h1>
                <nav className="nav-bar">
                    <button
                        onClick={() => setCurrentPage('problems')}
                        className={currentPage === 'problems' ? 'active' : ''}
                    >
                        Problems
                    </button>
                    <button
                        onClick={() => setCurrentPage('entrepreneurs')}
                        className={currentPage === 'entrepreneurs' ? 'active' : ''}
                    >
                        Entrepreneurs
                    </button>
                </nav>
            </header>

            <main className="container">
                {error && <div style={{ color: 'red' }}>Error: {error}. Is the backend server running?</div>}

                {currentPage === 'problems' && (
                    <div className="problems-feed">
                        {problems.map(p => <ProblemCard key={p.id} problem={p} />)}
                    </div>
                )}

                {currentPage === 'entrepreneurs' && (
                    <div className="entrepreneurs-directory">
                        {entrepreneurs.map(e => <EntrepreneurCard key={e.id} entrepreneur={e} />)}
                    </div>
                )}
            </main>
        </div>
    );
};

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<App />);
