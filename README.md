# zh-ch-appointment-checker

## Overview

This Python script checks for available time slots on a specified website and sends a notification if an earlier time slot is found compared to a predefined static date. The script periodically checks for new time slots every minute with a random offset.

## Prerequisites

- Python 3.6 or higher
- Requests library

## Installation

1. **Clone the repository or download the script file** to your local machine.

2. **Install the required Python package**:
    ```sh
    pip install requests
    ```

## Setup

1. **Set User Information for Notification**:
    - Replace `"your_email@example.com"` with your actual email.
    - Replace `"+1234567890"` with your actual phone number.
    ```python
    USER_EMAIL = "your_email@example.com"
    USER_NUMBER = "+1234567890"
    ```

2. **Set ZH Login Token**:
    - Replace `'your_login_token_here'` with your login token received from the migration office.
    ```python
    LOGIN_TOKEN = 'your_login_token_here'
    ```

3. **Set Notification API Details**:
    - Replace `'https://api.your_notificationapi.com/sender'` with your actual Notification API URL.
    - Replace `'your_notification_token_here'` with your actual Notification API token.
    ```python
    NOTIFICATION_URL = 'https://api.your_notificationapi.com/sender'
    NOTIFICATION_TOKEN = 'your_notification_token_here'
    ```

4. **Set Static Date**:
    - By default, the static date is set to 14 days from the current date.
    - If you need to adjust this date, you can modify the `STATIC_DATE` variable.
    ```python
    STATIC_DATE = datetime.now(timezone.utc) + timedelta(days=14)
    ```

## Usage

1. **Run the script**:
    ```sh
    python script_name.py
    ```

2. **Script Behavior**:
    - The script will check for available time slots every minute with a random offset between 0 to 45 seconds.
    - If an earlier time slot is found compared to the static date, a notification will be sent to the specified email and phone number.

## Example

Here's an example of how the script will output information:

- If an earlier slot is found (plus a notification via the notificationapi):
    ```plaintext
    Earliest available time slot: 2024-01-25T09:00:00+00:00
    Notification sent.
    ```

- If no earlier slot is found:
    ```plaintext
    There are no newer slots available.
    ```

## Customization

- **Change the checking interval**:
    - By default, the script runs every minute with an additional random offset.
    - You can adjust the sleep time in the main loop as needed.
    ```python
    time.sleep(60 + random.randint(0, 45))
    ```
