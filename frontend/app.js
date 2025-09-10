const { useState, useEffect } = React;

// --- Mock Data ---
const mockProblems = [
    {
        id: 1,
        summary: "The traffic light at the intersection of Main St and 1st Ave has a very short green light, causing long backups.",
        keywords: "traffic, infrastructure, urban planning",
        category: "Traffic",
        source: "Reddit",
        author_username: "user123",
        score: 128,
    },
    {
        id: 2,
        summary: "Local parks have a severe littering problem, and there aren't enough trash cans available.",
        keywords: "environment, community, sanitation",
        category: "Environment",
        source: "User",
        author_username: "anonymous",
        score: 45,
    },
];

const mockEntrepreneurs = [
    {
        id: 1,
        name: "Alice Johnson",
        organization: "SolveIt Innovations",
        expertise: "Healthcare, Technology",
        description: "Focused on developing tech solutions for rural healthcare access.",
        email: "contact@solveit.com"
    },
    {
        id: 2,
        name: "Bob Williams",
        organization: "GreenFuture NGO",
        expertise: "Environment, Governance",
        description: "Advocating for sustainable urban development and green policies.",
        email: "bob.w@greenfuture.org"
    }
];


// --- Components ---

const ProblemCard = ({ problem }) => {
    const keywords = problem.keywords.split(',').map(k => k.trim());
    return (
        <div className="problem-card">
            <p className="summary">{problem.summary}</p>
            <div className="keywords">
                {keywords.map(kw => <span key={kw} className="keyword">{kw}</span>)}
            </div>
            <div className="meta-info">
                <span className="author-info">
                    {problem.source === 'Reddit' ? `r/subreddit · u/${problem.author_username}` : 'User Submission'}
                </span>
                <span className="score-badge">{problem.score} Karma</span>
            </div>
        </div>
    );
};

const EntrepreneurCard = ({ entrepreneur }) => {
    const expertiseTags = entrepreneur.expertise.split(',').map(e => e.trim());
    return (
        <div className="entrepreneur-card">
            <h2>{entrepreneur.name}</h2>
            <div className="organization">{entrepreneur.organization}</div>
            <p className="description">{entrepreneur.description}</p>
            <div className="expertise">
                {expertiseTags.map(tag => <span key={tag} className="expertise-tag">{tag}</span>)}
            </div>
            <button className="contact-button" onClick={() => alert(`Contact: ${entrepreneur.email}`)}>
                Contact
            </button>
        </div>
    );
};


// --- Main App ---

const App = () => {
    const [currentPage, setCurrentPage] = useState('problems'); // 'problems' or 'entrepreneurs'
    // In a real app, this data would be fetched from the API
    const [problems, setProblems] = useState([]);
    const [entrepreneurs, setEntrepreneurs] = useState([]);

    useEffect(() => {
        // Simulating API fetch
        setProblems(mockProblems);
        setEntrepreneurs(mockEntrepreneurs);
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
