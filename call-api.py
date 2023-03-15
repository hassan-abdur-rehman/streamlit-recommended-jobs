import streamlit as st
import requests
import json

st.title("""This App can tell the params being used and developers who will be recommended a job""")

# st.write("""Please press enter after applying jobId""")

def load_data(text_input):
    headers = { 
        'service-account-token': '1|DAa7x9wnCGNjk9uwzDmMC8kI4ppg1GxY',
        'Content-type': 'application/json'
    }
    payload = {
        "jobId": int(text_input),
        "options": { 
            "forceRefresh": False, 
            "skipRecommendation": True, 
            "includeSearchPayloadInResponse": True, 
            "includeDevelopersInResponse": True, 
            "useSpreadSheetForRates": True 
        } 
    }
    response = requests.post('https://matching.turing.com/api_/recommended-jobs', data=json.dumps(payload), headers=headers)
    return response

text_input = st.text_input("jobId", key="jobId")
if text_input:
    data = load_data(text_input)
    st.write(data.json())
# You can access the value at any point with:


