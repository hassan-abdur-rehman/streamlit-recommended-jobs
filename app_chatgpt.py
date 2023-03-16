import streamlit as st
import requests
import json

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
    return response.json()

def split_job_ids(comma_separated_ids):
    return comma_separated_ids.split(",")

text_input = st.text_input("Enter comma-separated jobIds", key="jobId")

if text_input:
    splitted_job_ids = split_job_ids(text_input)
    total = len(splitted_job_ids)

    for i in range(0, total):
        st.subheader(f"Job {i+1}: {splitted_job_ids[i]}")
        response_data = load_data(int(splitted_job_ids[i]))

        if "searchPayload" in response_data:
            st.write('Total received: ', response_data['totalReceived'])
            search_payload = response_data['searchPayload']

            job_id = st.text_input(f'Job {i+1} - jobId', search_payload['jobId'])
            required_skills = st.text_input(f'Job {i+1} - required_skills', search_payload['requiredSkills'])
            yoe = st.text_input(f'Job {i+1} - yoe', search_payload['yoe'])
            max_salary = st.text_input(f'Job {i+1} - max_salary', search_payload['maxSalary'])
            countries_include = st.text_input(f'Job {i+1} - countries_include', search_payload['countries']['include'])
            countries_exclude = st.text_input(f'Job {i+1} - countries_exclude', search_payload['countries']['exclude'])

            search_button = st.button(f'Search for Job {i+1}')

            if search_button:
                headers = { 
                    'Content-type': 'application/json'
                }

                payload = {
                    "jobId": int(job_id),
                    "requiredSkills": json.loads(required_skills),
                    "yoe": int(yoe),
                    "maxSalary": int(max_salary),
                    "countries": {
                        "include": json.loads(countries_include),
                        "exclude": json.loads(countries_exclude)
                    }
                }
                response = requests.post('https://developer-search.turing.com/api/search/hms-devs', data=json.dumps(payload), headers=headers)
                st.write(response.json())
        else:
            st.write(response_data)
