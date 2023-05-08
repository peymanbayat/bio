# to run -> streamlit run main.py
import streamlit as st
import methods

st.set_option('deprecation.showfileUploaderEncoding', False)
# Introduction
st.title("Bioinformatic Armory Web App")
st.write("Use sidebar to change mode!")

# List of choices that will show on the sidebar
activities = ["Basic DNA Sequence Analysis", "Count Point Mutations",
              "Find motifs", "Find..."]

choice = st.sidebar.selectbox("Select activity", activities)


# Code for basic analysis and translation
if choice == "Basic DNA Sequence Analysis":
    methods.basic_DNA()
elif choice == "Count Point Mutations":
    methods.count_point_mut()
# Finds motifs, user has to input
elif choice == "Find motifs":
    methods.find_motifs()
elif choice == "Find...":
    st.subheader("TODO:...")
