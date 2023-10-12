import smtplib
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime
import requests
from api.external import get_dataset_info
from settings import EMAIL_USER, EMAIL_PASS, GITHUB_TOKEN


def send_email(subject: str, message: str, recipient: str) -> bool:
    """
    Send an email using Gmail

    Args:
        subject (str): Email subject
        message (str): Email message
        recipient (str): Email recipient

    Returns:
        None
    """

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = recipient

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_PASS, recipient, msg.as_string())
        return True
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        return False


def notify_user(email: str, station_name: str) -> bool:
    """
    Send email to the user with the station info

    Args:
        email (str): User email
        station_name (str): Station name

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        station_data = get_dataset_info("velib-disponibilite-en-temps-reel", where=f'name like "{station_name}"')[0]
    except IndexError:
        print(f"Station {station_name} not found.")
        return False

    date = datetime.now().strftime("%H:%M")
    message = (
        f"Info pour la station: {station_data['name']} à {date}\n"
        "----------------------\n"
        f"Places disponibles: {station_data['numdocksavailable']}/{station_data['capacity']}\n\n"
        f"Vélos disponibles\n"
        f"Mécanique: {station_data['mechanical']}\n"
        f"Électrique: {station_data['ebike']}\n"
    )

    return send_email("Your Vélib Station Update", message, email)


def trigger_github_action(email: str, station_name: str, time_slot: datetime) -> bool:
    """
    Trigger the GitHub action to send the email

    Args:
        email (str): User email
        station_name (str): Station name
        time_slot (datetime): Notification time

    Returns:
        bool: True if the GitHub action was triggered successfully, False otherwise.
    """

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.everest-preview+json",
    }
    data = {
        "event_type": "notify-user",
        "client_payload": {
            "email": email,
            "station": station_name,
            "time": time_slot.strftime("%H:%M")
        },
    }

    try:
        response = requests.post(
            "https://api.github.com/repos/bricefotzo/velib-subscribe/dispatches",
            headers=headers,
            json=data,
            timeout=10,
        )
        return response.status_code == 204
    except Exception as e:
        print(f"An error occurred while triggering GitHub action: {e}")
        return False


def results_to_df(results: list[dict]) -> pd.DataFrame:
    """
    Convert the API results to a Pandas DataFrame

    Args:
        results (list[dict]): API results

    Returns:
        pd.DataFrame: Pandas DataFrame
    """
    df = pd.DataFrame(results)
    df["lat"] = df["coordonnees_geo"].apply(lambda x: x.get("lat"))
    df["lon"] = df["coordonnees_geo"].apply(lambda x: x.get("lon"))
    return df
