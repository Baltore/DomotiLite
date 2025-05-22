# 🏠 DomotiLite

DomotiLite est une application locale de domotique intelligente, développée en Python.  
Elle permet de contrôler des appareils simulés, recevoir des données de capteurs, et déclencher automatiquement des actions selon des règles personnalisées.

---

## 🎯 Objectifs

- Simuler un système domotique connecté
- Mettre en œuvre une communication entre deux logiciels (client ↔ capteurs)
- Gérer des capteurs (température, luminosité) et des appareils (chauffage, volets, lumière, etc.)
- Démontrer des compétences en :
  - Programmation orientée objet
  - Base de données SQLite
  - Sockets TCP
  - Interface graphique (Tkinter)
  - Logique métier automatisée

---

## ⚙️ Architecture

- **DomotiLite UI** : reçoit les données, gère les appareils, déclenche les actions
- **Sensor Simulator** : envoie régulièrement des données capteurs et s’adapte selon l’état des appareils

---

## 🧠 Automatisme intégré

### Logique basée sur les capteurs + l'heure :

- 🌡️ La climatisation et le chauffage pour la Température
- ☀️/🌙 Les volets et la lumière en fonction de la Luminosité et du cycle

---

## 🖥️ Interface

- Design épuré 
- interface personnalisé
- Affichage temps réel des capteurs
- Gestion CRUD des appareils via une fenêtre dédiée

---

## 📦 Technologies utilisées

- Python
- Tkinter (GUI)
- SQLite3 (Base de données locale)
- Sockets TCP (communication capteur  app)
- Fichier schema.sql pour initialisation de la BDD

---

## ✅ Fonctionnalités clés

- ✔️ Communication machine ↔ machine via sockets TCP
- ✔️ Base SQLite avec minimum 3 tables
- ✔️ Interface graphique moderne
- ✔️ Capteurs et logique IOT simulés
- ✔️ Déclenchement d’actions automatisées
- ✔️ Cycle jour/nuit intégré
- ✔️ Bonus personnalisation + design

---

## 🚀 Lancement

1. Clone le dépôt :
```bash
   git clone https://github.com/ton_profil/DomotiLite.git
   cd DomotiLite
```
2. Lance l’interface :
```bash
   python client_gui/main.py
```
3. Dans un second terminal, lance le simulateur :
```bash
   python sensor_simulator/simulator.py
```

- N'oublie pas d'installer les dépendances

---

## 🎓 Auteur

- Projet réalisé dans le cadre de ma B2 Informatique — UF Développement logiciel & BDD, par Qays et Matthis à partir d’un sujet libre
