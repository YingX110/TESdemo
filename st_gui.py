import streamlit as st
import main

header = st.container()

with header:
    st.title('Nature Solution🌲: TES-LCA') 
    st.markdown("**website:** [SEERG](https://cbe.osu.edu/bakshi-sustainable-engineering-research-group) **| contact:** xue.326@osu.com")



with open("template.zip", "rb") as fp:
    btn = st.download_button(
        label="Input Data Template",
        data=fp,
        file_name="template.zip",
        mime="application/zip"
    )

uploaded_files = st.file_uploader("Choose input files: technology & intervention matrix, process information", accept_multiple_files=True)

num = 0
for upf in uploaded_files:
    if 'tech' in str(upf.name):
        dfA = upf
        num += 1
    elif 'intv' in str(upf.name):
        dfD = upf
        num += 1
    elif 'weight' in str(upf.name):
        wt = upf
        num += 1
    elif 'process' in str(upf.name):
        proc_xl = upf
        num += 1
    else:
        st.write('Check File Name❗')

if num < 5 and num > 0:
    st.write('⚠️ Missing File ⚠️')

# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)
#     st.write(bytes_data)

# with open('myfile.csv') as f:
#    st.download_button('Download CSV', f)



ES_name = st.text_input('Name of ecosystem services 👇', 'carbon sequestration')