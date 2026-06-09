<<<<<<< HEAD
# 🚇 KONEKT — Métro d'Abidjan

Plateforme web de réservation de billets pour le réseau de métro d'Abidjan (Ligne 1 : Anyama ↔ Aéroport FHB Port-Bouët). Développée avec Django, elle permet aux voyageurs d'acheter des tickets en ligne avec génération de QR code, et offre un tableau de bord de supervision pour les agents.

\---

## ✨ Fonctionnalités

### Côté Voyageur

* **Recherche de trajets** : sélection de la gare de départ et d'arrivée, affichage des prochains départs disponibles
* **Calcul tarifaire dynamique** : le prix est calculé selon le nombre de zones traversées (200 à 800 FCFA)
* **Calcul d'heure de passage** : l'heure affichée correspond à l'heure de passage réelle à la gare choisie (décalage de 3 min par escale)
* **Réservation en ligne** : formulaire passager avec choix du mode de paiement (Orange Money, MTN MoMo, Wave)
* **Ticket numérique** : billet PDF imprimable avec QR code unique généré à la réservation
* **Historique des voyages** : espace personnel listant tous les tickets achetés
* **Carte interactive Leaflet** : visualisation du tracé de la Ligne 1 avec le segment du trajet mis en surbrillance

### Côté Agent / Administration

* **Dashboard de supervision** : nombre total de billets émis, revenu global, activité récente
* **Graphique 7 jours** : volume de réservations sur la dernière semaine
* **Recherche de ticket** : vérification d'un billet par son code
* **Scan QR Code** : validation ou invalidation d'un billet à l'embarquement via l'URL de scan

\---

## 🗂️ Structure du projet

```
Metro\_Abidjan/
├── konekt\_project/          # Configuration Django
=======
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
>>>>>>> 69aad4dcb4d0866d0139f4bb6910a5af8bf2e246
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
<<<<<<< HEAD
├── transport/               # Application principale
│   ├── models.py            # Commune, Gare, Voyage, Reservation
│   ├── views.py             # Toutes les vues
│   ├── urls.py              # Routes de l'application
│   ├── admin.py             # Interface d'administration
│   ├── migrations/          # Migrations de base de données
│   └── templates/
│       └── transport/
│           ├── home.html          # Page d'accueil + recherche
│           ├── resultats.html     # Résultats de recherche
│           ├── form\_passager.html # Formulaire de réservation
│           ├── ticket.html        # Billet numérique
│           ├── mes\_tickets.html   # Historique voyageur
│           ├── agent\_dashboard.html # Dashboard agent
│           ├── scan\_result.html   # Résultat de scan QR
│           ├── login.html
│           └── inscription.html
├── static/
│   └── images/              # Images statiques du site
├── media/
│   └── qr\_codes/            # QR codes générés
├── db.sqlite3               # Base de données SQLite
└── manage.py
```

\---

## ⚙️ Installation

### Prérequis

* Python 3.10+
* pip

### 1\. Cloner / extraire le projet

```bash
cd Metro\_Abidjan
```

### 2\. Créer un environnement virtuel

```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# macOS / Linux
source venv/bin/activate
```

### 3\. Installer les dépendances

```bash
pip install django qrcode\[pil] Pillow
```

### 4\. Appliquer les migrations

```bash
python manage.py migrate
```

### 5\. Créer un superutilisateur (admin)

```bash
python manage.py createsuperuser
```

### 6\. Lancer le serveur

```bash
python manage.py runserver
```

Le site est accessible sur **http://127.0.0.1:8000/**

\---

## 🌐 Routes principales

|URL|Vue|Description|
|-|-|-|
|`/`|`accueil`|Page d'accueil et recherche de trajets|
|`/reserver/<id>/`|`reserver\_etape\_1`|Formulaire passager|
|`/valider/<id>/`|`valider\_reservation`|Confirmation et génération du ticket|
|`/ticket/<code>/`|`voir\_ticket`|Affichage d'un ticket|
|`/mes-tickets/`|`mes\_tickets`|Historique des réservations (connecté)|
|`/scan/<code>/`|`valider\_ticket\_scan`|Validation QR code par l'agent|
|`/agent-control/`|`dashboard\_agent`|Dashboard de supervision (staff)|
|`/login/`|`login\_view`|Connexion|
|`/inscription/`|`inscription\_view`|Création de compte|
|`/admin/`|Django Admin|Gestion complète des données|

