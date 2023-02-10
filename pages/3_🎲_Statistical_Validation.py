import streamlit as st
import payequity as pe
import pandas as pd
import streamlit_ext as ste


def main():
    try:
        jge = st.session_state['jge']
        st.success("Loaded JGE")
    except:
        st.error("JGE not loaded")
        
    st.title('Talent Ai Pay Equity')
    
    st.markdown("""---""") 
    
    st.header("🔢 Model Evaluation")
    st.markdown("""---""") 
    
    st.header("✨ Model Performance")
    st.markdown("""---""") 
    
    st.header("🛑 Illegitimate Factors Evaluation")
    st.markdown("""---""") 
    
    st.header("🎯 Legitimate Factors Evaluation")
    st.markdown("""---""") 

if __name__=="__main__":
    main()