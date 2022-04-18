import streamlit as st

def scrap_by_link_form():
    with st.form("get_links_by_urls"):
        col1, col2 = st.columns(2)
        with col1:
            tripadvisor_url = st.text_input("tripadvisor hotel url", value="")
            pass
        with col2:
            agoda_url = st.text_input("agoda hotel url", value="")
            agoda_option = st.checkbox("Agoda reviews", True)
            booking_option = st.checkbox("Booking reviews", False)
            pass

        num_pages = st.number_input("Number of pages to scrap", min_value=1, max_value=100)
        link_form_submition_button = st.form_submit_button()
        data = {"tripadvisor_url": tripadvisor_url, "agoda_url": agoda_url,
            "num_pages": num_pages, "agoda_option": agoda_option, "booking_option":booking_option}
        return data, link_form_submition_button
    pass