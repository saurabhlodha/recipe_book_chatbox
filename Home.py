import streamlit as st

st.set_page_config(
    page_title="Find Recipes",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Title of the app
st.title("Find yourself a great recipe")

# Description
st.write("""
Look for recipes by adding the ingredients you like and have
""")

# Navigation buttons
if st.button("Check the List of Cuisines"):
    st.switch_page("pages/Cuisines.py")

# if st.button("About Us"):
#     st.switch_page("pages/About_Us.py")
#
# if st.button("Forum"):
#     st.switch_page("pages/Forum.py")
