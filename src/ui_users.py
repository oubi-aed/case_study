#to start the Server with Git Bash you have to type in: python -m streamlit run src/ui_users.py

import streamlit as st
from queries import find_devices, store_user_data
from devices import Device

def ui_users():
    # Eine Überschrift der ersten Ebene
    st.write("# Nutzermanagement")

    # Auswahl der Aktion
    action = st.selectbox("Aktion auswählen", ["Nutzer anlegen", "Geräteauswahl"])

    if action == "Nutzer anlegen":
        st.write("## Neuen Nutzer anlegen")

        with st.form(key="new_user_form"):
            user_name = st.text_input("Nutzername")
            user_email = st.text_input("Email")
            user_role = st.selectbox("Rolle", ["Geräteverantwortlicher", "Reservierer"])

            # Every form must have a submit button.
            submitted = st.form_submit_button("Nutzer anlegen")
            if submitted:
                store_user_data(user_name, user_email, user_role)
                st.write(f"User {user_name} with email {user_email} and role {user_role} has been created.")

    elif action == "Geräteauswahl":
        st.write("## Geräteauswahl")

        # Eine Auswahlbox mit Datenbankabfrage, das Ergebnis wird in current_device gespeichert
        devices_in_db = find_devices()

        if devices_in_db:
            current_device_name = st.selectbox(
                'Gerät auswählen',
                options=devices_in_db, key="sbDevice")

            if current_device_name in devices_in_db:
                loaded_device = Device.load_data_by_device_name(current_device_name)
                if loaded_device:
                    st.session_state['current_device'] = loaded_device
                    st.write(f"Loaded Device: {loaded_device}")  # uses __str__ method
                else:
                    st.error("Device not found in the database.")

                with st.form(key="user_form"):
                    st.write(loaded_device.device_name)

                    text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
                    loaded_device.set_managed_by_user_id(text_input_val)  # Uses setter method

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        loaded_device.store_data()
                        st.write("Data stored.")
                        st.rerun()
            else:
                st.error("Selected device is not in the database.")
        else:
            st.write("No devices found.")
            st.stop()

    st.write("Session State:")
    st.session_state

ui_users()