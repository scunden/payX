import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Talent Ai PayX",
    page_icon="🏠",
)

st.title("Home")
st.sidebar.success("Select a page above.")

st.session_state["df"] = pd.DataFrame()

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered: ", my_input)