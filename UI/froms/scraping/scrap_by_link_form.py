import streamlit as st

def scrap_by_link_form():
    with st.form("get_links_by_urls"):
        col1, col2 = st.columns(2)
        with col1:
            tripadvisor_url = st.text_input("tripadvisor hotel url", value="")
            tripadvisor_url_pages = st.number_input("number of pages to scrap from tripadvisor", min_value=1, max_value=100)
            pass
        with col2:
            agoda_url = st.text_input("agoda hotel url", value="")
            agoda_url_pages = st.number_input("number of pages to scrap from agoda", min_value=1, max_value=100)
            pass
        link_form_submition_button = st.form_submit_button()
        data = {"tripadvisor_url": tripadvisor_url, "tripadvisor_url_pages": tripadvisor_url_pages,
            "agoda_url": agoda_url, "agoda_url_pages": agoda_url_pages}
        return data, link_form_submition_button
    pass