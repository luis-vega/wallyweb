import os
import cv2
import time
import requests
import numpy as np
from turtle import onclick
import streamlit as st
from PIL import Image, ImageDraw



st.set_page_config(
   page_title="Where Is Wally?",
   page_icon= '🖼️'
)
st.title("Where Is Wally?")

url = 'http://localhost:8000'

### columns and rows ###
col1, col2, col3= st.columns(3)

### initialize state ###
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def callback():
    st.session_state.button_clicked = True


### image selection ###
uploaded_file = st.sidebar.file_uploader("Upload your Wally image", accept_multiple_files=False, type=["png", "jpg", "jpeg"])
if uploaded_file != None:
    image = Image.open(uploaded_file)
    st.session_state.orginal_image = image
    st.image(image)
    img_bytes = uploaded_file.getvalue()
else:
    if 'orginal_image' not in st.session_state:
        st.session_state.orginal_image = None

### challenge selection###
add_radio = st.sidebar.radio(
    "What Would You Like To Play?",
    ("Against Ai" ,  "Against Time"))
        
if add_radio == "Against Time":
    timer_selection = st.sidebar.radio(
        "Select time",
        ("0:30  (Hard)" , "1:00  (Medium)","2:00  (Easy)"))
    if timer_selection == "0:30  (Hard)":
        timer = 0.5
    elif timer_selection == "1:00  (Medium)":
        timer = 1.0
    else:
        timer = 2.0


### against ai ###    
   
if add_radio == "Against Ai":
    bt1 = st.sidebar.button("Press To Start/Reset", key="a")
    ph_myself = col1.empty()
    ph_ai = col3.empty()
    ai_found = False
    if 'against_ai_result' not in st.session_state:
        st.session_state.result = None
    bt2 = col2.button("Found Wally", key="b")
    if bt1:
        try:
            ### Using api to reach model ###
            res = requests.post(url + "/upload_image", files={'img': img_bytes})
            ###
        except:
            pass
        if st.session_state.orginal_image == None:
            st.title("You Might Forgot To Upload Your Image")
        else:
            try:
                for secs in range(0,999*60,+1):
                    if res.status_code == 200:
                        ### Response from module ###
                        #sol = res.content
                        sol = [(1050,0),(1250,200)]
                    else:
                        st.markdown("**Oops**, something went wrong 😓 Please try again.")
                        print(res.status_code, res.content)

                    mm, ss = secs//60, secs%60    
                    if ai_found == False:
                        amm, ass = secs//60, secs%60
                    ph_myself.metric("Your Time:", f"{mm:02d}:{ss:02d}")
                    ph_ai.metric("Ai Time:", f"{amm:02d}:{ass:02d}")
                    time.sleep(1)
                    user_time = (f"You Found Wally at: {mm:02d}:{ss:02d}")
                    
                    if sol != None :
                        ai_found = True
                    
                    if ai_found == True:
                        st.session_state.against_ai_result = (f"Ai Found Wally at: {amm:02d}:{ass:02d}")
                        ph_ai.empty()
                        ph_ai.subheader(st.session_state.against_ai_result)
                        with col1.expander("Need Some Help?"):
                            st.write(f"Maybe Try To Look Closely At The {sol}")
                        with col3.expander("I Give Up!"):
                            #st.image()
                            draw = ImageDraw.Draw(st.session_state.orginal_image)
                            draw.ellipse(xy= sol, fill = None , outline ='purple', width= 10)
                            st.session_state.orginal_image.save("drawn_result.png")
                            st.image(st.session_state.orginal_image)

                        for secs in range(mm*60+ss,999*60,+1):
                            mm, ss = secs//60, secs%60
                            ph_myself.metric("Your Time:", f"{mm:02d}:{ss:02d}")
                            time.sleep(1)
                            user_time = (f"You Found Wally at: {mm:02d}:{ss:02d}")
                        ai_found = 3


            finally:
                st.session_state.against_ai_user_result = user_time
                st.session_state.against_ai_result = (f"Ai Found Wally at: {amm:02d}:{ass:02d}")    
    if bt2:
        ph_myself.subheader(st.session_state.against_ai_user_result)
        ph_ai.subheader(st.session_state.against_ai_result)
        
### against time ###

elif add_radio == "Against Time":
    bt1 = st.sidebar.button("Press To Start/Reset", key="a")
    ph_myself = col1.empty()
    ph_myself_conc = col3.empty()
    if 'against_time_result' not in st.session_state:
        st.session_state.against_time_result = None
    bt2 = col1.button("Found Wally", key="b")
    if bt1:
        try:
            ### Using api to reach model ###
            res = requests.post(url + "/upload_image", files={'img': img_bytes})
            ###
        except:
            pass
        if st.session_state.orginal_image == None:
            st.title("You Might Forgot To Upload Your Image")
        else:
            try:
                N = int(timer * 60)
                for secs in range(N,-1,-1):
                    mm, ss = secs//60, secs%60
                    ph_myself.metric("Time Left:", f"{mm:02d}:{ss:02d}")
                    time.sleep(1)
                    end = mm*60 + ss
                    sonuc = N - end
                    if sonuc%60 < 10:
                        sonsonuc = (f"You spent {sonuc//60}:0{sonuc%60}")
                        
                    else:
                        sonsonuc = (f"You spent {sonuc//60}:{sonuc%60}")
                    ph_myself_conc.text(sonsonuc)
                    if secs == 0:
                        st.title("Time Is Up!")
                        if res.status_code == 200:
                            ### Response from module ###
                            #sol = res.content
                            sol = [(1050,0),(1250,200)]
                            with col3.expander("Where is he?"):
                                #st.image()
                                draw = ImageDraw.Draw(st.session_state.orginal_image)
                                draw.ellipse(xy= sol, fill = None , outline ='purple', width= 10)
                                st.session_state.orginal_image.save("drawn_result.png")
                                st.image(st.session_state.orginal_image)
                            

                        else:
                            st.markdown("**Oops**, something went wrong 😓 Please try again.")
                            print(res.status_code, res.content)

            finally:
                st.session_state.against_time_result = sonsonuc
                st.session_state.against_time_spent = sonuc
    if bt2:
        ph_myself_conc.subheader(st.session_state.against_time_result)
        if st.session_state.against_time_spent < 15:
            st.title("Wow, Excellent!")
        elif 15 <= st.session_state.against_time_spent <30:
            st.title("Good Job!")
        else:
            st.title("You can do better than that!")



   


            
                        
                
                


### sidebar image ###
st.sidebar.image("/home/omerdondu/code/Krastro/wallyweb/images/where-to-next-457477.png", use_column_width=True)

