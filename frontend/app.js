const { useState, useEffect, createElement: e } = React;

const API_URL = "http://localhost:8000";

// --- Components ---

const ProblemCard = ({ problem }) => {
    const keywords = Array.isArray(problem.keywords) ? problem.keywords : (problem.keywords || '').split(',').map(k => k.trim());

    return e('div', { className: 'problem-card' },
        e('p', { className: 'summary' }, problem.summary),
        e('div', { className: 'keywords' },
            ...keywords.map(kw => e('span', { key: kw, className: 'keyword' }, kw))
        ),
        e('div', { className: 'meta-info' },
            e('span', { className: 'author-info' },
                problem.source === 'Reddit' ? `r/${problem.subreddit || 'subreddit'} · u/${problem.author_username}` : 'User Submission'
            ),
            e('span', { className: 'score-badge' }, `${problem.score} Karma`)
        )
    );
};

const EntrepreneurCard = ({ entrepreneur }) => {
    const expertiseTags = Array.isArray(entrepreneur.expertise) ? entrepreneur.expertise : (entrepreneur.expertise || '').split(',').map(exp => exp.trim());

    return e('div', { className: 'entrepreneur-card' },
        e('h2', null, entrepreneur.name),
        e('div', { className: 'organization' }, entrepreneur.organization),
        e('p', { className: 'description' }, entrepreneur.description),
        e('div', { className: 'expertise' },
            ...expertiseTags.map(tag => e('span', { key: tag, className: 'expertise-tag' }, tag))
        ),
        e('button', { className: 'contact-button', onClick: () => alert(`Contact information has been requested.`) }, 'Contact')
    );
};

const FilterBar = ({ setSourceFilter, setCategoryFilter }) => {
    const categories = ["Traffic", "Environment", "Education", "Healthcare", "Governance", "Technology", "Other"];

    return e('div', { className: 'filter-bar' },
        e('select', { onChange: e => setSourceFilter(e.target.value) },
            e('option', { value: '' }, 'All Sources'),
            e('option', { value: 'Reddit' }, 'Reddit'),
            e('option', { value: 'User' }, 'User')
        ),
        e('select', { onChange: e => setCategoryFilter(e.target.value) },
            e('option', { value: '' }, 'All Categories'),
            ...categories.map(cat => e('option', { key: cat, value: cat }, cat))
        )
    );
};


// --- Main App ---

const App = () => {
    const [currentPage, setCurrentPage] = useState('problems');
    const [problems, setProblems] = useState([]);
    const [entrepreneurs, setEntrepreneurs] = useState([]);
    const [error, setError] = useState(null);
    const [sourceFilter, setSourceFilter] = useState('');
    const [categoryFilter, setCategoryFilter] = useState('');

    useEffect(() => {
        const fetchProblems = async () => {
            const params = new URLSearchParams();
            if (sourceFilter) params.append('source', sourceFilter);
            if (categoryFilter) params.append('category', categoryFilter);

            try {
                const res = await fetch(`${API_URL}/getProblems?${params.toString()}`);
                if (!res.ok) throw new Error('Failed to fetch problems');
                const data = await res.json();
                setProblems(data);
            } catch (err) {
                setError(err.message);
                console.error("Error fetching problems:", err);
            }
        };

        const fetchEntrepreneurs = async () => {
            try {
                const res = await fetch(`${API_URL}/getEntrepreneurs`);
                if (!res.ok) throw new Error('Failed to fetch entrepreneurs');
                const data = await res.json();
                setEntrepreneurs(data);
            } catch (err) {
                setError(err.message);
                console.error("Error fetching entrepreneurs:", err);
            }
        };

        if (currentPage === 'problems') {
            fetchProblems();
        } else {
            fetchEntrepreneurs();
        }
    }, [currentPage, sourceFilter, categoryFilter]);

    const handleExport = () => {
        window.open(`${API_URL}/exportProblems`, '_blank');
    };

    const problemPage = e('div', null,
        e(FilterBar, { setSourceFilter, setCategoryFilter }),
        e('div', { className: 'problems-feed' },
            ...problems.map(p => e(ProblemCard, { key: p.id, problem: p }))
        )
    );

    const entrepreneurPage = e('div', null,
        e('div', { className: 'entrepreneurs-directory' },
            ...entrepreneurs.map(e_item => e(EntrepreneurCard, { key: e_item.id, entrepreneur: e_item }))
        )
    );

    return e('div', { className: 'app-container' },
        e('header', { className: 'app-header' },
            e('h1', null, 'Collective Problems'),
            e('nav', { className: 'nav-bar' },
                e('button', { onClick: () => setCurrentPage('problems'), className: currentPage === 'problems' ? 'active' : '' }, 'Problems'),
                e('button', { onClick: () => setCurrentPage('entrepreneurs'), className: currentPage === 'entrepreneurs' ? 'active' : '' }, 'Entrepreneurs'),
                e('button', { onClick: handleExport, className: 'export-button' }, 'Export JSON')
            )
        ),
        e('main', { className: 'container' },
            error && e('div', { style: { color: 'red' } }, `Error: ${error}. Is the backend server running?`),
            currentPage === 'problems' ? problemPage : entrepreneurPage
        )
    );
};

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(e(App));
