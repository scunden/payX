import streamlit as st
import payequity as pe
import pandas as pd
import streamlit_ext as ste

def generate_divs(gender, eth, gender_min, eth_min, gender_ref, eth_ref):
    div_vars, div_min, div_ref = ({},{},{})
    for variable in [gender, eth]:
        if variable != "":
            if variable==gender:
                div_vars.update({'GENDER':gender})
                div_min.update({'GENDER':gender_min})
                div_ref.update({'GENDER':gender_ref})
            elif variable==eth:
                div_vars.update({'ETHNICITY':eth})
                div_min.update({'ETHNICITY':eth_min})
                div_ref.update({'ETHNICITY':eth_ref})
    
    return div_vars, div_min, div_ref

def key_variables_section(df, columns):
    # Key Variables
    st.header("⚙️ Identify Key Variables")
    name = ste.text_input(label="Please type in the name of your organization", placeholder="Company X")
    eeid = ste.selectbox(label="Please select the variable corresponding to employee ID", 
                        options=columns, index=0, key='eeid')

    job_group_column = ste.selectbox(label="Please select the variable corresponding to job groups", 
                                    options=columns, index=0, key='job_group_column')
    job_groups = df[job_group_column].unique().tolist() if job_group_column != "" else None
    pay_component = ste.selectbox(label="Please select the variable corresponding to the desired pay component", 
                                 options=columns, index=0, key='pay_component')
    key_variables = [eeid, job_group_column, pay_component]
    
    if '' in key_variables:
        st.warning('Error: Please ensure all variables above are filled out', icon="⚠️")
    
    # st.session_state["name"] = name
    # st.session_state["eeid"] = eeid
    # st.session_state["job_group_column"] = job_group_column
    # st.session_state["job_groups"] = job_groups
    # st.session_state["pay_component"] = pay_component
    # st.session_state["key_variables"] = key_variables
    
    st.markdown("""---""") 
    return name, job_groups, key_variables
        
    

def diversities_section(df, columns):# Diversities
    st.header("⚙️ Identify Diversities")
    st.subheader("Gender")

    # Gender
    st.write("Leave the following fields blank if gender is not included in the analysis")
    gender = ste.selectbox(label="Please select the variable corresponding to gender ", 
                          options=columns, index=0,
                          key='gender'
                          )
    
    
    gender_options = [] if gender == "" else df[gender].unique().tolist()    
    gender_min_disabled = False if gender_options is not [] else True

    gender_min = ste.selectbox(label="Please select the minority feature for gender", 
                            options=gender_options, index=0
                            , disabled=gender_min_disabled
                            # ,key='gender_min_'
                            )
    gender_ref = ste.selectbox(label="Please select the reference feature for gender", 
                            options=[x for x in gender_options if x != gender_min], index=0
                            , disabled=gender_min_disabled
                            # ,key='gender_ref'
                            )
    
    st.markdown("""---""") 

    # Ethnicity
    st.subheader("Ethnicity")
    st.write("Leave the following fields blank if ethnicity is not included in the analysis")
    eth = ste.selectbox(label="Please select the variable corresponding to ethnicity", 
                       options=columns, index=0
                    #    , key='eth'
                       )
    
    eth_options = [] if eth == "" else df[eth].unique() 
    eth_min_disabled = False if eth is not [] else True    
     
    
    eth_min = ste.selectbox(label="Please select the minority feature for ethnicity", 
                           options=eth_options, index=0, disabled=eth_min_disabled,
                        #    key='eth_min'
                           )
    eth_ref = ste.selectbox(label="Please select the reference feature for ethnicity", 
                           options=[x for x in eth_options if x != eth_min], index=0, disabled=eth_min_disabled,
                        #    key='eth_ref'
                           )
    
    # Generate dictionaries
    div_vars, div_min, div_ref = generate_divs(gender, eth, gender_min, eth_min, gender_ref, eth_ref)
    
    if gender=='' and eth=='':
        st.warning('Error: Both gender and ethnicity cannot be blank', icon="⚠️")

    st.markdown("""---""")
    
    return gender, eth, div_vars, div_min, div_ref

def modelling_vars_section(df, name, key_variables, gender, eth, div_vars, div_min, div_ref):
    
    eeid, job_group_column, pay_component = key_variables
    # Predictive and Diagnostic vars
    st.header("⚙️ Select Legitimate Drivers of Pay")
    predictive_vars_options = [x for x in df.columns if x not in key_variables+[gender, eth]]
    predictive_vars = ste.multiselect(label="Select legitimate variables that impact pay", 
                                     options=predictive_vars_options, key="pred_vars")
    st.markdown("""---""") 
    disable_button = True
    jge = None

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
            
            columns  = st.columns(2)
            specified = {}
            
            st.subheader("Set References for All Job Groups")
                
            for i, var in enumerate(categorical):

                variable = columns[0].selectbox(label="Variable: {}".format(var), 
                                                options=categorical, index=i,key=str(i)+var+'col0', disabled=True)
                references = df[var].unique()
                ref = columns[1].selectbox(label="Select reference", key=str(i)+var+'col2', options=references)
                specified.update({variable:ref})
            
            st.markdown("""---""") 

    except:
        st.warning('Error: Please verify that prior sections were correctly completed', icon="⚠️")

    if st.button('Run Analysis'):
        with st.spinner('Generating audit...'):
            try:
                jge.generate_job_groups()
                jge.set_overall_references(specified=specified)
                jge.run_regressions()
                jge.generate_audit()
                jge.audit.export_all(version='test')
                st.session_state['jge'] = jge
                st.success('Audit ran and successfully exported!', icon="✅")
            except:
                st.warning('Error: Failed to run audit', icon="⚠️")
                
        
    return jge

def main():
    st.title('Talent Ai Pay Equity')
    
    st.markdown("""---""") 
    df = pd.read_csv("data.csv")
    
    columns = [""]+[x for x in df.columns]
    name, job_groups, key_variables = key_variables_section(df, columns)
    gender, eth, div_vars, div_min, div_ref =  diversities_section(df, columns)
    jge = modelling_vars_section(df, name, key_variables, gender, eth, div_vars, div_min, div_ref)
    
if __name__=="__main__":
    main()
