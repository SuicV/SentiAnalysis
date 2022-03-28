import streamlit as st
from utils.navbar import navbar
from Preprocessors.ReviewPreprocessor import ReviewPreprocessor

st.set_page_config(page_title='Topic Detection', layout="wide")

nv_bar = navbar()