import streamlit as st
import client, home, general
import pandas as pd
import os




st.set_page_config(layout="wide", page_title='dashboard P7')


@st.cache_data
def load_data():
    df_test = pd.read_csv('test_data_prod.csv', index_col=0)
    df_total = pd.read_csv('df_total_prod.csv', index_col=0)
    df_analyse=pd.read_csv('app_train_prod.csv', index_col=0)
    df_analyse=df_analyse[['TARGET','NAME_CONTRACT_TYPE','CODE_GENDER','AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY',
                       'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 
                       'OCCUPATION_TYPE']].copy()
    return df_test,df_total,df_analyse

df_test,df_total,df_analyse = load_data()


def main():
    st.sidebar.title('Navigation')
    options = st.sidebar.selectbox('Select a page:',
                                   ['Home', 'General Information', 'Client Information'])

    if options == 'Home':
        home.home()
    elif options == 'General Information':
        general.general(df_analyse)
    elif options == 'Client Information':
        client.client(df_total, df_test)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    main()



