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
    
    df = df.loc[(df.Variable==div)&(df.Feature==feature)].sort_values(by=["Job Group"]).reset_index(drop=True)
    
    ref = df.Reference.unique()[0]
    st.subheader("🚨 {} Pay Gap : {} v/s {}".format(div.title(), feature.title(), ref.title()))
    fig = px.bar(df, x="Job Group", y=y, color=color, 
                 color_discrete_map={'Yes': color_schemes[7],'No': color_schemes[10]},
                 text_auto=".1%"
                 )
    fig.update_layout(yaxis_tickformat = '.0%',yaxis_title="{} Pay Gap".format(div.title()))
    
    gap_ex = df.loc[df["Exp. Coef."]<0]["Exp. Coef."]
    gap_ex = df["Exp. Coef."] if gap_ex.shape[0]==0 else gap_ex
    jg_ex = df["Job Group"].loc[gap_ex.index[0]]
    more_less = "more" if gap_ex.iloc[0] > 0 else "less"
    st.write(docs.PAY_GAP_EX.format(jg_ex, jg_ex, feature, abs(gap_ex.iloc[0]), more_less, ref))
    
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
        
if __name__=="__main__":
    if "jge" in st.session_state.keys():
        main()
    else:
        st.error(docs.VAL_PLACEHOLDER, icon="🚨")