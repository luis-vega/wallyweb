import streamlit as st
from PIL import Image
import time

st.set_page_config()

uploaded_file = st.file_uploader("Upload your Wally image", accept_multiple_files=False, type=['png','jpg'])
if uploaded_file != None:
    # st.write("filename:", uploaded_file.name)
    image = Image.open(uploaded_file)
    st.image(image, caption='Can you find Wally in less than 2 minutes?')


    if st.button('Can our AI be faster'):
        ph = st.empty()
        N = int(0.1*60)
        for secs in range(N,0,-1):
            mm, ss = secs//60, secs%60
            ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        st.write('Yes it is')
