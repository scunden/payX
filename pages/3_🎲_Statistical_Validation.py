import streamlit as st
import payequity as pe
import pandas as pd
import streamlit_ext as ste
import docs
import plotly.graph_objects as go


def no_jge():
    st.error(docs.VAL_PLACEHOLDER, icon="🚨")

def main():
        
    jge = st.session_state['jge']
    st.title('Talent Ai Pay Equity')
    
    st.markdown("""---""") 
    
    st.header("🔢 Model Evaluation")
    summary = jge.audit.summary.copy()
    num_models = summary.shape[0]
    rejected = len(jge.rejected_jg)
    overfit = summary.loc[summary['DoF Ratio']<8]['Job Group'].unique().tolist()
    good_perf = summary.loc[summary['MAPE']<=0.10]['Job Group'].unique().tolist()
    poor_perf = summary.loc[summary['MAPE']>0.10]['Job Group'].unique().tolist()
    
    if rejected == 0:
        st.success("All job groups successfully created!")
    else:
        st.success("Successfully created job groups for {} groups".format(num_models))
        st.error("Failed to create job groups for {} groups due to insufficient headcount, namely: {}".format(
            rejected, jge.rejected_jg), icon="🚨")
        st.write(docs.MINIMUM_HEADCOUNT)
        st.markdown("""---""") 
        
    if len(overfit)==0:
        st.success("All created job groups have sufficient statistical robustness")
    else:
        st.warning("{} out of the {} job groups need to be carefully analyzed, namely: {}".format(
            len(overfit), num_models, overfit), icon="⚠️")    
        st.write(docs.OVERFIT)
        
    st.markdown("""---""") 
    
    st.header("✨ Model Performance")
    
    if len(good_perf) > 0:
        st.success("{} out of {} models are able to predict pay with reasonable accuracy!".format(len(good_perf), num_models))    
        
    if len(poor_perf) > 0:
        st.warning("{} out of {} models have performance concerns, namely: {}. Please see documentation".format(
            len(poor_perf), num_models,poor_perf), icon="⚠️")  
        st.write(docs.PERFORMANCE)
          
    st.markdown("""---""") 
    
    st.header("🛑 Illegitimate Factors Evaluation")
    hug_coef = jge.audit.hug_coef.copy()
    high_vif = hug_coef.loc[hug_coef['VIF']>5]['Job Group'].unique().tolist()
    if len(high_vif)==0:
        st.success("All models have interpretable pay gaps")    
    else:
        st.error(docs.BAD_GAPS, icon="🚨")
        
    high_vif_coef = hug_coef.loc[hug_coef['VIF']>1.3]
    
    if high_vif_coef.shape[0] > 0:
        st.success("All models have interpretable pay gaps") 
    else:
        for jg, div in high_vif_coef[['Job Group','Variable']].values:
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
    
    if "jge" in st.session_state.keys():
        main()
    else:
        no_jge()