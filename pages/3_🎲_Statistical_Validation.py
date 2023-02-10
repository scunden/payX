import streamlit as st
import payequity as pe
import pandas as pd
import streamlit_ext as ste

import plotly.graph_objects as go


def main():
        
    jge = st.session_state['jge']
    st.title('Talent Ai Pay Equity')
    
    st.markdown("""---""") 
    
    st.header("🔢 Model Evaluation")
    summary = jge.audit.summary.copy()
    num_models = summary.shape[0]
    
    st.write("Failed to create job groups for {} groups".format(summary.loc[summary['Observations']<95].shape[0]))
    for jg in summary.loc[summary['Observations']<95]['Job Group']:
        st.error('Error: Job group not created for "{}" due to insufficient headcount'.format(jg), icon="🚨")
        
        
    st.write("{} out of the {} job groups need to be carefully analyzed: ".format(summary.loc[summary['DoF Ratio']<8].shape[0], num_models))    
    for jg in summary.loc[summary['DoF Ratio']<8]['Job Group']:
        st.warning('Warning: Job group "{}" has either low headcount, or too many features - see documentation'.format(jg), icon="⚠️")
        
    st.markdown("""---""") 
    
    
    st.header("✨ Model Performance")
    num_perf = summary.loc[summary['MAPE']>0.10].shape[0]
    if num_perf > 0:
        st.success("{} out of {} models are able to predict pay with reasonable accuracy!".format(num_models-num_perf, num_models))    
          
    for jg in summary.loc[summary['MAPE']>0.10]['Job Group']:
        st.warning('Warning: Job group "{}" has accuracy issues - see documentation'.format(jg), icon="⚠️")
        
    st.markdown("""---""") 
    
    st.header("🛑 Illegitimate Factors Evaluation")
    hug_coef = jge.audit.hug_coef.copy()
    high_vif = hug_coef.loc[hug_coef['VIF']>1.3]['Job Group'].unique().tolist()
    if len(high_vif)==0:
        st.success("All models have interpretable pay gaps")    
        
    for jg, div in hug_coef.loc[hug_coef['VIF']>1.3][['Job Group','Variable']].values:
        st.error('Error: Job group "{}" has an unreliable "{}" pay gap'.format(jg, div), icon="🚨")
        
    st.markdown("""---""") 
    
    st.header("🎯 Legitimate Factors Evaluation")
    predictive_coef = jge.audit.predictive_coef.copy()
    high_vif_pred = predictive_coef.loc[predictive_coef['VIF']>5]['Job Group'].unique().tolist()
    if len(high_vif_pred)==0:
        st.success("All models have interpretable coefficients")    
        
    for jg, var in predictive_coef.loc[predictive_coef['VIF']>5][['Job Group','Variable']].values:
        st.warning('Warning: Job group "{}" has an unreliable "{}" pay gap'.format(jg, var), icon="⚠️")
    st.markdown("""---""") 

if __name__=="__main__":
    main()