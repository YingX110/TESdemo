from distutils.command.config import dump_file
import streamlit as st
from build_data_v2 import format_process
from main2 import *
from plotmap import mapplot



page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

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

mtx_num = 3 # A, D and Wt
process = []

for upf in uploaded_files:
    if 'process' in str(upf.name):
        p = pd.read_csv(upf, index_col=0)
        process.append(p)
    elif 'tech' in str(upf.name):
        dfA = pd.read_csv(upf, index_col=0)
        mtx_num -= 1
    elif 'intv' in str(upf.name):
        dfD = pd.read_csv(upf, index_col=0)
        mtx_num -= 1
    elif 'weight' in str(upf.name):
        wt = pd.read_csv(upf, index_col=0)
        mtx_num -= 1
    else:
        st.write('Rename files as required❗')

if mtx_num > 0:
    st.write('⚠️ Missing File ⚠️')
    
    # if 'tech' in str(upf.name):
    #     dfA = pd.read_csv(upf, index_col=0)
    #     num += 1
    # elif 'intv' in str(upf.name):
    #     dfD = pd.read_csv(upf, index_col=0)
    #     num += 1
    # elif 'weight' in str(upf.name):
    #     wt = pd.read_csv(upf, index_col=0)
    #     num += 1
    # elif 'process' in str(upf.name):
    #     dfpro = pd.read_csv(upf, index_col=0)
    #     process.append(dfpro)
    #     num += 1
    # else:
    #     st.write('Rename files as required❗')



ES_name = st.selectbox("Name of ecosystem services 👇", 
("carbon sequestration", "water provision (in processing)"), disabled=False)

if st.button('Calculate 🖱️'):
    toy = format_process(process)
    obj = LcaSystem(toy, dfA, dfD, wt)
    obj.add_process(SP_info)
    res = obj.tes_cal()
    # fig = obj.barplot(ES_name)
    # st.plotly_chart(fig, use_container_width=True)

    mapdf = pd.read_csv('mapdata1.csv')
    procloc = obj.get_location()
    SCALE = obj.SCALES[ES_name]
    SPM = obj.SPM[ES_name]

    fig2 = mapplot(mapdf, procloc, SPM, SCALE)
    st.plotly_chart(fig2, use_container_width=True)



