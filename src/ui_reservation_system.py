import streamlit as st
from queries import find_devices
from devices import Device
from datetime import datetime

def ui_reservation_system():
    st.write("# Reservierungssystem")
    st.write("## Reserviere dein Gerät")

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
                default_start = datetime.today().date()
                default_end = datetime.today().date()

                timeframe_device_reservation_start = st.date_input("Reserviert von:", value=default_start, min_value=datetime.today().date())
                timeframe_device_reservation_end = st.date_input("Reserviert bis:", value=default_end, min_value=datetime.today().date())

                submitted = st.form_submit_button("Reservierung speichern")
                if submitted:
                    if loaded_device.is_reserved(timeframe_device_reservation_start, timeframe_device_reservation_end):
                        st.error("Das Gerät ist in diesem Zeitraum bereits reserviert.")
                    else:
                        loaded_device.add_reservation(reserviert_fuer, timeframe_device_reservation_start, timeframe_device_reservation_end)
                        loaded_device.store_data()
                        st.success("Reservierung erfolgreich gespeichert!")
                        st.rerun()
        else:
            st.error("Selected device is not in the database.")
    else:
        st.write("No devices found.")
        st.stop()

    st.write("Session State:")
    st.session_state

ui_reservation_system()