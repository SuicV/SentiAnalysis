import streamlit as st
def scrap_by_search_form():
    # scrap reviews by search tag
    with st.form("get_reviews_by_search"):
        col1, col2 = st.columns(2)
        with col1:
            search_tag = st.text_input("search tag", "Marrakech hotels")
            search_num_pages = st.number_input("number of reviews pages to scrap", min_value=1, max_value=100)
            pass
        with col2:
            otas_values = st.multiselect("Online travel agencies", options=["TripAdvisor", "Agoda"])
            urls_count = st.number_input("Number of urls to scrap", min_value=1, max_value=50)
            pass
        search_form_submition_button = st.form_submit_button("Scrap")
        data = {
            "search_tag": search_tag, "search_num_pages": search_num_pages, "otas_values": otas_values,
            "urls_count": urls_count
        }
        return data, search_form_submition_button