#to start the Server with Git Bash you have to type in: python -m streamlit run src/ui_reservation_system.py

import streamlit as st
from queries import find_devices
from devices import Device
from datetime import datetime

def ui_reservation_system():

    # Eine Überschrift der ersten Ebene
    st.write("# Reservierungssystem")

    # Eine Überschrift der zweiten Ebene
    st.write("## Reserviere dein Gerät")

    # Eine Auswahlbox mit Datenbankabfrage, das Ergebnis wird in current_device gespeichert
    devices_in_db = find_devices()

    if devices_in_db:
        current_device_name = st.selectbox(
            'Gerät auswählen',
            options=devices_in_db, key="sbDevice_reservation")

        if current_device_name in devices_in_db:
            loaded_device = Device.find_by_attribute("device_name", current_device_name)
            if loaded_device:
                st.write(f"Loaded Device: {loaded_device}")
            else:
                st.error("Device not found in the database.")

            with st.form(key="reservation_form"):
                reserviert_fuer = st.text_input("Reserviert für:", value=loaded_device.reserved_by or "")
                loaded_device.set_reserved_by(reserviert_fuer)

                # Standardwerte für die Datumsauswahl setzen
                default_start = loaded_device.timeframe_device_reserved_start or datetime.today().date()
                default_end = loaded_device.timeframe_device_reserved_end or datetime.today().date()

                # Kalender für Start- und Enddatum
                timeframe_device_reservation_start = st.date_input("Reserviert von:", value=default_start, min_value=datetime.today().date())
                loaded_device.set_timeframe_device_reserved_start(timeframe_device_reservation_start)

                timeframe_device_reservation_end = st.date_input("Reserviert bis:", value=default_end, min_value=datetime.today().date())
                loaded_device.set_timeframe_device_reserved_end(timeframe_device_reservation_end)


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

ui_reservation_system()