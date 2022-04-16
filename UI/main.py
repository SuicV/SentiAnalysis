import sys
if "E:\\PychCarmProjects\\s4\\ServQC_ML" not in sys.path:
    sys.path.append("E:\\PychCarmProjects\\s4\\ServQC_ML")

import streamlit as st
from utils.navbar import navbar
# pages imports
from pages.home import home
from pages.preprocessing_page import preprocessing_page
from pages.aspect_extraction_page import aspects_extraction_page
from pages.sentiment_classification_page import sentiment_classification_page
from pages.scraping_page import scraping_page
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