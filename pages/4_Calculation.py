from distutils.command.config import dump_file
import base64
import streamlit as st
from build_data import format_process
from main import *
from plotmap import mapplot


st.set_page_config(layout="wide")

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


st.markdown("<div class='calimg'><div class='caltext'><h1 class='calh1'>Nature's Solution: TES-LCA</h1><p class='calp'>Including Nature's carrying capacity into assessment & design</p></div></div>", unsafe_allow_html=True)
def set_bg_hack(main_bg):

    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .calimg {{
             background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
             height: 100%;
             background-position: center;
             background-repeat: no-repeat;
             position: relative;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
     
set_bg_hack('images/nature.jpg')

# st.markdown("<h1 class='calh1'> Natural Solution: TES-LCA🌲</h1>", unsafe_allow_html=True)
st.text("")

col1,col2 = st.columns([5,5])

with col1:
    Type = st.selectbox("Type of the system", 
    ("LCA", "Unit process", "Goe-unit process"), disabled=False)
with col2:
    ES_name = st.selectbox("Select the name of ecosystem services 🌱", 
    ("carbon sequestration", "water provision (in processing)"), disabled=False)

st.text("")
st.text("")

col1,col2 = st.columns([6,4])

with col2:
    st.text("")
    st.text("")
    st.text("")
    with open("./user_input_data/template.zip", "rb") as fp:
        btn = st.download_button(
            label="Template Download 📁 (.zip)",
            data=fp,
            file_name="template.zip",
            mime="application/zip"
        )
    
with col1:
    uploaded_files = st.file_uploader("", accept_multiple_files=True)
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


st.text("")
st.text("")
st.text("")
if st.button('Calculate 🖱️'):
    toy = format_process(process)
    obj = LcaSystem(toy, dfA, dfD, wt)
    obj.add_process(SP_info)
    res = obj.tes_cal()
    obj.vk_cal()

    barfig = obj.barplot()
    barfig.update_layout(
        title="Environmental Impact & Ecological Threshold",
        xaxis_title='',
        yaxis_title='ton CO<sub>2</sub>/FU',
        legend_title="Process"
    )
    barfig.update_traces(width=0.5)
    
    coordfig = obj.coordinateplot(ES_name)

    st.plotly_chart(barfig, use_container_width=True)
    st.text("")
    st.plotly_chart(coordfig, use_container_width=True)