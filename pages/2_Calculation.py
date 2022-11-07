from distutils.command.config import dump_file
import base64
import streamlit as st
from build_data import format_process
from main import *
from plotmap import mapplot
from PIL import Image



# st.set_page_config(layout="wide")

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
    '<div><img src="https://github.com/YingX110/TESdemo/raw/interface/images/ONE.png" style="vertical-align: middle;" width="70px"/><span class="stp1" style="vertical-align: middle;"> &ensp; STEP 1: DEFINE VARIABLES</span></div>',
    unsafe_allow_html=True
)

st.markdown("")
col1,col2 = st.columns([5,5])

with col1:
    Type = st.selectbox("Type of the system", 
    ("LCA", "Unit process", "Geo-unit process"), disabled=False)
    AES_fw = st.selectbox("Framework for assessment", 
    ("TES", "PB"), disabled=False)
with col2:
    ES_name = st.selectbox("Select the name of ecosystem services 🌱", 
    ("carbon sequestration", "water provision (in processing)"), disabled=False)
    SP_name = st.selectbox("Select the sharing principle", 
    ("demand", "gdp", "inverse of gdp", "area", "population"), disabled=False)

st.text("")
st.text("")

st.markdown(
    '<div><img src="https://github.com/YingX110/TESdemo/raw/interface/images/TWO.png" style="vertical-align: middle;" width="70px"/><span class="stp1" style="vertical-align: middle;"> &ensp; STEP 2: UPLOAD SPREADSHEET</span></div>',
    unsafe_allow_html=True
)


col1,col2 = st.columns([6,4])

with col2:
    st.text("")
    st.text("")
    st.text("")
    with open("./user_input_data/template_new.zip", "rb") as fp:
        btn = st.download_button(
            label="Template Download 📁 (.zip)",
            data=fp,
            file_name="template.zip",
            mime="application/zip"
        )
    
with col1:
    uploaded_files = st.file_uploader("", accept_multiple_files=True) # this is a list
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


########################################
if process != []:
    toy = format_process(process)
    # for v in toy.values():
    #     v[ES_name]['SP name'] = SP_name

    # obj = LcaSystem(toy, dfA, dfD, wt, AES)
    # obj.add_process(SP_info)

    if Type != 'LCA':
        obj = LcaSystem(PDic=toy, AES=AES_fw)
        obj.add_process(SP_info)
        ls_vk = []
        ls_s = []
        ls_d = []
        ls_name = []
        for p in obj.processes:
            sup = p.supply[ES_name]
            dmd = p.EI[ES_name]
            Vk = (sup - dmd) / dmd
            ls_s.append(sup)
            ls_d.append(dmd)
            ls_vk.append(Vk)
            if Type == "Geo-unit process":
                ls_name.append(p.location)
            else:
                ls_name.append(p.name)
        data_up = pd.DataFrame({'Supply': ls_s, 'Demand':ls_d, 'Process': ls_name})
    else:
        obj = LcaSystem(toy, dfA, dfD, wt, AES_fw)
        obj.add_process(SP_info)
        res = obj.tes_cal()
        obj.vk_cal()
    

st.text("")
st.text("")

col1, col2, col3 = st.columns([5, 2, 3])

with col1:
    st.markdown(
    '<div><img src="https://github.com/YingX110/TESdemo/raw/interface/images/THREE.png" style="vertical-align: middle;" width="70px"/><span class="stp1" style="vertical-align: middle;"> &ensp; STEP 3: CALCULATE 👉</span></div>',
    unsafe_allow_html=True
    )


st.text("")

def changerange(lb, ub, pct):
    up_sign = ub / np.absolute(ub)
    lb_sign = lb / np.absolute(lb)
    newlb = lb * (1 - lb_sign * pct)
    newub = ub * (1 + up_sign * pct)
    return [newlb, newub]


if st.button('Click 🖱️'):
    if Type != 'LCA':
        barfig_up = px.bar(data_up, x="Process", y=['Supply', 'Demand'], barmode='group')
        barfig_up.update_layout(
            xaxis_title='System name',
            yaxis_title='ton CO<sub>2</sub>/FU',
        )
        ls_tmp = ls_s + ls_d
        # newrange = changerange(min(ls_tmp), max(ls_tmp), 0.05)
        # barfig_up.update(layout_yaxis_range = newrange)
        st.plotly_chart(barfig_up, use_container_width=True)
    else:
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



col1, col2 = st.columns([7,3])
with col2:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
    '<div><span style="vertical-align: middle;"> Founded by &ensp;</span><img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/NSF_logo.png" style="vertical-align: middle;" width="60px"/></div>',
    unsafe_allow_html=True
    )