import streamlit as st
import requests
import json
from ast import literal_eval

st.title("""This App can tell the params being used and developers who will be recommended a job""")

def load_data(job_id):
    headers = { 
        'service-account-token': '1|DAa7x9wnCGNjk9uwzDmMC8kI4ppg1GxY',
        'Content-type': 'application/json'
    }
    payload = {
        "jobId": job_id,
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

def split_job_ids(comma_separated_ids):
    comma_separated_str = comma_separated_ids.split(",")
    return comma_separated_str

def on_search_click(job_id, required_skills, yoe, max_salary, countries_include, countries_exclude):
    headers = { 
        'Content-type': 'application/json'
    }
    st.write("required_skills", literal_eval(required_skills))
    st.write("required_skills", required_skills)

    st.write("jobId", type(job_id))
    st.write("jobId", int(job_id))

    payload = {
        "jobId": int(job_id),
        "requiredSkills": literal_eval(required_skills),
        "yoe": int(yoe),
        "maxSalary": int(max_salary),
        "countries": {
            "include": literal_eval(countries_include),
            "exclude": literal_eval(countries_exclude)
        }
    }
    response = requests.post('https://developer-search.turing.com/api/search/hms-devs', data=json.dumps(payload), headers=headers)

    st.write(response.json())
    # return response

text_input = st.text_input("jobId", key="jobId")
if text_input:
    splitted_job_ids = split_job_ids(text_input)
    total = len(splitted_job_ids)
    list = st.tabs(splitted_job_ids)
    
    for i in range(0, total):
        with list[i]:
            response = load_data(int(splitted_job_ids[i]))
            # list[i].write(data.json())

            if "searchPayload" in response.json():
                data = response.json()
                st.write('Total received: ', data['totalReceived'])
                search_payload = data['searchPayload']
                job_id = st.text_input('jobId', search_payload['jobId'])
                required_skills = required_skills = st.text_input('required_skills', search_payload['requiredSkills'])
                yoe = yoe = st.text_input('yoe', search_payload['yoe'])
                max_salary = st.text_input('max_salary', search_payload['maxSalary'])
                countries_include = st.text_input('countries_include', search_payload['countries']['include'])
                countries_exclude = st.text_input('countries_exclude', search_payload['countries']['exclude'])
            else:
                list[i].write(response.json())
                # search_again_button = st.button('Search Again', on_click=on_search_click, args=(job_id, required_skills, yoe, max_salary, countries_include, countries_exclude))
                # search_again_button.on_click(on_search_click, job_id = int(splitted_job_ids[i]), required_skills = required_skills, yoe = yoe, max_salary = max_salary)

    
    
# You can access the value at any point with:


