import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
NMS_API_KEY = os.getenv('NMS_API_KEY')
OTPMS_KEY = os.getenv('OTPMS_KEY')
NMS_BASE_URL = os.getenv('NMS_BASE_URL')
OTPMS_BASE_URL = os.getenv('OTPMS_BASE_URL')



def interact_with_microservice(base_url, endpoint, method='GET', data=None, additional_headers=None):
    """
    Common function to interact with microservices.
    Returns a tuple containing (data, error_message, status_code).
    """
    
    url = f"{base_url}{endpoint}"
    print("url",url)
    default_headers = {'Content-Type': 'application/json', 'Accept': '*/*'}
    
    # Merge default headers with additional headers if provided
    headers = {**default_headers, **(additional_headers or {})}

    try:
        response = requests.request(method, url, data=data, headers=headers)
        return response.json()
    except requests.RequestException as e:
        error_message = f"Error interacting with microservice: {e}"
        error_response = {
            "status":"error",
            "message":error_message,
            "StatusCode":6001

        }
        return error_response


def generate_otp_with_otpms(otp_type, user_id):
    additional_headers = {'Authorization': OTPMS_KEY}
    response_data = interact_with_microservice(
        OTPMS_BASE_URL,
        'generate-otp',
        method='POST',
        data=json.dumps({"otpType": str(otp_type), "userID": int(user_id)}),
        additional_headers=additional_headers
    )
    return response_data


def verify_otp_with_otpms(key, otp):
    additional_headers = {'Authorization': OTPMS_KEY}
    response_data = interact_with_microservice(
        OTPMS_BASE_URL,
        'verify-otp',
        method='POST',
        data=json.dumps({"key": str(key), "otp": str(otp)}),
        additional_headers=additional_headers
    )
    return response_data


def send_nms_sms(phone_number, message):
    additional_headers = {'Authorization': NMS_API_KEY}
    response_data = interact_with_microservice(
        NMS_BASE_URL,
        'send-sms',
        method='POST',
        data=json.dumps({"phone_number": phone_number, "message": message}),
        additional_headers=additional_headers
    )
    return response_data