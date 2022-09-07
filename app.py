import os
import cv2
import time
import requests
import datetime as dt
import numpy as np
# from turtle import onclick
import streamlit as st
from PIL import Image, ImageDraw
import json

import streamlit.components.v1 as components



st.set_page_config(
   page_title="Where Is Wally?",
   page_icon= '🖼️'
)
title = st.title("Where Is Wally?")

url = 'http://localhost:8000'
# url = 'https://lightwaldo2-bwi4mwxyya-ey.a.run.app'

### columns and rows ###
col1, col2, col3= st.columns(3)

### initialize state ###
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def callback():
    st.session_state.button_clicked = True


### image selection ###
uploaded_file = st.sidebar.file_uploader("Upload Your Wally Image", accept_multiple_files=False, type=["png", "jpg", "jpeg"])
if uploaded_file != None:
    image = Image.open(uploaded_file)
    st.session_state.orginal_image = st.image(image)
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
        if st.session_state.orginal_image == None:
            st.title("You Might Forgot To Upload Your Image")
        else:
            try:
                ### Using api to reach model ###
                title.title("Ai Is Working On It")
                start = dt.datetime.now()
                res = requests.post(url + "/upload_image", files={'img': img_bytes})
                ###
                bg_igm = st.markdown('''
                <style>
                body {
                background-image: url("https://htmlcolorcodes.com/assets/images/colors/grass-green-color-solid-background-1920x1080.png");
                background-size: cover;
                }
                </style>
                ''', unsafe_allow_html=True)
            except:
                pass
            try:
                for secs in range(0,999*60,+1):
                    #start = dt.datetime.now()
                    #title.title("Ai Is Working On It")
                    if res.status_code == 200:
                        sol = res.json()
                        st.session_state.sol = sol
                    else:
                        st.markdown("**Oops**, something went wrong 😓 Please try again.")
                        print(res.status_code, res.content)

                    mm, ss = secs//60, secs%60
                    #if ai_found == False:
                    #    amm, ass = secs//60, secs%60
                    ph_myself.metric("Your Time:", f"{mm:02d}:{ss:02d}")
                    #ph_ai.metric("Ai Time:", f"{amm:02d}:{ass:02d}")
                    time.sleep(1)
                    bg_igm.empty()
                    user_time = (f"You Found Wally at: {mm:02d}:{ss:02d}")

                    if sol != None :
                        ai_found = True
                        title.title("Where Is Wally?")

                    if ai_found == True:
                        time_sp = str(dt.datetime.now() - start).replace("0:", "" , 1).replace(".", ":")
                        st.session_state.against_ai_result = (f"Ai Found Wally in: {time_sp}")
                        ph_ai.empty()
                        ph_ai.subheader(st.session_state.against_ai_result)
                        # with col1.expander("Need Some Help?"):
                            # img_size = st.session_state.orginal_image.size
                            #if any of the cords is 0 it messes up but don't have time to solve it
                            # cord_x = sol[0][0]/img_size[0]
                            # cord_y = sol[0][1]/img_size[1]
                            # if cord_x < 0.37:
                            #     x = "Left"
                            # elif 0.37 <= cord_x < 0.53:
                            #     x = "Middle"
                            # else:
                            #     x = "Right"
                            # if cord_y < 0.37:
                            #     y = "Top"
                            # elif 0.37 <= cord_x < 0.53:
                            #     y = "Middle"
                            # else:
                            #     y = "Bottom"

                            # st.write(f"Maybe Try To Look Closely To The {y} {x}.")

                        with col3.expander("I Give Up!"):
                            heatmap = np.asarray(json.loads(sol))
                            data=np.array(image)
                            # data = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
                            xx, yy = np.meshgrid(np.arange(heatmap.shape[2]), np.arange(heatmap.shape[1]))
                            x = (xx[heatmap[0, :, :, 0] > 0.999])
                            y = (yy[heatmap[0, :, :, 0] > 0.999])
                            for i, j in zip(x, y):
                                y_pos = j * 3
                                x_pos = i * 3
                                cv2.rectangle(data, (x_pos, y_pos), (x_pos + 64, y_pos + 64), (0, 255, 0),2)
                            # data = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
                            st.image(data)


                        for secs in range(mm*60+ss,999*60,+1):
                            mm, ss = secs//60, secs%60
                            ph_myself.metric("Your Time:", f"{mm:02d}:{ss:02d}")
                            time.sleep(1)
                            user_time = (f"You Found Wally at: {mm:02d}:{ss:02d}")
                        ai_found = 3


            finally:
                st.session_state.against_ai_user_result = user_time
                #st.session_state.against_ai_result = (f"Ai Found Wally at: {amm:02d}:{ass:02d}")
    if bt2:
        try:
            ph_myself.subheader(st.session_state.against_ai_user_result)
            ph_ai.subheader(st.session_state.against_ai_result)
            st.session_state.orginal_image.empty()
            st.image(st.session_state.sol)

        except:
            st.title("Try To Start The Game First")

### against time ###

elif add_radio == "Against Time":
    bt1 = st.sidebar.button("Press To Start/Reset", key="a")
    ph_myself = col1.empty()
    ph_myself_conc = col3.empty()
    if 'against_time_result' not in st.session_state:
        st.session_state.against_time_result = None
    bt2 = col1.button("Found Wally", key="b")
    if bt1:
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
                        ### Using api to reach model ###
                        res = requests.post(url + "/upload_image", files={'img': img_bytes})
                        st.title("Time Is Up!")
                        if res.status_code == 200:
                            sol = res.content
                            #sol = [(1050,0),(1250,200)]
                            with col3.expander("Where is he?"):
                                heatmap = np.asarray(json.loads(sol))
                                data=np.array(image)
                                # data = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
                                xx, yy = np.meshgrid(np.arange(heatmap.shape[2]), np.arange(heatmap.shape[1]))
                                x = (xx[heatmap[0, :, :, 0] > 0.999])
                                y = (yy[heatmap[0, :, :, 0] > 0.999])
                                for i, j in zip(x, y):
                                    y_pos = j * 3
                                    x_pos = i * 3
                                    cv2.rectangle(data, (x_pos, y_pos), (x_pos + 64, y_pos + 64), (0, 255, 0),2)
                                    # data = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
                                st.image(data)
                                # draw = ImageDraw.Draw(st.session_state.orginal_image)
                                # draw.ellipse(xy= sol, fill = None , outline ='purple', width= 10)
                                # st.session_state.orginal_image.save("drawn_result.png")
                                # st.image(st.session_state.orginal_image)

                        else:
                            st.markdown("**Oops**, something went wrong 😓 Please try again.")
                            print(res.status_code, res.content)

            finally:
                st.session_state.against_time_result = sonsonuc
                st.session_state.against_time_spent = sonuc
    if bt2:
        try:
            if st.session_state.against_time_result != None:
                ph_myself_conc.subheader(st.session_state.against_time_result)
            if st.session_state.against_time_spent < 15:
                st.title("Wow, Excellent!")
            elif 15 <= st.session_state.against_time_spent <30:
                st.title("Good Job!")
            else:
                st.title("You can do better than that!")
        except:
            st.title("Try To Start The Game First")

components.html(
    """
<div data-role="imagemagnifier"
    data-magnifier-mode="glass"
    data-lens-type="circle"
    data-lens-size="200"
>
</div>
    """
)

# if st.checkbox('Magnifier'):
#     st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

### sidebar image ###
st.sidebar.image("./images/where-to-next-457477.png", use_column_width=True)
