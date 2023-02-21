import streamlit as st
import pandas as pd
import numpy as np
import streamlit_ext as ste
import docs
import plotly.express as px

st.set_page_config(
        page_title="Talent Ai PayX",
        page_icon="🎇",
    )


def plot_pay_gaps(df, div, feature, y="Exp. Coef.", color="Significant"):
    color_schemes = px.colors.qualitative.Prism
    
    df = df.loc[(df.Variable==div)&(df.Feature==feature)].sort_values(by=["Job Group"])
    ref = df.Reference.unique()[0]
    st.subheader("🚨 {} Pay Gap : {} v/s {}".format(div.title(), feature.title(), ref.title()))
    fig = px.bar(df, x="Job Group", y=y, color=color, 
                 color_discrete_map={'Yes': color_schemes[7],'No': color_schemes[10]},
                 text_auto=".1%"
                 )
    fig.update_layout(yaxis_tickformat = '.0%')
    
    return fig

def plot_headcount(jge, div, feature, x='Job Group', y='Headcount'):
    st.subheader("👨‍👩‍👧‍👦 Headcount by {} & Job Group".format(div.title()))
    jgc = jge.column_map_inv[jge.job_group_column]
    df = jge.audit.df.copy().sort_values(by=[jgc])
    
    
    df = df.groupby([jgc, div]).size().reset_index()
    df = df.rename({0:y,jgc:x}, axis=1)
    fig = px.bar(df, x=x, y=y, color=div, text_auto=True)
    
    return fig

def plot_distribution(jge, div, feature, x='Job Group', y='Headcount'):
    st.subheader("👨‍👩‍👧‍👦 Headcount Distribution by {} & Job Group".format(div.title()))
    jgc = jge.column_map_inv[jge.job_group_column]
    df = jge.audit.df.copy().sort_values(by=[jgc])
    
    
    df_stack = df.groupby([jgc, div]).size().reset_index()
    df_stack['Percentage'] = df.groupby([jgc, div]).size().groupby(level=[0], group_keys=True).apply(lambda 
        x:x/float(x.sum())).values
    df_stack = df_stack.rename({0:y,jgc:x}, axis=1)
    fig = px.bar(df_stack, x=x, y='Percentage', color=div, text_auto=".0%")
    fig.update_layout(yaxis_tickformat = '.0%')
    
    return fig

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
    df = jge.audit.hug_coef.copy()
    
    st.subheader("⚙️ Select Parameters")
    columns = st.columns(2)
    st.markdown("""---""") 
    div = columns[0].selectbox(label="Select Diversity: ", options=df.Variable.unique())
    
    features_options = df.loc[df.Variable==div].Feature.unique().tolist()
    feature = columns[1].selectbox(label="Select Feature: ", options=features_options)
    
    tab1, tab2, tab3 = st.tabs(["Pay Gaps", "Headcount", "Distribution"])
    with tab1:
        fig1 = plot_pay_gaps(df, div=div, feature=feature)
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        fig2 = plot_headcount(jge, div=div, feature=feature)
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    with tab3:
        fig3 = plot_distribution(jge, div=div, feature=feature)
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
       
    st.markdown("""---""") 
    o_df = jge.audit.summary.copy()
    
    st.markdown("""---""") 
    tab1o, tab2o, tab3o = st.tabs(["Lower Outliers", "Upper Outliers", "Total Outliers"])
    with tab1o:
        fig1o = plot_outliers(o_df, o_type="Lower")
        st.plotly_chart(fig1o, theme="streamlit", use_container_width=True)
    with tab2o:
        fig2o = plot_outliers(o_df, o_type="Upper")
        st.plotly_chart(fig2o, theme="streamlit", use_container_width=True)
    with tab3o:
        fig3o = plot_outliers(o_df, o_type="")
        st.plotly_chart(fig3o, theme="streamlit", use_container_width=True)

if __name__=="__main__":
    if "jge" in st.session_state.keys():
        main()
    else:
        st.error(docs.VAL_PLACEHOLDER, icon="🚨")