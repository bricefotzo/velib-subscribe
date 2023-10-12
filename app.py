import os
from dotenv import load_dotenv
import streamlit as st
from utils.ui import render_ui
from utils.helpers import trigger_github_action, convert_to_local_time
from db.mongo import add_user, add_or_update_preference, get_user_by_email


# Configuration
CITIES = ["Paris", "Aubervilliers", "Nanterre"]


def main():
    _ , station_name, time_slot, email, subscribe_button = render_ui(CITIES)
    local_time_slot = convert_to_local_time(time_slot)
    if subscribe_button:
        try:
            existing_user = get_user_by_email(email)
            if not existing_user:
                add_user(email, is_premium=False)
            add_or_update_preference(email, station_name, local_time_slot.strftime('%H:%M'))

            if trigger_github_action(email, station_name, local_time_slot):
                st.success(
                    f"Notification programmée pour {time_slot} à la station {station_name} pour l'adresse {email}!")
            else:
                st.error("Erreur lors du déclenchement de l'action GitHub.")

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
