#!/usr/bin/python3

import requests
import json
import argparse
import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

access_token = os.getenv("SURVEY_MONKEY_AT")
parse = argparse.ArgumentParser()
parse.add_argument("file", help="Filename of json file that contains survey content")
parse.add_argument("emails", help="File with list of emails")
args = parse.parse_args()

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def gmail_send_message(email,link):

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
     
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()
        message.set_content(f"This is an automated draft mail. {link}")
        message["To"] = f"{email}"
        message["From"] = "mmarcetic@griddynamics.com"
        message["Subject"] = "Automated Draft"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"Message Id: {send_message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None

    return send_message

def parse_questions(file):

    with open(file, 'r') as f:
        data = json.load(f)

    survey_name = list(data.keys())[0]

    questions = []
    answers = []

    for page_name, q in data[survey_name].items():
        page_info = {
            "title" : page_name,
            "position" : 1
        }

        for q_name, q_data in q.items():
            q_payload = {
                "Question_name" : q_name,
                "Description" : q_data["Description"],
                "Answers" : q_data["Answers"]
            }

            questions.append(q_payload["Description"])
            answers.append(q_payload["Answers"])

    return survey_name, questions, page_info, answers

def create_survey(survey_name):
    url = "https://api.surveymonkey.com/v3/surveys"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    payload = {
        "title": survey_name
    }

    response = requests.post(url,json=payload, headers=headers)

    if response.status_code == 201:
        data = response.json()
        return data['id']
    else:
        print(f"Request failed with status code: {response.status_code}")

def create_survey_page(survey_id, page_info):

    url = f"https://api.surveymonkey.com/v3/surveys/{survey_id}/pages"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    payload = page_info

    response = requests.post(url,json=payload, headers=headers)

    if response.status_code == 201:
        data = response.json()
        return data['id']
    else:
        print(f"Request failed with status code: {response.status_code}")

def create_page_with_question(survey_id, page_id, question, answer_list):
    url = f"https://api.surveymonkey.com/v3/surveys/{survey_id}/pages/{page_id}/questions"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    payload = {
        "headings": [
            {
                "heading": question
            }
        ],
        "family": "single_choice",
        "subtype": "vertical",
        "forced_ranking": False,
        "answers": {
            "choices": [{"text": answer} for answer in answer_list]
        }
    }
    print(payload)

    response = requests.post(url,json=payload, headers=headers)

    if response.status_code == 201:
        print(f"Question is created successfully")
    else:
        print(f"Request failed with status code: {response.status_code}")

def create_collectors(survey_id):

    url = f"https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    payload = {
        "type" : "weblink",
        "name" : "First-collector"
    }

    response = requests.post(url,json=payload, headers=headers)

    if response.status_code == 201:
        data = response.json()
        return data['id']
    else:
        print(f"Request failed with status code: {response.status_code}")

def get_collector(survey_id):

    url = f"https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors"

    headers = {
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        colector_id = data['data'][0]['id']
        return colector_id
    else:
        print(f"Request failed with status code: {response.status_code}")

def get_url(collector_id):

    url = f"https://api.surveymonkey.com/v3/collectors/{collector_id}"

    headers = {
    'Accept': "application/json",
    'Authorization': f"Bearer {access_token}"
    }

    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['url']
    else:
        print(f"Request failed with status code: {response.status_code}")

def read_emails_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            emails = file.readlines()
        emails = [email.strip() for email in emails]
        return emails
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

def main():

    survey_name,questions,page_info,answers = parse_questions(args.file)
    file_with_emails = args.emails

    id_survey = create_survey(survey_name)
    id_page = create_survey_page(id_survey, page_info)

    for question, answers_list in zip(questions, answers):
        create_page_with_question(id_survey,id_page,question,answers_list)

    create_collectors(id_survey)
    coll_id = get_collector(id_survey)
    link = get_url(coll_id)

    list_of_emails = read_emails_from_file(file_with_emails)
    for email in list_of_emails:
        gmail_send_message(email, link)

if __name__ == "__main__":
    main()