\---

## 🗃️ Modèles de données

### `Commune`

Représente une commune sur la ligne (ordonnée par `position`).

|Champ|Type|Description|
|-|-|-|
|`nom`|CharField|Nom de la commune|
|`position`|PositiveIntegerField|Ordre sur la ligne (unique)|

### `Gare`

Station du réseau, rattachée à une commune.

|Champ|Type|Description|
|-|-|-|
|`nom`|CharField|Nom de la gare|
|`commune`|ForeignKey|Commune de rattachement|

### `Voyage`

Départ planifié sur la ligne.

|Champ|Type|Description|
|-|-|-|
|`sens`|CharField|`ALLER` (Anyama→Port-Bouët) ou `RETOUR`|
|`jour\_depart`|DateField|Date du départ|
|`heure\_depart`|TimeField|Heure de départ au terminus|
|`est\_ouvert`|BooleanField|Ouvert à la réservation|
|`gare\_depart\_defaut`|ForeignKey|Terminus de départ (auto-rempli)|
|`gare\_arrivee\_defaut`|ForeignKey|Terminus d'arrivée (auto-rempli)|

### `Reservation`

Ticket acheté par un passager.

|Champ|Type|Description|
|-|-|-|
|`voyage`|ForeignKey|Voyage associé|
|`nom\_passager`|CharField|Nom|
|`prenom\_passager`|CharField|Prénom|
|`gare\_depart\_nom`|CharField|Nom de la gare de départ|
|`gare\_arrivee\_nom`|CharField|Nom de la gare d'arrivée|
|`code\_ticket`|CharField|Code unique (ex: `KNEKT-AF92`)|
|`prix\_paye`|PositiveIntegerField|Montant en FCFA|
|`mode\_paiement`|CharField|Orange / MTN / Wave|
|`heure\_reelle\_passage`|TimeField|Heure de passage calculée à la gare choisie|
|`qr\_code`|ImageField|Image du QR code généré|
|`est\_valide`|BooleanField|`True` = ticket non encore utilisé|
|`date\_utilisation`|DateTimeField|Horodatage du passage en contrôle|

\---

## 🔐 Accès et rôles

|Rôle|Accès|
|-|-|
|**Visiteur**|Recherche, consultation des horaires, achat de tickets sans compte|
|**Voyageur connecté**|+ Historique des tickets (`/mes-tickets/`)|
|**Agent (is\_staff)**|+ Dashboard de supervision, validation des QR codes|
|**Superadmin**|+ Interface `/admin/` complète|

\---

## 🧮 Logique tarifaire

Le prix est calculé selon le nombre de zones (positions de communes) séparant le départ de l'arrivée :

|Zones traversées|Tarif|
|-|-|
|0 – 1|200 FCFA|
|2|300 FCFA|
|3|400 FCFA|
|4|500 FCFA|
|5|600 FCFA|
|6+|800 FCFA|

\---

## 🗺️ Ligne 1 — Stations

La Ligne 1 relie **Anyama Centre** à **l'Aéroport FHB Port-Bouët** en 18 stations sur \~37 km, traversant : Anyama, Abobo, Adjamé, le Plateau, Treichville, Marcory, Koumassi et Port-Bouët.

\---

## 🛠️ Technologies utilisées

|Technologie|Usage|
|-|-|
|**Django 6.0**|Framework web backend|
|**SQLite**|Base de données (développement)|
|**Tailwind CSS** (CDN)|Styles et mise en page|
|**Leaflet.js**|Carte interactive du tracé|
|**Chart.js**|Graphique du dashboard agent|
|**qrcode\[pil]**|Génération des QR codes|
|**Font Awesome**|Icônes|

\---

## 👥 Auteurs

Développé par **Aziz Compaoré**   
© 2026 KONEKT Métro Abidjan

=======
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
>>>>>>> 69aad4dcb4d0866d0139f4bb6910a5af8bf2e246
