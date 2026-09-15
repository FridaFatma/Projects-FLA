import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SHEET_URL = "https://docs.google.com/spreadsheets/d/1aiOOaoXg_Yo00xh-X5A29W3NlfAm0xWq5nNYB1a-co4/edit?usp=sharing"

@st.cache_data(ttl=1800)
def get_sheet_data(worksheet_name):
    creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"])
        dict(st.secrets["gcp_service_account"]), scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_url(SHEET_URL).worksheet(worksheet_name)
    return pd.DataFrame(sheet.get_all_records())
