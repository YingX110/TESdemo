from distutils.command.config import dump_file
import streamlit as st
from build_data_v2 import format_process
from main2 import *
from plotmap import mapplot


with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


st.markdown("<h1> Solutions with Nature🌲 <br> - TES-LCA</h1>", unsafe_allow_html=True)

# with col2:
#     st.markdown("**website:** [SEERG](https://cbe.osu.edu/bakshi-sustainable-engineering-research-group) **| contact:** xue.326@osu.com")


with open("template.zip", "rb") as fp:
    btn = st.download_button(
        label="Template Download 📁 (.zip)",
        data=fp,
        file_name="template.zip",
        mime="application/zip"
    )