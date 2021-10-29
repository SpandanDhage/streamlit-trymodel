import pandas as pd
import streamlit as st
import requests
import json
from PIL import Image
from streamlit_lottie import st_lottie
import numpy as np
from Viewtrigger import Views as v

st.set_page_config(layout="wide", page_title="रुची WebApp")
st.title("रुची WebApp")
st.markdown("_(Get started by creating New Account)_")

endpoint = "http://fastapi-trymodel-container:8080"

hide_menu_style = """
<style>
#MainMenu {visibility : hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_menu_style, unsafe_allow_html=True)


def viewMainOn():
    viewMain = v.viewMainOn()
    return viewMain


def loadLottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def loadLottieUrl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


st.balloons()

st.sidebar.subheader("New User Please Create Account")

with st.sidebar.expander("Login"):
    with st.form(key="loginForm"):
        username = st.text_input("Email Id")
        password = st.text_input("Password", type='password')
        data = {
            "username": username,
            "password": password
        }
        Login = st.form_submit_button("Login")


if Login or viewMainOn():
    if username != "" and password != "":
        response = requests.post(f"{endpoint}/login", data)
        if response.status_code == 200:

            img = Image.open("./app/Asset/fig1.jpg")
            st.image(img)

            st.sidebar.success("Logged in successfully !!")
            mainHead = st.header("My Site Version 1.0")

            col1, col2 = st.columns(2)
            col1.subheader(f"Welcome {(json.loads(response.text))['name']} !!")
            col1.markdown(f"Logged in with email id : **{username}**")

            with col1.form(key="ScoreForm"):
                Name = st.text_input("Name")
                sub = st.form_submit_button("Score")
            if sub and Name != "":
                score = np.random.randint(1, 100)
                col1.markdown(f"Your Score is {score}")

            with col2:
                helloRobo = loadLottieUrl("https://assets8.lottiefiles.com/packages/lf20_3vbOcw.json")
                st_lottie(helloRobo, key="helloRobo")
            st.subheader("Feedback")

            with st.form(key="feedBackForm"):
                st.markdown("_You can submit as many feedbacks as you like..._")
                feedbackTitle = st.text_input("Feedback about", max_chars=20)
                feedback = st.text_area("Please enter feedBack here", max_chars=80)
                Submit = st.form_submit_button("Submit")

            if Submit and feedback != "" and feedbackTitle != "":
                col3, col4 = st.columns([1, 8])
                with col3:
                    submitted = loadLottieUrl("https://assets7.lottiefiles.com/private_files/lf30_nrnx3s.json")
                    st_lottie(submitted, key="submitted", height=60, width=100)
                data = {
                    "title": feedbackTitle,
                    "body": feedback,
                    "userId": (json.loads(response.text))['name']
                }
                feedbackRes = requests.post(f"{endpoint}/addBlog", data=json.dumps(data))

                with col4:
                    st.success("Response successfully Submitted")
            elif Submit and feedback == "" and feedbackTitle == "":
                st.markdown("**Please enter proper Details ...**")

            with st.expander("My Feedbacks"):
                myfeedbacks = requests.get(f"{endpoint}/blog/{(json.loads(response.text))['name']}")
                if myfeedbacks.status_code == 404:
                    st.markdown(f"**{(json.loads(myfeedbacks.text))['detail']}**")
                else:
                    feedbacks=(json.loads(myfeedbacks.text))
                    df=pd.DataFrame(feedbacks, columns=['body', 'title', 'userId'])
                    df['Feedback By']=df.userId
                    df.drop('userId', axis=1, inplace=True)
                    df['Feedback']=df.body
                    df.drop('body', axis=1, inplace=True)
                    df['About']=df.title
                    df.drop('title', axis=1, inplace=True)
                    st.dataframe(df)

            with st.expander("All Other Feedbacks", expanded=True):
                myfeedbacks = requests.get(f"{endpoint}/blog")
                if myfeedbacks.status_code == 404:
                    st.markdown(f"**{(json.loads(myfeedbacks.text))['detail']}**")
                else:
                    feedbacks=(json.loads(myfeedbacks.text))

                    df=pd.DataFrame(feedbacks, columns=['body', 'title', 'userId'])
                    df['Given By']=df.userId
                    df.drop('userId', axis=1, inplace=True)
                    df['Feedback']=df.body
                    df.drop('body', axis=1, inplace=True)
                    df['About']=df.title
                    df.drop('title', axis=1, inplace=True)
                    st.dataframe(df)

        elif response.status_code == 404:
            st.sidebar.error(f"{(json.loads(response.text))['detail']}")
    elif Login:
        st.sidebar.warning("Enter valid Username and Password")

if not Login:
    helloRobo1 = loadLottieUrl("https://assets8.lottiefiles.com/packages/lf20_3vbOcw.json")
    st_lottie(helloRobo1, key="helloRobo1")


with st.sidebar.expander("Create Account", expanded=True):
    with st.form(key="createUser"):
        username = st.text_input("Name")
        email = st.text_input("Email")
        createPassword = st.text_input("Password", type='password')
        confirmPassword = st.text_input("Confirm Password", type='password')
        data = {
            "name": username,
            "email": email,
            "password": createPassword
        }
        createUsr = st.form_submit_button("Create User")

if createUsr:
    if createPassword != confirmPassword:
        st.sidebar.error("Passwords not Match")
    else:
        response = requests.post(f"{endpoint}/addUser", data=json.dumps(data))
        if response.status_code == 208:
            st.sidebar.warning(f"{(json.loads(response.text))['detail']}")
        elif response.status_code == 201:
            st.sidebar.success(f"Account successfully created")
        else:
            st.sidebar.error("Unable to create")
