import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import random
from streamlit_autorefresh import st_autorefresh

# Configuration de la page
st.set_page_config(
    page_title=" Détection de Fraude",
    page_icon="",
    layout="wide"
)

# Auto-refresh quand le streaming est actif
if 'streaming' in st.session_state and st.session_state.streaming:
    st_autorefresh(interval=2000, limit=None, key="auto_refresh")

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a5f, #2d5a87);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .fraud-alert {
        background: linear-gradient(135deg, #ff4757, #ff6b81);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        animation: pulse 2s infinite;
    }
    .safe-alert {
        background: linear-gradient(135deg, #2ed573, #7bed9f);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .suspect-alert {
        background: linear-gradient(135deg, #ffa502, #ffcc00);
        padding: 20px;
        border-radius: 10px;
        color: #333;
        text-align: center;
    }
    .stat-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #1e3a5f;
    }
    .transaction-ok { color: #2ed573; }
    .transaction-fraud { color: #ff4757; }
    .transaction-suspect { color: #ffa502; }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 71, 87, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 71, 87, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 71, 87, 0); }
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de l'état de session
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'analyzed': 0,
        'frauds': 0,
        'suspects': 0,
        'legitimate': 0
    }
if 'streaming' not in st.session_state:
    st.session_state.streaming = False
if 'transaction_id' not in st.session_state:
    st.session_state.transaction_id = 220

def predict_fraud(montant, montant_moyen, is_foreign, is_high_risk, is_declined, nb_refus):
    """
    Algorithme de détection de fraude basé sur des règles et un score de risque
    """
    score = 0
    
    # Ratio montant / moyenne
    if montant_moyen > 0:
        ratio = montant / montant_moyen
        if ratio > 25:
            score += 40
        elif ratio > 10:
            score += 25
        elif ratio > 5:
            score += 15
        elif ratio > 3:
            score += 8
    
    # Montant absolu
    if montant > 10000:
        score += 25
    elif montant > 5000:
        score += 15
    elif montant > 2000:
        score += 8
    
    # Transaction étrangère
    if is_foreign:
        score += 10
    
    # Pays à haut risque
    if is_high_risk:
        score += 20
    
    # Transaction refusée
    if is_declined:
        score += 5
    
    # Nombre de refus aujourd'hui
    if nb_refus >= 5:
        score += 20
    elif nb_refus >= 3:
        score += 12
    elif nb_refus >= 1:
        score += 5
    
    # Ajouter un peu de variabilité
    score += random.uniform(-5, 5)
    score = max(0, min(100, score))
    
    return score

def get_fraud_level(score):
    if score >= 70:
        return "FRAUDE", "🔴", "fraud-alert"
    elif score >= 40:
        return "SUSPECT", "🟡", "suspect-alert"
    else:
        return "LÉGITIME", "🟢", "safe-alert"

def generate_random_transaction():
    """Génère une transaction aléatoire pour le flux en temps réel"""
    montant = random.choice([
        random.randint(10, 200),
        random.randint(50, 500),
        random.randint(100, 1000),
        random.randint(500, 3000),
        random.randint(2000, 15000)
    ])
    return montant

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1>🔒 SYSTÈME DE DÉTECTION DE FRAUDE</h1>
    <p>Analyse intelligente des transactions en temps réel</p>
</div>
""", unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([1, 1])

# Colonne gauche - Formulaire d'analyse
with col1:
    st.markdown("### 📝 ANALYSER UNE TRANSACTION")
    
    with st.form("transaction_form"):
        montant = st.number_input("Montant ($)", min_value=0.0, value=5000.0, step=100.0)
        montant_moyen = st.number_input("Montant moyen/jour ($)", min_value=0.0, value=200.0, step=50.0)
        
        col_check1, col_check2 = st.columns(2)
        with col_check1:
            is_foreign = st.checkbox("Transaction étrangère", value=True)
            is_declined = st.checkbox("Transaction refusée")
        with col_check2:
            is_high_risk = st.checkbox("Pays à haut risque", value=True)
        
        nb_refus = st.number_input("Nombre de refus aujourd'hui", min_value=0, value=3, step=1)
        
        submitted = st.form_submit_button("🔍 ANALYSER", use_container_width=True)
    
    if submitted:
        score = predict_fraud(montant, montant_moyen, is_foreign, is_high_risk, is_declined, nb_refus)
        level, emoji, css_class = get_fraud_level(score)
        
        # Mise à jour des statistiques
        st.session_state.stats['analyzed'] += 1
        if level == "FRAUDE":
            st.session_state.stats['frauds'] += 1
        elif level == "SUSPECT":
            st.session_state.stats['suspects'] += 1
        else:
            st.session_state.stats['legitimate'] += 1
        
        # Affichage du résultat
        st.markdown("### 📊 RÉSULTAT DE L'ANALYSE")
        
        if level == "FRAUDE":
            st.markdown(f"""
            <div class="fraud-alert">
                <h2>⚠️ FRAUDE DÉTECTÉE !</h2>
                <h3>Probabilité: {score:.1f}%</h3>
                <p>Niveau: ÉLEVÉ {emoji}</p>
            </div>
            """, unsafe_allow_html=True)
            st.error(f"🚨 Transaction de ${montant:,.2f} identifiée comme FRAUDULEUSE avec un score de {score:.1f}%")
        elif level == "SUSPECT":
            st.markdown(f"""
            <div class="suspect-alert">
                <h2>⚠️ TRANSACTION SUSPECTE</h2>
                <h3>Probabilité: {score:.1f}%</h3>
                <p>Niveau: MOYEN {emoji}</p>
            </div>
            """, unsafe_allow_html=True)
            st.warning(f"⚠️ Transaction de ${montant:,.2f} nécessite une vérification - Score: {score:.1f}%")
        else:
            st.markdown(f"""
            <div class="safe-alert">
                <h2>✅ TRANSACTION LÉGITIME</h2>
                <h3>Probabilité de fraude: {score:.1f}%</h3>
                <p>Niveau: FAIBLE {emoji}</p>
            </div>
            """, unsafe_allow_html=True)
            st.success(f"✅ Transaction de ${montant:,.2f} validée - Score de risque: {score:.1f}%")
        
        # Barre de progression
        st.progress(score / 100)

# Colonne droite - Flux en temps réel
with col2:
    st.markdown("### ⏱️ FLUX EN TEMPS RÉEL")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        start_btn = st.button("▶️ Démarrer", use_container_width=True, key="start_btn")
        if start_btn:
            st.session_state.streaming = True
            st.rerun()
    with col_btn2:
        pause_btn = st.button("⏸️ Pause", use_container_width=True, key="pause_btn")
        if pause_btn:
            st.session_state.streaming = False
            st.rerun()
    with col_btn3:
        reset_btn = st.button("🔄 Reset", use_container_width=True, key="reset_btn")
        if reset_btn:
            st.session_state.transactions = []
            st.session_state.transaction_id = 220
            st.session_state.stats = {
                'analyzed': 0,
                'frauds': 0,
                'suspects': 0,
                'legitimate': 0
            }
            st.session_state.streaming = False
            st.rerun()
    
    # Indicateur de statut
    if st.session_state.streaming:
        st.success("🟢 Flux actif - Génération automatique de transactions")
    else:
        st.info("⏸️ Flux en pause - Cliquez sur 'Démarrer' pour activer")
    
    # Conteneur pour les transactions
    transaction_container = st.container()
    
    # Générer une nouvelle transaction si le streaming est actif
    if st.session_state.streaming:
        # Générer une nouvelle transaction
        st.session_state.transaction_id += 1
        montant_rand = generate_random_transaction()
        score_rand = predict_fraud(
            montant_rand, 
            200, 
            random.random() > 0.7,
            random.random() > 0.8,
            random.random() > 0.9,
            random.randint(0, 5)
        )
        level_rand, emoji_rand, _ = get_fraud_level(score_rand)
        
        # Mise à jour stats
        st.session_state.stats['analyzed'] += 1
        if level_rand == "FRAUDE":
            st.session_state.stats['frauds'] += 1
        elif level_rand == "SUSPECT":
            st.session_state.stats['suspects'] += 1
        else:
            st.session_state.stats['legitimate'] += 1
        
        new_transaction = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'id': st.session_state.transaction_id,
            'amount': montant_rand,
            'status': level_rand,
            'emoji': emoji_rand
        }
        
        st.session_state.transactions.insert(0, new_transaction)
        st.session_state.transactions = st.session_state.transactions[:10]  # Garder les 10 dernières
    
    # Afficher les transactions
    with transaction_container:
        if st.session_state.transactions:
            for trans in st.session_state.transactions[:5]:
                status_class = "transaction-ok" if trans['status'] == "LÉGITIME" else \
                              ("transaction-fraud" if trans['status'] == "FRAUDE" else "transaction-suspect")
                
                status_text = "OK" if trans['status'] == "LÉGITIME" else \
                             ("FRAUDE!" if trans['status'] == "FRAUDE" else "SUSPECT")
                
                st.markdown(f"""
                <div style="padding: 8px; margin: 5px 0; background: #f8f9fa; border-radius: 5px; 
                            border-left: 4px solid {'#2ed573' if trans['status'] == 'LÉGITIME' else ('#ff4757' if trans['status'] == 'FRAUDE' else '#ffa502')};">
                    <span style="color: #666;">{trans['time']}</span>
                    <span style="margin-left: 10px;">#{trans['id']}</span>
                    <span style="margin-left: 10px; font-weight: bold;">${trans['amount']:,}</span>
                    <span style="margin-left: 10px;" class="{status_class}">{trans['emoji']} {status_text}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Cliquez sur 'Démarrer' pour voir le flux de transactions en temps réel")

# Section Statistiques
st.markdown("---")
st.markdown("### 📈 STATISTIQUES")

col_stat1, col_stat2, col_stat3, col_stat4, col_stat5 = st.columns(5)

with col_stat1:
    st.metric("Analysées", f"{st.session_state.stats['analyzed']:,}")

with col_stat2:
    st.metric("Fraudes", f"{st.session_state.stats['frauds']}", 
              delta=None if st.session_state.stats['frauds'] == 0 else f"+{st.session_state.stats['frauds']}")

with col_stat3:
    st.metric("Suspectes", f"{st.session_state.stats['suspects']}")

with col_stat4:
    st.metric("Légitimes", f"{st.session_state.stats['legitimate']}")

with col_stat5:
    taux_fraude = (st.session_state.stats['frauds'] / st.session_state.stats['analyzed'] * 100) \
                  if st.session_state.stats['analyzed'] > 0 else 0
    st.metric("Taux Fraude", f"{taux_fraude:.1f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🔒 Système de Détection de Fraude v1.0 | Propulsé par Machine Learning</p>
</div>
""", unsafe_allow_html=True)
