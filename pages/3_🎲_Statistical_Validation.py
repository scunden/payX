import streamlit as st
import streamlit_ext as ste
import docs
import config
import numpy as np


st.set_page_config(
        page_title="Talent Ai PayX",
        page_icon="🎇",
    )

def main():
        
    jge = st.session_state['jge']
    st.title('Talent Ai Pay Equity')
    
    st.markdown("""---""") 
    
    st.header("🔢 Model Evaluation")
    summary = jge.audit.summary.copy()
    num_models = summary.shape[0]
    rejected = len(jge.rejected_jg)
    
    overfit_df = jge.audit.predictive_dof.copy()
    overfit_df = overfit_df.loc[overfit_df['Ratio']<config.DOF_THRESHOLD][['Job Group','Observations','Features','DoF', 'Ratio']]
    overfit = overfit_df['Job Group'].unique().tolist()
    
    good_perf = summary.loc[summary['MAPE']<=config.PERFORMANCE_THRESHOLD]['Job Group'].unique().tolist()
    poor_perf = summary.loc[summary['MAPE']>config.PERFORMANCE_THRESHOLD]['Job Group'].unique().tolist()
    
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
        st.dataframe(data=overfit_df,use_container_width=True)
        
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
    high_vif = hug_coef.loc[hug_coef['VIF']>config.VIF_THRESHOLD_PG]['Job Group'].unique().tolist()
    if len(high_vif)==0:
        st.success("All models have interpretable pay gaps")    
    else:
        st.error(docs.BAD_GAPS, icon="🚨")
        
    high_vif_gap = hug_coef.loc[hug_coef['VIF']>config.VIF_THRESHOLD_PG]
    
    if high_vif_gap.shape[0] > 0:
        st.success("All models have interpretable pay gaps") 
    else:
        for jg, div in high_vif_gap[['Job Group','Variable']].values:
            st.error('Error: Job group "{}" has an unreliable "{}" pay gap'.format(jg, div), icon="🚨")
        
    st.markdown("""---""") 
    
    st.header("🎯 Legitimate Factors Evaluation")
    predictive_coef = jge.audit.predictive_coef.copy()
    high_vif_pred = predictive_coef.loc[(predictive_coef['VIF']>config.VIF_THRESHOLD)]
    
    if high_vif_pred.shape[0]==0:
        st.success("All models have interpretable coefficients")    
    else:
        instances = high_vif_pred.shape[0]
        across_jg = high_vif_pred["Job Group"].unique().shape[0]
        st.warning('Warning: There are {} instances of unreliable coefficients across {} job groups'.format(
            instances, across_jg), icon="⚠️")
        st.markdown("""---""") 
        st.subheader("Unreliable Coefficients")
        display_vif(high_vif_pred.sort_values(by=['VIF'], ascending=False))
        st.markdown("""---""") 
        st.subheader("Correlations")
        view_correlation(high_vif_pred, jge)
        
    st.markdown("""---""") 


def display_vif(df):
    cols = [x for x in df.columns if x not in ['Significant','P>|t|']]
    st.dataframe(data=df[cols],use_container_width=True)

def display_correlation(corr, jg, var, feature):
    if feature is None:
        feature_corr = corr.loc[(corr["Job Group"]==jg)&(corr["Variable 1"]==var)].copy()
    else:
        feature_corr = corr.loc[(corr["Job Group"]==jg)&(corr["Variable 1"]==var)&(corr["Feature 1"]==feature)].copy()
        
    feature_corr = feature_corr.loc[(feature_corr['Variable 1']!=feature_corr['Variable 2'])]
    feature_corr["Absolute Correlation"] = np.abs(feature_corr.Correlation)
    feature_corr = feature_corr.loc[feature_corr['Absolute Correlation']>config.CORR_THRESHOLD].sort_values(by=['Absolute Correlation'], ascending=False)
    st.dataframe(data=feature_corr[[x for x in feature_corr if x!="Absolute Correlation"]],use_container_width=True)

def view_correlation(df, jge):
    
    corr = jge.audit.predictive_corr.copy()
    
    columns = st.columns(3)
    jg = columns[0].selectbox(label="Select Job Group", options=df["Job Group"].unique())
    
    options = df.loc[df['Job Group']==jg]['Variable'].unique()
    var = columns[1].selectbox(label="Select Variable", options=options)
    
    feature_options = df.loc[(df['Job Group']==jg)&(df['Variable']==var)]['Feature'].unique()
    
    if df.loc[(df['Job Group']==jg)&(df['Variable']==var)]['Feature'].isnull().values.any():
        feature_options=[]

    feature = columns[2].selectbox(label="Select Feature", options=feature_options)
    
    display_correlation(corr, jg, var, feature)
    
    

if __name__=="__main__":
    
    if "jge" in st.session_state.keys():
        main()
    else:
        st.error(docs.VAL_PLACEHOLDER, icon="🚨")