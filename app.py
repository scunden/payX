import streamlit as st
import payequity as pe
import pandas as pd
import plotly.express as px

def view_pay_gaps(df, x, y):
    fig = px.bar(df, x=x, y=y, orientation='h')
    fig.show()

def generate_divs(gender, eth, gender_min, eth_min, gender_ref, eth_ref):
    div_vars, div_min, div_ref = ({},{},{})
    for variable in [gender, eth]:
        if variable is not None:
            if variable==gender:
                div_vars.update({'GENDER':gender})
                div_min.update({'GENDER':gender_min})
                div_ref.update({'GENDER':gender_ref})
            elif variable==eth:
                div_vars.update({'ETHNICITY':gender})
                div_min.update({'ETHNICITY':gender_min})
                div_ref.update({'ETHNICITY':gender_ref})
    
    return div_vars, div_min, div_ref


def main ():
    st.title('Talent Ai Pay Equity')
    
    st.markdown("""---""") 
    df = pd.read_csv("data.csv")
    columns = [None]+[x for x in df.columns]

    # Key Variables
    st.header("⚙️ Identify Key Variables", anchor="keyvar")
    name = st.text_input(label="Please type in the name of your organization", placeholder="Company X")
    eeid = st.selectbox(label="Please select the variable corresponding to employee ID", options=columns, index=0)

    job_group_column = st.selectbox(label="Please select the variable corresponding to job groups", options=columns, index=0)
    job_groups = df[job_group_column].unique().tolist() if job_group_column is not None else None
    pay_component = st.selectbox(label="Please select the variable corresponding to the desired pay component", options=columns, index=0)
    key_variables = [eeid, job_group_column, pay_component]
    st.markdown("""---""") 

    # Diversities
    st.header("⚙️ Identify Diversities")
    st.subheader("Gender")

    gender_min_disabled, eth_min_disabled = (True, True)

    # Gender
    gender = st.selectbox(label="Please select the variable corresponding to gender (select 'None' if gender is not included in the analysis)", options=columns, index=0)
    gender_min_disabled = False if gender is not None else gender_min_disabled
    gender_options = [] if gender is None else df[gender].unique()
    gender_min = st.selectbox(label="Please select the minority feature for gender (select 'None' if gender is not included in the analysis)", options=gender_options, index=0, disabled=gender_min_disabled)
    gender_ref = st.selectbox(label="Please select the reference feature for gender (select 'None' if gender is not included in the analysis)", options=[x for x in gender_options if x != gender_min], index=0, disabled=gender_min_disabled)
    st.markdown("""---""") 
    

    # Ethnicity
    st.subheader("Ethnicity")
    eth = st.selectbox(label="Please select the variable corresponding to ethnicity (select 'None' if ethnicity is not included in the analysis)", options=columns, index=0)
    eth_min_disabled = False if eth is not None else eth_min_disabled    
    eth_options = [] if eth is None else df[eth].unique()  
    eth_min = st.selectbox(label="Please select the minority feature for ethnicity (select 'None' if ethnicity is not included in the analysis)", options=eth_options, index=0, disabled=eth_min_disabled)
    eth_ref = st.selectbox(label="Please select the reference feature for ethnicity (select 'None' if ethnicity is not included in the analysis)", options=[x for x in eth_options if x != eth_min], index=0, disabled=eth_min_disabled)
    
    # Generate dictionaries
    div_vars, div_min, div_ref = generate_divs(gender, eth, gender_min, eth_min, gender_ref, eth_ref)
    st.markdown("""---""") 

    # Predictive and Diagnostic vars
    st.header("⚙️ Select Legitimate Drivers of Pay")
    predictive_vars_options = [x for x in df.columns if x not in key_variables+[gender, eth]]
    predictive_vars = st.multiselect(label="Select legitimate variables that impact pay (do not include gender, race, ethnicity...)", options=predictive_vars_options)
    st.markdown("""---""") 

    try:
        if len(predictive_vars)>0:
            jge = pe.JobGroupEnssemble(
            df=df, 
            eeid=eeid, 
            pay_component=pay_component, 
            predictive_vars=predictive_vars, 
            diagnostic_vars=None, 
            iter_order=None,
            column_map=None, 
            column_map_inv=None, 
            div_vars=div_vars, 
            div_min=div_min, 
            div_ref=div_ref,
            name=name,
            job_group_column=job_group_column,
            headcount_cutoff=80
            )
            categorical = [x for x in [jge.column_map_inv[x] for x in jge.categorical] if x in predictive_vars]
            # PSet References
            st.subheader("Set References for All Job Groups")
            columns  = st.columns(2)
            specified = {}
            for i, var in enumerate(categorical):

                variable = columns[0].selectbox(label="Variable: {}".format(var), options=categorical, index=i,key=str(i)+var+'col0', disabled=True)
                references = df[var].unique()
                ref = columns[1].selectbox(label="Select reference", key=str(i)+var+'col2', options=references)
                specified.update({variable:ref})
            st.markdown("""---""") 
    except:
        st.warning('Error: Please verify that prior sections were correctly completed', icon="⚠️")

    if st.button('Run Analysis'):
        with st.spinner('Generating audit...'):
            jge.generate_job_groups()
            jge.set_overall_references(specified=specified)
            jge.run_regressions()
            jge.generate_audit()
            jge.audit.export_all(version='test')
        st.success('Audit ran and successfully exported!', icon="✅")

if __name__=="__main__":
    main()
