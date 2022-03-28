import streamlit as st

def home():

    st.write('--------------------------------------------')
    st.markdown("<h1 style='text-align: center'>Service Quality Controle</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center'>Nowadays, the abundance of online reviews about products and services, might be an indicator for enterprises about their performance and the satisfaction of their clients.<br /> For this reason, we created a system for sentiment analysis of online reviews, to analyze sentiment about different aspects of a business.</h5>", unsafe_allow_html=True)
        
    st.write(' ')

    st.markdown("<h4>Fonctionnalities:</h4>", unsafe_allow_html=True)
    st.markdown("1- Reviews Scrapping")
    st.markdown("2- Reviews Preprocessing")
    st.markdown("3- Aspects Extraction")
    st.markdown("4- Sentiment Classification")

    st.markdown('')
    st.markdown("<h6 style='text-align: center'>Made By: OULAHBIB Idriss</h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center'>Supervised By: Pr.BOUKHAROUK Mohamed & Pr.OUAARAB Aziz</h6>", unsafe_allow_html=True)
    st.write('--------------------------------------------')
