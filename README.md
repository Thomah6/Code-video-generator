# 🎬 AI Video Generator

Système automatisé de génération de vidéos TikTok/Shorts montrant du code Python qui s'écrit et son résultat visuel.

## ✨ Fonctionnalités

- 🤖 **Génération IA** : Utilise Groq (Llama 3.3) pour créer du code Python créatif
- 🎨 **Animations variées** : Fractales, jeux, data viz, art génératif, simulations
- 📹 **Effet Typing** : Code qui s'écrit caractère par caractère
- 🎵 **Musique automatique** : Intégration Pixabay pour musiques libres
- 🔒 **Validation sécurisée** : Vérification syntaxique et sécurité du code
- 🎯 **Format TikTok** : Vidéos 9:16 optimisées

## 🛠️ Stack Technique

**Backend:**
- FastAPI (Python)
- Groq API (LLM)
- MoviePy (montage vidéo)
- FFmpeg (encodage)
- Pillow (génération frames)

**Frontend:**
- React + Vite
- Tailwind CSS
- Design moderne et responsive

## 🚀 Installation

### Prérequis

- Python 3.11+
- Node.js 18+
- FFmpeg installé
- Clé API Groq (gratuite sur groq.com)

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Éditer .env et ajouter votre GROQ_API_KEY
```

### Frontend

```bash
cd frontend
npm install
```

## ▶️ Lancement

### Backend
```bash
cd backend
uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`

### Frontend
```bash
cd frontend
npm run dev
```

L'interface sera disponible sur `http://localhost:5173`

## 📖 Utilisation

1. Ouvrir l'interface web
2. Choisir le type d'animation (ou "Surprise-moi!")
3. Ajuster la durée (15-60s)
4. Sélectionner le style musical
5. Cliquer sur "Générer la vidéo"
6. Attendre la génération (30s-2min selon complexité)
7. Télécharger et poster sur TikTok! 🎉

## 🎯 Roadmap

- [ ] Système de queue avec Celery + Redis
- [ ] WebSocket pour suivi temps réel
- [ ] Enregistrement de l'exécution du code (Xvfb)
- [ ] Montage final avec MoviePy
- [ ] Galerie de vidéos générées
- [ ] Export direct vers TikTok/Instagram
- [ ] Templates de code personnalisables

## 📝 License

MIT

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésite pas à ouvrir une issue ou PR.

---

**Fait avec ❤️ pour créer du contenu viral**
