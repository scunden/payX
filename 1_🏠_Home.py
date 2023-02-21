import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from payequity.payequity import Audit, JobGroup, JobGroupEnssemble, Regressor

import streamlit as st
import docs

st.set_page_config(
        page_title="Talent Ai PayX",
        page_icon="🎇",
    )

def main():
    for k, v in st.session_state.items():
        st.session_state[k] = v

    
    st.title('Talent Ai Pay Equity')

    st.markdown("""---""") 
    st.write(docs.WELCOME)
    st.markdown("""---""")
    st.subheader("🔑 Key Variables")
    st.write(docs.KEY_VARIABLES)
    # Job Groups, Pay Component, Illegitimate Variables, Legitimate Variables
    kv_columns  = st.columns(4)
    if kv_columns[0].button("Job Group"): st.write(docs.JOB_GROUP)
    if kv_columns[1].button("Pay Component"): st.write(docs.JOB_GROUP)

    kv_columns[2].button("Illegitimate Factors")
    kv_columns[3].button("Legitimate Factors")
    st.markdown("""---""")

    st.subheader("🎲 Statistical Validation")
    st.write(docs.VALIDATION)
    sv_columns  = st.columns(4)
    sv_columns[0].button("Minimum Headcount")
    sv_columns[1].button("Headcount/Feature Balance")
    sv_columns[2].button("Model Performance")
    sv_columns[3].button("Correlated Features")
    st.markdown("""---""")

    st.subheader("🚨 Pay Gaps")
    st.markdown("""---""")

    st.subheader("📊 Drivers of Pay")
    st.markdown("""---""")

    st.subheader("🚩 Outliers")
    st.markdown("""---""")
    st.subheader("💊 Remediation")
    st.subheader("🎯 Gap Exploration")
    st.subheader("💸 Fair Pay Calculator")

if __name__=="__main__":
    main()