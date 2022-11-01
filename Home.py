import streamlit as st
import base64

def set_bg_hack(main_bg):

    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
     

set_bg_hack('images/nature2.jpg')

# st.markdown("<h1 style='text-align: center; color: white; font-size: 53px;'>Towards the Global Goal <br> for Nature </h1>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: center; color: white; font-size: 22px;'>
# <q>As humans we are born of the Earth, <br> nourished by the Earth, <br> healed by the Earth</q></p>", unsafe_allow_html=True)

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



st.markdown('<h1 class="homeh1">Towards the Global Goal <br> for Nature</h1>', unsafe_allow_html=True)
st.text('')
st.text('')
st.text('')
st.text('')
st.markdown('<p class="homep"><q>As humans we are born of the Earth, <br> nourished by the Earth, <br> healed by the Earth</q></p>', unsafe_allow_html=True)


col1,col2, col3 = st.columns(3)
with col2:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown('<a href="https://cbe.osu.edu/bakshi-sustainable-engineering-research-group" target="_blank" rel="noopener noreferrer" class="btn">Visit Us To Know More</a>', unsafe_allow_html=True)