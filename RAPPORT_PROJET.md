# 📋 RAPPORT DE PROJET — Détection de Fraude sur les Transactions par Carte de Crédit

**Dépôt :** [`khalid058r/Fraude_detection_Trans`](https://github.com/khalid058r/Fraude_detection_Trans)  
**Langage principal :** Python (Jupyter Notebook + Script)  
**Date de création :** 4 février 2026  
**Dernière mise à jour :** 8 février 2026  

---

## 1. 🎯 Présentation du Projet

Ce projet est un **système complet de détection de fraude** sur les transactions par carte de crédit. Il couvre l'ensemble du cycle de vie d'un projet de Machine Learning : de l'**exploration des données** à la **mise en production** via une application web interactive.

L'objectif est de développer un modèle capable de **classifier automatiquement** les transactions comme **légitimes**, **suspectes** ou **frauduleuses**, en utilisant des algorithmes de Machine Learning supervisé.

---

## 2. 📁 Architecture du Projet

| Fichier | Rôle | Profil concerné |
|---|---|---|
| `credit_card.csv` | Données brutes des transactions | Data Engineer |
| `credit_card_processed.csv` | Données nettoyées et transformées | Data Engineer |
| `Credit_Card_Fraud.ipynb` | Notebook d'exploration et modélisation initiale | ML Engineer |
| `Credit_Card_Fraud_Improved.ipynb` | Notebook avec modèle amélioré | ML Engineer |
| `fraude_detection.ipynb` | Notebook de détection de fraude | ML Engineer |
| `projetML-amine.ipynb` | Notebook expérimental (SVM, Decision Trees, etc.) | ML Engineer |
| `best_model_fraud_detection.pkl` | Modèle ML sérialisé (pickle) | ML Engineer / Data Engineer |
| `scaler_fraud_detection.pkl` | Scaler sauvegardé pour normalisation | Data Engineer |
| `feature_importance.png` | Visualisation de l'importance des features | ML Engineer |
| `app.py` | Application Streamlit de déploiement | ML Engineer / Data Engineer |

---

## 3. 👥 Équipe et Contributions

Le projet est le fruit d'une **collaboration entre 3 contributeurs** :

| Contributeur | Rôle principal | Contributions clés |
|---|---|---|
| **Khalid** (khal-frj3041) | Chef de projet / Data Engineer | Données initiales, simulation, amélioration du modèle, application Streamlit |
| **Tahri-jpg** | ML Engineer | Exploration des données, tests de modèles (SVM, Decision Trees), projections réelles |
| **AmineKL-dev** | ML Engineer | Graphiques, visualisations, notebook expérimental |

---

## 4. 🔬 Profil ML Engineer — Compétences Démontrées

### 4.1 Exploration des Données (EDA)
- **Analyse statistique** des distributions des transactions
- **Visualisation** avec Matplotlib/Seaborn (graphiques, importance des features)
- Identification du **déséquilibre des classes** (fraude vs légitime)

### 4.2 Modélisation Machine Learning
Les notebooks montrent l'expérimentation avec **plusieurs algorithmes** :
- 🌳 **Decision Trees** — Arbres de décision
- 🔀 **SVM** (Support Vector Machines)
- 🌲 **Random Forest** (modèle sauvegardé en `.pkl`)
- Potentiellement d'autres modèles d'ensemble

### 4.3 Pipeline ML Complet

```
Données brutes → Prétraitement → Feature Engineering → Entraînement → Évaluation → Sérialisation → Déploiement
```

- **Normalisation** des features (StandardScaler sauvegardé en `scaler_fraud_detection.pkl`)
- **Feature Importance** analysée et visualisée
- **Sérialisation** du meilleur modèle avec `pickle` (`best_model_fraud_detection.pkl`)
- **Versionnement** de l'amélioration (notebook v1 → notebook Improved)

### 4.4 Système de Scoring de Risque
L'application implémente un **algorithme de scoring multi-critères** :

```python
def predict_fraud(montant, montant_moyen, is_foreign, is_high_risk, is_declined, nb_refus):
    score = 0
    # Ratio montant / moyenne (poids: 8-40 pts)
    # Montant absolu (poids: 8-25 pts)
    # Transaction étrangère (+10 pts)
    # Pays à haut risque (+20 pts)
    # Transaction refusée (+5 pts)
    # Nombre de refus (+5-20 pts)
    # Variabilité aléatoire (-5 à +5)
    return score  # Score entre 0 et 100
```

**Classification à 3 niveaux :**

| Score | Niveau | Action |
|---|---|---|
| ≥ 70% | 🔴 FRAUDE | Blocage immédiat |
| 40-69% | 🟡 SUSPECT | Vérification manuelle |
| < 40% | 🟢 LÉGITIME | Transaction validée |

---

## 5. 🔧 Profil Data Engineer — Compétences Démontrées

### 5.1 Pipeline de Données
- **Ingestion** : Chargement des données CSV brutes (`credit_card.csv`)
- **Transformation** : Nettoyage, encoding, normalisation → `credit_card_processed.csv`
- **Feature Store** : Sauvegarde du scaler et du modèle en format pickle

### 5.2 Architecture de l'Application

```python
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import random
from streamlit_autorefresh import st_autorefresh
```

### 5.3 Traitement en Temps Réel (Streaming)
L'application Streamlit implémente un **flux de données en temps réel** :
- **Auto-refresh** toutes les 2 secondes via `streamlit_autorefresh`
- **Génération simulée** de transactions aléatoires
- **Gestion d'état** avec `st.session_state` (transactions, statistiques, état du streaming)
- **Buffer circulaire** : conservation des 10 dernières transactions

### 5.4 Tableau de Bord (Dashboard)
- **KPIs en temps réel** : Transactions analysées, Fraudes détectées, Suspectes, Légitimes, Taux de fraude
- **Interface responsive** avec CSS personnalisé et animations
- **Alertes visuelles** différenciées (rouge/jaune/vert)

### 5.5 Gestion du Versionnement (Git)
- Utilisation de **Git/GitHub** pour la collaboration
- **Merges** entre branches de différents contributeurs
- Historique de commits structuré (13 commits sur 5 jours)

---

## 6. 🐍 Niveau Python — Évaluation

### 6.1 Grille d'évaluation

| Compétence | Niveau | Détail |
|---|---|---|
| **Syntaxe de base** | ⭐⭐⭐⭐⭐ | Variables, fonctions, conditions, boucles |
| **Programmation orientée données** | ⭐⭐⭐⭐ | Pandas, NumPy, manipulation de DataFrames |
| **Machine Learning** | ⭐⭐⭐⭐ | Scikit-learn (modèles, scaler, pickle) |
| **Visualisation** | ⭐⭐⭐⭐ | Matplotlib, Seaborn, graphiques avancés |
| **Développement Web** | ⭐⭐⭐⭐ | Streamlit, gestion d'état, CSS intégré |
| **Architecture logicielle** | ⭐⭐⭐ | Fonctions bien structurées, mais pas de classes OOP |
| **Gestion des erreurs** | ⭐⭐ | Vérifications basiques (division par zéro) |
| **Tests unitaires** | ⭐ | Absents du projet |
| **Documentation** | ⭐⭐⭐ | Docstrings présentes, mais pas de README |

### 6.2 Niveau Global : **Intermédiaire Avancé** 🟢

**Points forts :**
- ✅ Maîtrise de l'écosystème **Data Science Python** (Pandas, NumPy, Scikit-learn)
- ✅ Capacité à construire un **pipeline ML end-to-end**
- ✅ Développement d'une **application web fonctionnelle** avec Streamlit
- ✅ Utilisation de **features avancées** : session state, auto-refresh, CSS personnalisé
- ✅ **Sérialisation** des modèles pour le déploiement

**Axes d'amélioration :**
- ⚠️ Ajouter un fichier `README.md` documentant le projet
- ⚠️ Ajouter un `requirements.txt` pour la reproductibilité
- ⚠️ Implémenter des **tests unitaires** (pytest)
- ⚠️ Utiliser des **classes Python** (OOP) pour mieux structurer le code
- ⚠️ Ajouter une **gestion des erreurs** plus robuste (try/except)
- ⚠️ Remplacer le modèle à règles dans `app.py` par le vrai modèle ML sérialisé

---

## 7. 🏗️ Stack Technique

```
📊 Data Science     : Pandas, NumPy, Scikit-learn
📈 Visualisation    : Matplotlib, Seaborn
🤖 ML Models        : Decision Trees, SVM, Random Forest
💾 Sérialisation    : Pickle (.pkl)
🌐 Web App          : Streamlit, streamlit_autorefresh
🎨 Frontend         : HTML/CSS inline, Animations CSS
🔄 Versionnement    : Git, GitHub
📓 Notebooks        : Jupyter Notebook
```

---

## 8. 📊 Résumé des Profils

### Profil ML Engineer ✅
> Ce projet démontre une capacité à **concevoir, entraîner, évaluer et déployer** des modèles de Machine Learning pour un cas d'usage réel (détection de fraude). L'expérimentation avec plusieurs algorithmes et l'itération (version initiale → version améliorée) montrent une **démarche scientifique rigoureuse**.

### Profil Data Engineer ✅
> Le projet montre la maîtrise de la **chaîne de traitement des données** : ingestion, transformation, stockage, et exposition via un dashboard interactif en temps réel. La gestion du streaming simulé et de l'état applicatif démontre une compréhension des **architectures data en production**.

---

## 9. 💡 Recommandations d'Amélioration

1. **Charger le vrai modèle ML** (`best_model_fraud_detection.pkl`) dans `app.py` au lieu du système à règles
2. Ajouter un **`README.md`** professionnel avec instructions d'installation
3. Créer un **`requirements.txt`** (`pip freeze`)
4. Ajouter des **métriques du modèle** dans le dashboard (précision, recall, F1-score, matrice de confusion)
5. Implémenter un **pipeline CI/CD** avec GitHub Actions
6. Ajouter un **Dockerfile** pour conteneuriser l'application
7. Intégrer un **stockage persistant** (base de données) pour l'historique des transactions

---

*Rapport généré le 10/03/2026 — basé sur l'analyse du dépôt [khalid058r/Fraude_detection_Trans](https://github.com/khalid058r/Fraude_detection_Trans)*
