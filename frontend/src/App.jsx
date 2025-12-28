import { useState } from 'react'

function App() {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)
    const [config, setConfig] = useState({
        animation_type: 'surprise',
        duration: 30,
        music_style: 'electro'
    })

    const generateVideo = async () => {
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Erreur lors de la génération')
            }

            const data = await response.json()
            setResult(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-2xl w-full">
                <h1 className="text-4xl font-bold text-center mb-2 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                    🎬 AI Video Generator
                </h1>
                <p className="text-center text-gray-600 mb-8">
                    Génère des vidéos TikTok avec du code Python animé
                </p>

                <div className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Type d'animation
                        </label>
                        <select
                            value={config.animation_type}
                            onChange={(e) => setConfig({ ...config, animation_type: e.target.value })}
                            className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-purple-500 focus:outline-none transition"
                        >
                            <option value="surprise">🎲 Surprise-moi!</option>
                            <option value="fractal">🌀 Fractale</option>
                            <option value="game">🎮 Jeu</option>
                            <option value="dataviz">📊 Data Viz</option>
                            <option value="art">🎨 Art Génératif</option>
                            <option value="simulation">⚡ Simulation</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Durée: {config.duration}s
                        </label>
                        <input
                            type="range"
                            min="15"
                            max="60"
                            value={config.duration}
                            onChange={(e) => setConfig({ ...config, duration: parseInt(e.target.value) })}
                            className="w-full"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Style musical
                        </label>
                        <div className="grid grid-cols-4 gap-2">
                            {['electro', 'lofi', 'epic', 'chill'].map((style) => (
                                <button
                                    key={style}
                                    onClick={() => setConfig({ ...config, music_style: style })}
                                    className={`px-4 py-2 rounded-lg font-medium transition ${config.music_style === style
                                        ? 'bg-purple-600 text-white'
                                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                        }`}
                                >
                                    {style}
                                </button>
                            ))}
                        </div>
                    </div>

                    <button
                        onClick={generateVideo}
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-4 px-6 rounded-xl hover:shadow-lg transform hover:scale-105 transition disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                    >
                        {loading ? '⏳ Génération en cours...' : '✨ Générer la vidéo'}
                    </button>

                    {error && (
                        <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
                            <p className="text-red-800 font-medium">❌ {error}</p>
                        </div>
                    )}

                    {result && (
                        <div className="bg-green-50 border-2 border-green-200 rounded-xl p-4 space-y-4">
                            <p className="text-green-800 font-medium">✅ {result.message}</p>
                            <p className="text-sm text-green-600">Job ID: {result.job_id}</p>

                            {result.video_url && (
                                <div className="space-y-3">
                                    <video
                                        src={result.video_url}
                                        controls
                                        className="w-full rounded-lg shadow-lg"
                                    />
                                    <a
                                        href={result.video_url}
                                        download={`video_${result.job_id}.mp4`}
                                        className="block w-full bg-green-600 text-white font-bold py-3 px-6 rounded-xl hover:bg-green-700 text-center transition"
                                    >
                                        📥 Télécharger la vidéo
                                    </a>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default App
