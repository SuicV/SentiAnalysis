from matplotlib.pyplot import bar
import streamlit as st
from utils.navbar import navbar
from pages import *

st.set_page_config(page_title='Opinion mining', layout="wide")

nv_bar = navbar()

if nv_bar == "Home":
    home.home()
