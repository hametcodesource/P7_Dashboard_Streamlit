import pandas as pd
import shap
import requests
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def client(df_total,df_test):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df_test=df_test.reset_index()
# dev
    #url = "http://127.0.0.1:5000/"
# prod
    url = "https://p7-api-flaskk-67a5da9a7e53.herokuapp.com/"


    list_client_id=list(df_total.SK_ID_CURR.unique())
    list_client_id=[str(id) for id in list_client_id]
    print(list_client_id)
    def update_sk(sk_id):
        predict_proba_1=0.5
        if sk_id in list_client_id:
            url_pred = url + "predict/" + sk_id
            response = requests.get(url_pred)
            if response:
                predict_proba_1 = float(response.json()['predict_proba_1'])
            else:
                print("erreur web : ", response)

        gauge_predict = go.Figure(go.Indicator( mode = "gauge+number",
                                                value = predict_proba_1*100,
                                                domain = {'x': [0, 1], 'y': [0, 1]},
                                                gauge = {
                                                    'axis': {'range': [0, 100], 'tickwidth': 0.2, 'tickcolor': "darkblue"},
                                                    'bgcolor': "lightcoral",
                                                    'steps': [
                                                        {'range': [0, 40], 'color': 'lightgreen'},
                                                        {'range': [40, 60], 'color': 'palegoldenrod'}
                                                    ],
                                                    'threshold': {
                                                        'line': {'color': "red", 'width': 4},
                                                        'thickness': 0.75,
                                                        'value': 100}},
                                                title = {'text': f"client {sk_id}"}))

        return gauge_predict


    option_sk = st.selectbox('Selectionner un numero de client',list_client_id)
    row_appli_sk = ( df_total['SK_ID_CURR'] == int(option_sk))

    st.subheader("Personnal Information")
    sex = df_total.loc[row_appli_sk, ['CODE_GENDER']].values[0][0]
    st.write("Sex :",sex)
    age = int(np.trunc(- int(df_total.loc[row_appli_sk, ['DAYS_BIRTH']].values)/365))
    st.write("Age :", age)
    Own_realty = df_total.loc[row_appli_sk, ['FLAG_OWN_REALTY']].values[0][0]
    st.write("Propriétaire(Maison/Appartement)  :", Own_realty)

    st.subheader("Credit Information")

    credit = str(df_total.loc[row_appli_sk, ['AMT_CREDIT']].values[0][0])
    st.write("Montant du crédit du prêt :", credit)
    annuity = df_total.loc[row_appli_sk, ['AMT_ANNUITY']].values[0][0] / 12
    st.write(f"Prêt mensuel : {annuity:.1f}")


    st.subheader("Retour Prediction")
    st.write("""
    **le retour est un score de 0 à 100. Le seuil de refus est à 50.**
    
    1. Un retour en dessous de 40 est une acceptation du crédit.
    
    2. Un retour au dessus de 60 est un refus du crédit.
    
    3. Pour un score entre 40 et 60, on va regarder l'interpretabilité de la prediction pour aider au choix. 
    
    On pourra s'aider aussi de la page "Client Analysis pour étudier le client et les clients lui ressemblant.
    """)


    fig = update_sk(option_sk)
    st.plotly_chart(fig)

    st.subheader("INTERPRETATION VALEURS SHAPLEY")
    st.write("""
        ** Les variables sont classes de haut en bas par ordre d'importance dans l'interpretation.** 
        
        **La  couleur pour chaque variable est un indicateur de l'influence sur la prediction.** 
        
        **Les variables en rouge font augmenter le score et donc le risque de defaut de paiement.**
         
        """)
    
    


    def update_shap(sk_id,df_test,var_):
        client_info=df_test[df_test.SK_ID_CURR==int(sk_id)]
        col=list(client_info.columns)
        col.remove("SK_ID_CURR")
        col.remove("index")
        print("okkkk",client_info)
        client_info=client_info[col]
        if sk_id in list_client_id:
            url_pred = url + "predict/" + sk_id
            print(url_pred)
            response = requests.get(url_pred)
            if response:
                shap_values =response.json()['shap_values']
                val=[shap_values[0][:8]]
                print("1",type(np.array(shap_values)))
                print("2",type(np.array(val)))
                print(shap_values)
            else:
                print("erreur web : ", response)
        #print(client_info)
        plt.figure(figsize=(8, 6))
        summary_plot=shap.summary_plot(np.array(shap_values), client_info,max_display=var_)
        plt.gcf().set_size_inches(20, 8)
        return plt.gcf()
    
    var_ = st.selectbox('Select Nombre de Variable:',range(3,20))
    fig=update_shap(option_sk,df_test,var_)
    st.pyplot(fig)
    
    st.subheader("Extrait des données de Test")
    st.table(df_test[df_test['SK_ID_CURR'] == int(option_sk)])

