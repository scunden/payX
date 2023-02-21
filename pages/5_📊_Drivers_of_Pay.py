import streamlit as st
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from payequity.payequity import Audit, JobGroup, JobGroupEnssemble, Regressor

import pandas as pd
import streamlit_ext as ste

st.set_page_config(
        page_title="Talent Ai PayX",
        page_icon="🎇",
    )

def main():
    pass

if __name__=="__main__":
    main()