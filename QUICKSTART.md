# 🚀 Guide de Démarrage Rapide

## Étape 1 : Obtenir une clé API Groq (GRATUIT)

1. Va sur https://console.groq.com
2. Crée un compte (gratuit)
3. Va dans "API Keys"
4. Clique "Create API Key"
5. Copie la clé (commence par `gsk_...`)

## Étape 2 : Configuration Backend

```bash
cd backend

# Créer le fichier .env
copy .env.example .env

# Éditer .env et remplacer:
# GROQ_API_KEY=your_groq_api_key_here
# par ta vraie clé API
```

## Étape 3 : Installer les dépendances Python

```bash
# Toujours dans backend/
pip install -r requirements.txt
```

**Note:** Si tu as des erreurs avec `moviepy`, installe FFmpeg :
- Windows : `choco install ffmpeg` (avec Chocolatey)
- Ou télécharge depuis https://ffmpeg.org/download.html

## Étape 4 : Démarrer le Backend

```bash
# Dans backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Tu devrais voir :
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ Backend prêt ! Teste : http://localhost:8000 (tu devrais voir un message JSON)

## Étape 5 : Configuration Frontend

Ouvre un **nouveau terminal** :

```bash
cd frontend

# Installer les dépendances
npm install
```

## Étape 6 : Démarrer le Frontend

```bash
# Toujours dans frontend/
npm run dev
```

Tu devrais voir :
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ Frontend prêt ! Ouvre http://localhost:5173

## Étape 7 : Tester la Génération

1. Ouvre http://localhost:5173 dans ton navigateur
2. Choisis "Fractale" (ou "Surprise-moi!")
3. Durée : 30 secondes
4. Style : Electro
5. Clique "Générer la vidéo"

**Résultat attendu :**
- Message de succès avec un Job ID
- Le code Python généré est validé
- Les frames du typing effect sont créées

## 🐛 Dépannage

### Erreur : "GROQ_API_KEY not found"
→ Vérifie que tu as bien créé le fichier `.env` dans `backend/` avec ta clé API

### Erreur : "Module not found"
→ Assure-toi d'avoir installé les dépendances :
```bash
cd backend
pip install -r requirements.txt
```

### Erreur : "FFmpeg not found"
→ Installe FFmpeg sur ton système

### Port 8000 déjà utilisé
→ Change le port dans la commande uvicorn :
```bash
uvicorn app.main:app --reload --port 8001
```
Et modifie aussi `frontend/vite.config.js` ligne 8 : `target: 'http://localhost:8001'`

## 📝 Commandes Utiles

**Backend :**
```bash
# Démarrer
cd backend
uvicorn app.main:app --reload

# Voir les logs en temps réel
# (les logs s'affichent automatiquement dans le terminal)
```

**Frontend :**
```bash
# Démarrer
cd frontend
npm run dev

# Build pour production
npm run build
```

## 🎯 Prochaines Étapes

Une fois que tout fonctionne :
1. Teste différents types d'animations
2. Vérifie que le code généré est valide
3. On pourra ensuite implémenter :
   - L'enregistrement de l'exécution du code
   - Le montage vidéo complet
   - Le téléchargement des vidéos

---

**Besoin d'aide ?** Partage-moi les messages d'erreur si tu en as !
