import streamlit as st
from persist import persist, load_widget_state
import pandas as pd
import payequity as pe


def page_home():
    st.title('Talent Ai Pay Equity')
    
    st.markdown("""---""") 
    st.session_state["df"] = pd.read_csv("data.csv")
    st.session_state["columns"] = [None]+[x for x in st.session_state["df"].columns]

def key_variables_page():
    # Key Variables
    df = st.session_state["df"].copy()
    columns = st.session_state["columns"]
    
    st.header("⚙️ Identify Key Variables", anchor="keyvar")
    name = st.text_input(label="Please type in the name of your organization", 
                         placeholder="Company X", key=persist("name"))
    eeid = st.selectbox(label="Please select the variable corresponding to employee ID", 
                        options=columns, index=0, key=persist("eeid"))
    job_group_column = st.selectbox(label="Please select the variable corresponding to job groups", 
                                    options=columns, index=0, key=persist("job_group_column"))
    job_groups = df[job_group_column].unique().tolist() if job_group_column is not None else None
    pay_component = st.selectbox(label="Please select the variable corresponding to the desired pay component", 
                                 options=columns, index=0, key=persist("pay_component"))
    key_variables = [eeid, job_group_column, pay_component]
    
    st.session_state["key_variables"] = key_variables
    st.markdown("""---""") 

def generate_divs(gender, eth, gender_min, eth_min, gender_ref, eth_ref):
    div_vars, div_min, div_ref = ({},{},{})
    for variable in [gender, eth]:
        if variable is not None:
            if variable==gender:
                div_vars.update({'GENDER':gender})
                div_min.update({'GENDER':gender_min})
                div_ref.update({'GENDER':gender_ref})
            elif variable==eth:
                div_vars.update({'ETHNICITY':eth})
                div_min.update({'ETHNICITY':eth_min})
                div_ref.update({'ETHNICITY':eth_ref})
    
    return div_vars, div_min, div_ref

def diversity_page():
    
    df = st.session_state["df"].copy()
    columns = st.session_state["columns"]
    
    st.header("⚙️ Identify Diversities")
    st.subheader("Gender")

    gender_min_disabled, eth_min_disabled = (True, True)

    # Gender
    gender = st.selectbox(label="Please select the variable corresponding to gender (select 'None' if gender is not included in the analysis)", 
                          options=columns, index=0, 
                          key=persist("gender")
                          )
    gender_min_disabled = False if gender is not None else gender_min_disabled
    gender_options = [] if gender is None else df[gender].unique()
    
    gender_min = st.selectbox(label="Please select the minority feature for gender (select 'None' if gender is not included in the analysis)", 
                              options=gender_options, index=0, disabled=gender_min_disabled,
                              key='gender_min_',
                            #   key=persist("gender_min_")
                              )
    gender_ref = st.selectbox(label="Please select the reference feature for gender (select 'None' if gender is not included in the analysis)", 
                              options=[x for x in gender_options if x != gender_min], 
                              index=0, disabled=gender_min_disabled,
                            #   key=persist("gender_ref_")
                              )
    st.markdown("""---""") 
    

    # Ethnicity
    st.subheader("Ethnicity")
    eth = st.selectbox(label="Please select the variable corresponding to ethnicity (select 'None' if ethnicity is not included in the analysis)", 
                       options=columns, index=0, 
                       key=persist("eth")
                       )
    eth_min_disabled = False if eth is not None else eth_min_disabled    
    eth_options = [] if eth is None else df[eth].unique()  
    eth_min = st.selectbox(label="Please select the minority feature for ethnicity (select 'None' if ethnicity is not included in the analysis)", 
                           options=eth_options, index=0, disabled=eth_min_disabled, 
                        #    key=persist("eth_min_")
                           )
    eth_ref = st.selectbox(label="Please select the reference feature for ethnicity (select 'None' if ethnicity is not included in the analysis)", 
                           options=[x for x in eth_options if x != eth_min], 
                           index=0, disabled=eth_min_disabled, 
                        #    key=persist("eth_ref_")
                           )
    
    # Generate dictionaries
    div_vars, div_min, div_ref = generate_divs(gender, eth, gender_min, eth_min, gender_ref, eth_ref)
    st.session_state["div_vars"] = div_vars
    st.session_state["div_min"] = div_min
    st.session_state["div_ref"] = div_ref
    
    st.markdown("""---""") 

def predictive_vars_page():
    # Predictive and Diagnostic vars
    st.header("⚙️ Select Legitimate Drivers of Pay")
    predictive_vars_options = [x for x in st.session_state["df"] .columns if x\
        not in st.session_state["key_variables"] +[st.session_state["gender"], st.session_state["eth"]]]
    
    st.session_state["predictive_vars"] = st.multiselect(label="Select legitimate variables that impact pay (do not include gender, race, ethnicity...)", 
                                     options=predictive_vars_options, key=persist("predictive_vars_"))
    st.markdown("""---""") 
    

    try:
        if len(st.session_state["predictive_vars"])>0:
            jge = pe.JobGroupEnssemble(
            df=st.session_state["df"], 
            eeid=st.session_state["eeid"], 
            pay_component=st.session_state["pay_component"], 
            predictive_vars=st.session_state["predictive_vars"], 
            diagnostic_vars=None, 
            iter_order=None,
            column_map=None, 
            column_map_inv=None, 
            div_vars=st.session_state["div_vars"], 
            div_min=st.session_state["div_min"], 
            div_ref=st.session_state["div_ref"],
            name=st.session_state["name"],
            job_group_column=st.session_state["job_group_column"],
            headcount_cutoff=80
            )
            categorical = [x for x in [jge.column_map_inv[x] for x in jge.categorical] if x in st.session_state["predictive_vars"]]
            # PSet References
            st.subheader("Set References for All Job Groups")
            columns  = st.columns(2)
            specified = {}
            for i, var in enumerate(categorical):

                variable = columns[0].selectbox(label="Variable: {}".format(var), 
                                                options=categorical, index=i,key=persist(str(i)+var+'col0'), disabled=True)
                references =st.session_state["df"][var].unique()
                ref = columns[1].selectbox(label="Select reference", key=persist(str(i)+var+'col2'), options=references)
                specified.update({variable:ref})
            st.markdown("""---""") 
            
            if st.button('Run Analysis'):
                jge.generate_job_groups()
                jge.set_overall_references(specified=specified)
                jge.run_regressions()
                jge.generate_audit()
                jge.audit.export_all(version='test')
    except:
        st.warning('Error: Please verify that prior sections were correctly completed', icon="⚠️")

PAGES = {
    "home": page_home,
    "key variables": key_variables_page,
    "diversity": diversity_page,
    "predictive variables": predictive_vars_page,
}

def main():
    page = st.sidebar.radio("Select your page", tuple(PAGES.keys()), format_func=str.title)
    PAGES[page]()
    

if __name__ == "__main__":
    load_widget_state()
    main()