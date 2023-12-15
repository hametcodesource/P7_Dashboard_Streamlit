import streamlit as st

def home():
    st.image('PretADepenser.jpg', width=300)
    st.write("""
    Ce tableau de bord est composé de deux parties :
    
      
    **1. GENERAL INFORMATION**
    
        description du jeu de données et rappel interpretablite du modèle
            
    **2. CLIENT INFORMATION**
    
        Information sur un client , prediction crédit et interprétation résultat
    
    """)