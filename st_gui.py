import streamlit as st
from build_data import dic_process
# import pandas as pd
from main import *

header = st.container()
col1,col2 = st.columns([2,8])

with header:
    st.title('Natural Solution🌲: TES-LCA') 

with col2:
    st.markdown("**website:** [SEERG](https://cbe.osu.edu/bakshi-sustainable-engineering-research-group) **| contact:** xue.326@osu.com")




with open("template.zip", "rb") as fp:
    btn = st.download_button(
        label="Template Download 📁 (.zip)",
        data=fp,
        file_name="template.zip",
        mime="application/zip"
    )

uploaded_files = st.file_uploader("Choose input files: technology & intervention matrix, weighting vector, process information", accept_multiple_files=True)

num = 0
for upf in uploaded_files:
    if 'tech' in str(upf.name):
        dfA = pd.read_csv(upf, index_col=0)
        num += 1
    elif 'intv' in str(upf.name):
        dfD = pd.read_csv(upf, index_col=0)
        num += 1
    elif 'weight' in str(upf.name):
        wt = pd.read_csv(upf, index_col=0)
        num += 1
    elif 'process' in str(upf.name):
        # proc_xl = pd.read_excel(upf)
        proc_xl = pd.ExcelFile(upf)
        num += 1
    else:
        st.write('Rename files as required❗')

if num < 4 and num > 0:
    st.write('⚠️ Missing File ⚠️')

# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)
#     st.write(bytes_data)

# with open('myfile.csv') as f:
#    st.download_button('Download CSV', f)



ES_name = st.text_input('Name of ecosystem services 👇', 'carbon sequestration')

if st.button('Calculate 🖱️'):
    toy = dic_process(proc_xl)
    obj1 = LcaSystem(toy, dfA, dfD, wt)
    obj1.add_process(SP_info)
    res = obj1.tes_cal()
    fig = obj1.barplot(ES_name)
    st.plotly_chart(fig, use_container_width=True)

