import streamlit as st

def scrap_by_link_form():
    with st.form("get_links_by_urls"):
        col1, col2 = st.columns(2)
        with col1:
            tripadvisor_url = st.text_input("tripadvisor hotel url", value="")
            pass
        with col2:
            agoda_url = st.text_input("agoda hotel url", value="")
            pass
        num_pages = st.number_input("Number of pages to scrap", min_value=1, max_value=100)
        link_form_submition_button = st.form_submit_button()
        data = {"tripadvisor_url": tripadvisor_url, "agoda_url": agoda_url, "num_pages": num_pages}
        return data, link_form_submition_button
    pass