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
     

set_bg_hack('images/nature.jpg')

