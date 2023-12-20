import streamlit as st
from streamlit_oauth import OAuth2Component
import os
import base64
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

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
    if "auth" not in st.session_state:
        # create a button to start the OAuth2 flow
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
            st.write(result)
            # decode the id_token jwt and get the user's email address
            id_token = result["token"]["id_token"]
            # verify the signature is an optional step for security
            payload = id_token.split(".")[1]
            # add padding to the payload if needed
            payload += "=" * (-len(payload) % 4)
            payload = json.loads(base64.b64decode(payload))
            email = payload["email"]
            st.session_state["auth"] = email
            st.session_state["token"] = result["token"]
            st.rerun()
    else:
        st.write("Welcome " + st.session_state["auth"] + "")
        #st.write(st.session_state["token"])
        if st.button("Logout"):
            del st.session_state["auth"]
            del st.session_state["token"]