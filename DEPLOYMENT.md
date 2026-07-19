# Guide de Déploiement Complet : Connect Jeunes (VPS, Docker, Nginx, CI/CD)

Ce guide détaille les étapes nécessaires pour déployer l'application **Connect Jeunes** sur un VPS Linux (Ubuntu/Debian) en utilisant Docker, Nginx comme reverse proxy avec SSL (Certbot), et GitHub Actions pour le déploiement continu (CI/CD). 

La configuration s'inspire directement de l'architecture mise en œuvre dans le projet `etalents-urhc`.

---

## 🏗️ Architecture Globale

```mermaid
graph TD
    User([Utilisateur]) -->|HTTPS: Port 443| Nginx[Serveur Nginx Host]
    Nginx -->|Reverse Proxy: Port 8032| WebContainer[Conteneur Docker Web: Gunicorn]
    WebContainer -->|Shared Network| DBContainer[(Conteneur Central MySQL / SQLite)]
    GitHub[GitHub Actions] -->|SSH: Pull & Build| VPS[VPS Host]
```

---

## 📦 1. Fichiers de Configuration du Projet

Les fichiers suivants sont créés à la racine du projet :
- `Dockerfile` : Pour empaqueter l'application Django.
- `docker-compose.yml` : Pour orchestrer les services.
- `nginx.conf` : Modèle de configuration pour le Nginx de l'hôte VPS.
- `.github/workflows/deploy.yml` : Pour l'automatisation GitHub Actions.

---

## 🛠️ 2. Configuration Initiale du VPS (Hôte Linux)

Connectez-vous à votre VPS en SSH et suivez ces instructions :

### Étape A. Mettre à jour le système et installer Docker
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git nginx certbot python3-certbot-nginx

# Installer Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Étape B. Créer le réseau Docker partagé
Comme spécifié dans le fichier `docker-compose.yml`, le conteneur web doit se connecter à un réseau de base de données partagé préexistant :
```bash
docker network create shared_db_network
```

### Étape C. Configurer les répertoires et les droits
Créez le répertoire de l'application et donnez les permissions appropriées à Nginx pour qu'il puisse lire les fichiers statiques et médias :
```bash
sudo mkdir -p /var/www/customer/connect-jeunes
sudo chown -R $USER:www-data /var/www/customer/connect-jeunes
sudo chmod -R 775 /var/www/customer/connect-jeunes
```

### Étape D. Cloner le dépôt et initialiser le fichier `.env`
Clonez votre dépôt de code dans le répertoire créé :
```bash
git clone <URL_DE_VOTRE_DEPOT_GITHUB> /var/www/customer/connect-jeunes
cd /var/www/customer/connect-jeunes

# Créer le fichier d'environnement .env
cp .env.example .env
nano .env
```
> [!IMPORTANT]
> Remplissez les variables secrètes comme `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS` et les accès de base de données dans `/var/www/customer/connect-jeunes/.env`.

---

## 🌐 3. Configuration de Nginx et SSL (HTTPS)

### Étape A. Activer le site Nginx
1. Créez le fichier de configuration Nginx sur votre VPS :
   ```bash
   sudo nano /etc/nginx/sites-available/connect-jeunes
   ```
2. Collez-y le contenu du fichier `nginx.conf` de la racine du projet.
3. Activez le site et redémarrez Nginx :
   ```bash
   sudo ln -s /etc/nginx/sites-available/connect-jeunes /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Étape B. Générer le certificat SSL avec Certbot
Générez un certificat HTTPS gratuit signé par Let's Encrypt :
```bash
sudo certbot --nginx -d connect-jeunes.org -d www.connect-jeunes.org
```
*Choisissez l'option de redirection automatique de tout le trafic HTTP vers HTTPS.*

---

## 🔐 4. Configuration des Secrets GitHub

Configurez les secrets suivants dans l'onglet **Settings > Secrets and variables > Actions** de votre dépôt GitHub :

| Nom du Secret | Description | Exemple |
| :--- | :--- | :--- |
| `VPS_HOST` | L'adresse IP publique de votre VPS | `192.168.1.100` |
| `VPS_USER` | L'utilisateur SSH pour se connecter | `ubuntu` |
| `SSH_PRIVATE_KEY` | La clé privée SSH associée à la clé publique enregistrée sur le VPS | `-----BEGIN OPENSSH PRIVATE KEY----- ...` |

---

## 🚀 5. Lancer le Premier Déploiement

Une fois la configuration terminée, vous pouvez pousser votre code vers la branche `main` de GitHub. Le pipeline s'activera automatiquement.
