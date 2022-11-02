from distutils.command.config import dump_file
import base64
import streamlit as st
from build_data_v2 import format_process
from main2 import *
from plotmap import mapplot



with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


st.markdown("<div class='calimg'><div class='caltext'><h1 class='calh1'>Nature's Solution: TES-LCA🌲</h1><p class='calp'>Including Nature's carrying capacity into assessment & design</p></div></div>", unsafe_allow_html=True)
def set_bg_hack(main_bg):

    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .calimg {{
             background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
             height: 50%;
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

col1,col2 = st.columns([6,4])

with col2:
    st.text("")
    st.text("")
    st.text("")
    with open("template.zip", "rb") as fp:
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
    else:
            st.write('Rename files❗')
# if mtx_num > 0:
#     st.write('⚠️ Missing File ⚠️')

st.text("")
st.text("")
ES_name = st.selectbox("Select the name of ecosystem services 👇", 
("carbon sequestration", "water provision (in processing)"), disabled=False)