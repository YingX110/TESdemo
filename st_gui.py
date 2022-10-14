from distutils.command.config import dump_file
import streamlit as st
from build_data import dic_process
# import pandas as pd
from main import *
import plotly.graph_objects as go

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



usmap = st.container()
with usmap:
    st.markdown('Explore Carbon Sequestration over US 🇺🇸 using **TES Framework**') 

s1,s2 = st.columns(2)

with s1:
    SPM = st.selectbox("Select Sharing Principle:", 
    ("Population", "GDP", "Inverse of GDP", "Area", "Emission"), 
    disabled=False)

with s2:
    SCALE = st.selectbox("Select scales:", 
    ("Local, National", "Local, Worldwide", "Local, National, Worldwide", "Direct downscaling (PB)"), 
    disabled=False)



mapdf = pd.read_csv('./data_inventory/mapdata.csv')

if SCALE != "Direct downscaling (PB)":
    df = mapdf[(mapdf.Scale == SCALE) & (mapdf.Method == 'TES') & (mapdf.SP == SPM)]
else:
    df = mapdf[(mapdf.Method == 'PB') & (mapdf.SP == SPM)]


df = df.T
df = df.iloc[3:, :]
df = df.reset_index()
df = df.set_axis(['code', 'supply'], axis=1, inplace=False)

map = px.choropleth(locations=df['code'], 
                    locationmode="USA-states", 
                    color=df['supply'].astype(float), 
                    range_color=(1e4,7e8),
                    color_continuous_scale="Blugrn",
                    scope="usa")


# map = go.Figure(data=go.Choropleth(
#     locations=df['code'], 
#     z = df['supply'].astype(float), 
#     locationmode = 'USA-states', 
#     colorscale = 'Blugrn',
#     colorbar_title = "ton CO2/yr"))

map.update_layout(
    title_text = 'Supply by each state in the U.S. (2016 data)',
    geo_scope='usa')

st.plotly_chart(map, use_container_width=True)

