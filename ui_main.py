import streamlit as st
# navbar import
from UI.utils.navbar import navbar
# pages imports
from UI.pages.home import home
from UI.pages.preprocessing_page import preprocessing_page
from UI.pages.aspect_extraction_page import aspects_extraction_page
from UI.pages.sentiment_classification_page import sentiment_classification_page
from UI.pages.scraping_page import scraping_page

st.set_page_config(page_title='Opinion mining', layout="wide")

nv_bar = navbar()

if nv_bar == "Home":
    home()
if nv_bar == "Reviews Scraping":
    scraping_page()
elif nv_bar == "Reviews Preprocessing":
    preprocessing_page()
elif nv_bar == "Aspects Extraction":
    aspects_extraction_page()
elif nv_bar == "Sentiments Classification":
    sentiment_classification_page()