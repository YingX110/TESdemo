from distutils.command.config import dump_file
import base64
import streamlit as st
from build_data import format_process
from main import *
from plotmap import mapplot
from PIL import Image


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

# col1,col2 = st.columns([3,7])

# with col1:
#     st.image(
#         "https://github.com/YingX110/TESdemo/raw/interface/images/one.svg",
#         width=60,
#     )
# with col2:
#     st.markdown("<h3 class='calh3'>STEP 1: DEFINE</h3>", unsafe_allow_html=True)
#     st.markdown("<p class='step1'>Define the system boundary, functional unit and type of the system</p>", unsafe_allow_html=True)

st.markdown(
    '<div><img src="https://github.com/YingX110/TESdemo/raw/interface/images/one.svg" style="vertical-align: middle;" width="70px"/><span class="stp1" style="vertical-align: middle;"> &ensp; STEP 1: DEFINE VARIABLES</span></div>',
    unsafe_allow_html=True
)

st.markdown("")
col1,col2 = st.columns([5,5])

with col1:
    Type = st.selectbox("Type of the system", 
    ("LCA", "Unit process", "Goe-unit process"), disabled=False)
    AES = st.selectbox("Framework for assessment", 
    ("TES", "PB"), disabled=False)
with col2:
    ES_name = st.selectbox("Select the name of ecosystem services 🌱", 
    ("carbon sequestration", "water provision (in processing)"), disabled=False)
    SP_name = st.selectbox("Select the sharing principle", 
    ("demand", "gdp", "inverse of gdp", "area", "population"), disabled=False)

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