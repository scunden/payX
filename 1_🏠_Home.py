import sys
sys.path.append("..")
import streamlit as st
import docs
from payequity.payequity import Audit, JobGroup, JobGroupEnssemble, Regressor


for k, v in st.session_state.items():
    st.session_state[k] = v

st.set_page_config(
    page_title="Talent Ai PayX",
    page_icon="🏠",
)
st.title('Talent Ai Pay Equity')

st.markdown("""---""") 
st.write(docs.WELCOME)
st.markdown("""---""")
st.subheader("🔑 Key Variables")
st.write(docs.KEY_VARIABLES)
st.subheader("🎲 Statistical Validation")
st.write(docs.VALIDATION)
st.subheader("🚨 Pay Gaps")
st.subheader("📊 Drivers of Pay")
st.subheader("🚩 Outliers")
st.markdown("""---""")
st.subheader("💊 Remediation")
st.subheader("🎯 Gap Exploration")
st.subheader("💸 Fair Pay Calculator")

# st.title("Home")
# st.sidebar.success("Select a page above.")

# st.session_state["df"] = pd.DataFrame()

# if "my_input" not in st.session_state:
#     st.session_state["my_input"] = ""

# my_input = st.text_input("Input a text here", st.session_state["my_input"])
# submit = st.button("Submit")
# if submit:
#     st.session_state["my_input"] = my_input
#     st.write("You have entered: ", my_input)