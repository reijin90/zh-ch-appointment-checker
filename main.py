import requests
from datetime import datetime, timezone, timedelta
import time
import random

# User info for notification
USER_EMAIL = "your_email@example.com"
USER_NUMBER = "+1234567890"

# ZH Login
LOGIN_TOKEN = 'your_login_token_here'

# Notification API
NOTIFICATION_URL = 'https://api.your_notificationapi.com/sender'
NOTIFICATION_TOKEN = 'your_notification_token_here'

# Static date for comparison (defaults to today + 14 days)
# If an earlier appointment date was found it will send a notification. See example for a fixed time
STATIC_DATE = datetime.now(timezone.utc) + timedelta(days=14)
# STATIC_DATE = datetime.strptime('30.01.2024', '%d.%m.%Y').replace(tzinfo=utc_plus_one)

def check_time_slots(user_email, user_number):
    LOGIN_URL = 'https://www.zh.ch/proxy/migek/login'
    TIMESLOT_URL = 'https://www.zh.ch/proxy/migek/api/v1/timeslots/?days=7'

    login_headers = {
        'Accept': 'application/hal+json;charset=UTF-8',
        'Content-Type': 'application/json',
    }

    timeslot_headers = {
        'Accept': 'application/hal+json;charset=UTF-8',
    }

    notification_headers = {
        'Authorization': 'Basic ' + NOTIFICATION_TOKEN,
        'Content-Type': 'application/json',
    }

    login_payload = {
        'token': LOGIN_TOKEN
    }

    response = requests.post(LOGIN_URL, headers=login_headers, json=login_payload)
    response.raise_for_status()

    token_data = response.json()
    token = token_data['token']

    timeslot_headers['Authorization'] = f'Bearer {token}'

    response = requests.get(TIMESLOT_URL, headers=timeslot_headers)
    response.raise_for_status()

    timeslots_data = response.json()
    timeslots = timeslots_data.get('timeSlots', [])

    earliest_slot = None
    for slot in timeslots:
        if slot['capacity'] > 0:
            slot_time = datetime.fromisoformat(slot['startTime'].replace('Z', '+00:00'))
            if earliest_slot is None or slot_time < earliest_slot:
                earliest_slot = slot_time

    if earliest_slot and earliest_slot < STATIC_DATE:
        print(f"Earliest available time slot: {earliest_slot.isoformat()}")
        notification_payload = {
            "notificationId": "zh_timeslots",
            "user": {
                "id": user_email,
                "email": user_email,
                "number": user_number
            },
            "mergeTags": {
                "earliest_slot": earliest_slot.isoformat()
            }
        }
        notification_response = requests.post(NOTIFICATION_URL, headers=notification_headers, json=notification_payload)
        notification_response.raise_for_status()
        print("Notification sent.")
    else:
        print("There are no newer slots available.")

# Main loop to run the script every minute with a random offset
if __name__ == "__main__":
    while True:
        check_time_slots(USER_EMAIL, USER_NUMBER)
        time.sleep(60 + random.randint(0, 45))
