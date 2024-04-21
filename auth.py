import streamlit as st
import time
from streamlit_oauth import OAuth2Component
import os
import base64
import json
from dotenv import load_dotenv
import extra_streamlit_components as stx
import datetime

load_dotenv(dotenv_path=".env.local")

# using the extra streamlit component to get cookies data
@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()

# function to get email from cookies, not using now
def get_email():
    cookie_manager = get_manager()
    st.write(cookie_manager)
    value = cookie_manager.get("email")
    return value
    
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "")
AUTHORIZE_ENDPOINT = os.getenv("AUTHORIZE_ENDPOINT", "")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT", "")
REVOKE_ENDPOINT = os.getenv("REVOKE_ENDPOINT", "")

#TODO - Fix this to handle for both - local and streamlit cloud deployment
if CLIENT_ID == "":
    CLIENT_ID = st.secrets["CLIENT_ID"]
if CLIENT_SECRET == "":
    CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
if REDIRECT_URI == "":
    REDIRECT_URI = st.secrets["REDIRECT_URI"]
if AUTHORIZE_ENDPOINT == "":
    AUTHORIZE_ENDPOINT = st.secrets["AUTHORIZE_ENDPOINT"]
if TOKEN_ENDPOINT == "":
    TOKEN_ENDPOINT = st.secrets["TOKEN_ENDPOINT"]
if REVOKE_ENDPOINT == "":
    REVOKE_ENDPOINT = st.secrets["REVOKE_ENDPOINT"]                    

def authenticate_user():

    cookie_manager = get_manager()
    cookies = cookie_manager.get_all()
    st.write(cookies)
    value = cookie_manager.get("email")
    
    if value != None and "auth" not in st.session_state :
        # st.session_state["auth"] = value
        st.write("Welcome " + value + "")
        # st.write("auth" in st.session_state)
        
        if st.button("Logout"):
            cookie_manager.delete("email")
            if "auth" in st.session_state:
                del st.session_state["auth"]
            st.session_state["auth"] = value
            # cookies["email"] = None
            # st.write("auth" in st.session_state)
            
            
    else:  
        if "auth" not in st.session_state:
            # create a button to start the OAuth2 flow
            if len(cookie_manager.cookies) != 0:
                st.write(len(cookie_manager.cookies))
                st.write("Login to save your answers (Warning: This feature is unreliable, save your answers locally.)")
                oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, REVOKE_ENDPOINT)
                result = oauth2.authorize_button(
                    name="Continue with Google",
                    icon="https://www.google.com.tw/favicon.ico",
                    redirect_uri=REDIRECT_URI,
                    scope="email",
                    key="google",
                    extras_params={"prompt": "consent", "access_type": "offline"},
                    use_container_width=True,
                )        
    
                if result:
                    # decode the id_token jwt and get the user's email address
                    id_token = result["token"]["id_token"]
                    # verify the signature is an optional step for security
                    payload = id_token.split(".")[1]
                    # add padding to the payload if needed
                    payload += "=" * (-len(payload) % 4)
                    payload = json.loads(base64.b64decode(payload))
                    email = payload["email"]
                    st.session_state["auth"] = email
                    st.write("cookie has been added")
                    # cookie_manager.set("email", email , expires_at=datetime.datetime(year=2026, month=2, day=2))
                    st.session_state["token"] = result["token"]
                    st.rerun()
        else:
            st.write("auth" in st.session_state)
            
            # Calculate expiry date
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=7)
            # setting email cookie here
            cookie_manager.set("email", st.session_state["auth"], expires_at=expiry_date)
            st.write("Welcome " + st.session_state["auth"] + "")
            if st.button("Logout"):
                cookie_manager.delete("email")
                # if "auth" in st.session_state:
                #     del st.session_state["auth"]
            # cookie_manager.set("email", st.session_state["auth"] , expires_at=datetime.datetime(year=2026, month=2, day=2))
