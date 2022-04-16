import streamlit as st


def preprocessing_form():

    with st.form("preprocessing_form"):
        dataset = st.file_uploader("dataset", "csv", False)
        form_submition = st.form_submit_button("Clean")

    return dataset, form_submition