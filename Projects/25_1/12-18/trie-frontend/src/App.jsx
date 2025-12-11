import { useState } from 'react';

const API_BASE = 'http://192.168.1.213:8080/api';

function App() {
    const [isInited, setIsInited] = useState(false);
    const [initInfo, setInitInfo] = useState(null);
    const [loadingInit, setLoadingInit] = useState(false);

    const [query, setQuery] = useState('');
    const [k, setK] = useState(10);
    const [searchResults, setSearchResults] = useState([]);
    const [searchLoading, setSearchLoading] = useState(false);

    const [clusters, setClusters] = useState([]);
    const [clusterLoading, setClusterLoading] = useState(false);
    const [selectedCluster, setSelectedCluster] = useState(null);
    const [clusterItems, setClusterItems] = useState([]);

    const [error, setError] = useState(null);

    async function handleInit() {
        setError(null);
        setLoadingInit(true);
        setClusterItems([]);
        setSelectedCluster(null);

        try {
            const res = await fetch(`${API_BASE}/load-from-resources`, {
                method: 'POST',
            });
            if (!res.ok) throw new Error('Failed to init data');
            const info = await res.json();
            setInitInfo(info);
            setIsInited(true);

            await loadClusters();
        } catch (e) {
            console.error(e);
            setError(e.message || 'Init error');
        } finally {
            setLoadingInit(false);
        }
    }

    async function loadClusters() {
        setClusterLoading(true);
        setError(null);
        setClusters([]);
        setClusterItems([]);
        setSelectedCluster(null);

        try {
            const res = await fetch(`${API_BASE}/clusters`);
            if (!res.ok) throw new Error('Failed to load clusters');
            const data = await res.json();
            setClusters(data.clusterIds || []);
        } catch (e) {
            console.error(e);
            setError(e.message || 'Cluster load error');
        } finally {
            setClusterLoading(false);
        }
    }

    async function handleSearch(e) {
        e.preventDefault();
        if (!query.trim()) {
            setSearchResults([]);
            return;
        }
        if (!isInited) {
            setError('Сначала нажми "Load data"');
            return;
        }

        setError(null);
        setSearchLoading(true);
        setSearchResults([]);

        try {
            const params = new URLSearchParams({
                q: query,
                k: String(k),
            });
            const res = await fetch(`${API_BASE}/search/semantic?` + params.toString());
            if (!res.ok) throw new Error('Search request failed');
            const data = await res.json();
            setSearchResults(data);
        } catch (e) {
            console.error(e);
            setError(e.message || 'Search error');
        } finally {
            setSearchLoading(false);
        }
    }

    async function handleSelectCluster(clusterId) {
        if (!isInited) {
            setError('Сначала нажми "Load data"');
            return;
        }

        setError(null);
        setSelectedCluster(clusterId);
        setClusterItems([]);
        setClusterLoading(true);

        try {
            const params = new URLSearchParams({
                id: String(clusterId),
                k: String(k),
            });
            const res = await fetch(`${API_BASE}/search/by-cluster?` + params.toString());
            if (!res.ok) throw new Error('Failed to load cluster items');
            const data = await res.json();
            setClusterItems(data);
        } catch (e) {
            console.error(e);
            setError(e.message || 'Cluster items error');
        } finally {
            setClusterLoading(false);
        }
    }

    return (
        <div className="app">
            <header className="app-header">
                <h1>Vector Search Demo</h1>
                <button onClick={handleInit} disabled={loadingInit} className="init-button">
                    {loadingInit ? 'Loading...' : 'Load data (data.json)'}
                </button>
                {initInfo && (
                    <span className="init-info">
            Items: {initInfo.items}, kClusters: {initInfo.kClusters}
          </span>
                )}
            </header>

            {error && <div className="error-box">Error: {error}</div>}

            <div className="main-grid">
                {/* Левая панель: Semantic Search */}
                <section className="column">
                    <h2>Semantic search</h2>
                    <form onSubmit={handleSearch} className="search-form">
                        <input
                            type="text"
                            placeholder="Type your query..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            className="search-input"
                        />
                        <select
                            value={k}
                            onChange={(e) => setK(Number(e.target.value))}
                            className="search-select"
                        >
                            <option value={5}>Top-5</option>
                            <option value={10}>Top-10</option>
                            <option value={20}>Top-20</option>
                            <option value={50}>Top-50</option>
                        </select>
                        <button
                            type="submit"
                            disabled={searchLoading || !isInited}
                            className="primary-button"
                        >
                            {searchLoading ? 'Searching...' : 'Search'}
                        </button>
                    </form>

                    <div className="results-box">
                        {searchResults.length === 0 && !searchLoading && (
                            <div className="placeholder">
                                No results yet. Type a query and press "Search".
                            </div>
                        )}

                        {searchResults.map((item) => (
                            <div key={item.id} className="result-item">
                                <div className="result-text">{item.text}</div>
                                <div className="result-meta">
                                    <span>ID: {item.id}</span>
                                    <span>Cluster: {item.clusterId}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Правая панель: Clusters */}
                <section className="column">
                    <h2>Clusters</h2>

                    <div className="cluster-header">
                        <span>Available clusters:</span>
                        <button
                            onClick={loadClusters}
                            disabled={clusterLoading || !isInited}
                            className="small-button"
                        >
                            {clusterLoading ? 'Refreshing...' : 'Reload'}
                        </button>
                    </div>

                    <div className="cluster-list">
                        {clusters.length === 0 && isInited && !clusterLoading && (
                            <div className="placeholder">No clusters loaded yet.</div>
                        )}
                        {!isInited && (
                            <div className="placeholder">Press "Load data" first.</div>
                        )}

                        {clusters.map((cid) => (
                            <button
                                key={cid}
                                onClick={() => handleSelectCluster(cid)}
                                className={
                                    'cluster-button' + (selectedCluster === cid ? ' active' : '')
                                }
                            >
                                Cluster {cid}
                            </button>
                        ))}
                    </div>

                    <div className="results-box">
                        <h3 className="cluster-title">
                            Cluster items {selectedCluster !== null ? `(cluster ${selectedCluster})` : ''}
                        </h3>
                        {clusterItems.length === 0 &&
                            selectedCluster !== null &&
                            !clusterLoading && (
                                <div className="placeholder">
                                    No items in this cluster (or not loaded yet).
                                </div>
                            )}

                        {clusterItems.map((item) => (
                            <div key={item.id} className="result-item">
                                <div className="result-text">{item.text}</div>
                                <div className="result-meta">
                                    <span>ID: {item.id}</span>
                                    <span>Cluster: {item.clusterId}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            </div>
        </div>
    );
}

export default App;
