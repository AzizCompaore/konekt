🚇 Konekt – Billetterie en ligne du Métro d'Abidjan
> Application web de réservation et de validation de tickets pour le réseau de transport ferroviaire d'Abidjan (ligne Anyama ↔ Port-Bouët).
Konekt est un système de billetterie numérique conçu pour le futur métro d'Abidjan. Il permet aux passagers de consulter les horaires en temps réel, de réserver un ticket en ligne depuis leur gare, et d'obtenir un QR Code unique servant de titre de transport. Les agents de contrôle disposent d'un tableau de bord dédié pour valider les tickets par scan.
---
✨ Fonctionnalités
🧑‍💼 Côté Passager
🔍 Recherche de voyage : sélection de la gare de départ et d'arrivée parmi toutes les stations de la ligne
⏱️ Heure de passage estimée : calcul dynamique de l'heure d'arrivée du métro à la gare de l'utilisateur (3 min par escale)
💰 Tarification par zones : calcul automatique du prix en FCFA selon le nombre de zones traversées
🎫 Réservation en ligne : saisie des informations passager, choix du mode de paiement
📲 Ticket numérique avec QR Code : chaque réservation génère un QR code unique couleur orange (code `KNEKT-XXXX`)
🗂️ Mes tickets : consultation de l'historique des réservations (utilisateur connecté)
👤 Authentification : inscription, connexion, déconnexion
🕵️ Côté Agent de Contrôle
📊 Tableau de bord : nombre total de tickets vendus, revenu total généré
🔍 Recherche de ticket par code
✅ Validation par scan : le scan du QR code marque le ticket comme utilisé (avec horodatage), et affiche un message vert/rouge selon l'état
📋 Historique des 10 dernières réservations
---
🗺️ Ligne desservie
La ligne couvre 8 communes d'Abidjan, du nord au sud :
```
Anyama → Abobo → Adjamé → Plateau → Treichville → Marcory → Koumassi → Port-Bouët
```
Les trains circulent dans les deux sens :
ALLER : Anyama ➔ Port-Bouët
RETOUR : Port-Bouët ➔ Anyama
---
💰 Grille tarifaire
Zones traversées	Prix (FCFA)
0 – 1	200
2	300
3	400
4	500
5	600
6+	800
---
🛠️ Stack technique
Composant	Technologie
Backend	Python 3 / Django
Base de données	SQLite (développement)
Frontend	Bootstrap 5 + Django Templates
Génération QR Code	`qrcode` + Pillow
Authentification	Django Auth intégré
Contrôle accès agent	`@staff_member_required`
---
🚀 Installation
Prérequis
Python 3.10+
pip
Étapes
```bash
# 1. Cloner le dépôt
git clone https://github.com/ton-username/metro-abidjan-konekt.git
cd Metro_Abidjan

# 2. Créer et activer l'environnement virtuel
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 3. Installer les dépendances
pip install django pillow qrcode

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un superutilisateur (admin + agent)
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```
L'application est accessible à : http://127.0.0.1:8000
> ℹ️ Le tableau de bord agent est accessible à `/agent-control/` — réservé aux membres du staff Django (`is_staff = True`).
---
📁 Structure du projet
```
Metro_Abidjan/
│
├── konekt_project/              # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── transport/                   # Application principale
│   ├── models.py                # Commune, Gare, Voyage, Reservation
│   ├── views.py                 # Vues passager, agent, auth
│   ├── urls.py                  # Routes
│   ├── admin.py                 # Interface d'administration
│   ├── migrations/              # Historique des migrations
│   └── templates/transport/
│       ├── home.html            # Page d'accueil / horaires
│       ├── resultats.html       # Résultats de recherche de voyage
│       ├── form_passager.html   # Formulaire de réservation
│       ├── ticket.html          # Ticket numérique avec QR Code
│       ├── mes_tickets.html     # Historique des tickets
│       ├── agent_dashboard.html # Tableau de bord agent
│       ├── inscription.html
│       └── login.html
│
├── media/
│   └── qr_codes/                # QR codes générés (KNEKT-XXXX.png)
│
├── static/
│   └── images/
│
└── manage.py
```
---
🗄️ Modèles de données
Modèle	Description
`Commune`	Commune d'Abidjan avec sa position sur la ligne (1 à 8)
`Gare`	Station rattachée à une commune
`Voyage`	Départ planifié (sens, date, heure, statut ouvert/fermé)
`Reservation`	Ticket réservé par un passager avec QR code, heure de passage, statut de validité
---
🔒 Gestion des accès
Fonctionnalité	Accès requis
Consulter les horaires	Public
Rechercher un voyage	Public
Réserver un ticket	Public (sans compte)
Consulter ses tickets	Connecté (`@login_required`)
Tableau de bord agent	Staff Django (`@staff_member_required`)
Valider un ticket (scan)	Staff Django
Interface d'administration	Superutilisateur
---
📲 Format du QR Code
Chaque ticket génère un QR code qui encode l'URL de validation :
```
http://127.0.0.1:8000/scan/KNEKT-XXXX/
```
Le QR code est rendu en orange (`#FF8200`) sur fond blanc, aux couleurs du projet. Lors du scan par un agent, le ticket est marqué comme utilisé avec l'heure exacte de passage.
---
