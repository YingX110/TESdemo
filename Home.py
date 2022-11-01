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

st.markdown("<h1 style='text-align: center; color: white; font-size: 53px;'>Towards the Global Goal <br> for Nature </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 22px;'><q>As humans we are born of the Earth, <br> nourished by the Earth, <br> healed by the Earth</q></p>", unsafe_allow_html=True)

# st.sidebar.write(
#     f"This app shows how a Streamlit app can interact easily with a to read or store data."
# )