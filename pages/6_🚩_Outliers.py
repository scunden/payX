import streamlit as st
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from payequity.payequity import Audit, JobGroup, JobGroupEnssemble, Regressor

import pandas as pd
import streamlit_ext as ste
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
        page_title="Talent Ai PayX",
        page_icon="🎇",
    )


def plot_outliers(df, o_type="Lower"):
    color_schemes = px.colors.qualitative.Prism
    outlier = "{} Outlier Rate".format(o_type) if o_type!="" else "Outlier Rate"
    df = df.sort_values(by=['Job Group'])
    
    
    st.subheader("📈 {} Outlier Rate by Job Group".format(o_type))
    threshold = 0.025 if o_type!="" else 0.05
    color = ["Above" if x >= threshold else "Below" for x in df[outlier].tolist()]
    
    fig = px.bar(df, x="Job Group", y=outlier, 
                 color=color, 
                 color_discrete_map={'Above': color_schemes[7],'Below': color_schemes[1]},
                 text_auto=".1%"
                 )
    fig.update_layout(yaxis_tickformat = '.0%')
    
    return fig

def main():
    st.title('Talent Ai Pay Equity')
    st.markdown("""---""") 
    jge = st.session_state['jge']
    df = jge.audit.summary.copy()
    
    st.markdown("""---""") 
    tab1, tab2, tab3 = st.tabs(["Lower Outliers", "Upper Outliers", "Total Outliers"])
    with tab1:
        fig1 = plot_outliers(df, o_type="Lower")
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        fig2 = plot_outliers(df, o_type="Upper")
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    with tab3:
        fig3 = plot_outliers(df, o_type="")
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

if __name__=="__main__":
    main()