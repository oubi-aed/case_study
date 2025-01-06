#to start the Server with Git Bash you have to type in: python -m streamlit run src/ui_reservation_system.py

import streamlit as st
from queries import find_devices
from devices import Device

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
                st.write(loaded_device.device_name)

                text_input_val = st.text_input("Reserviert für:", value=loaded_device.reserved_by)
                loaded_device.set_reserved_by(text_input_val)

                text_input_reservation_time = st.text_input("reserviert von bis (dd,mm,yyyy-dd,mm,yyyy)", value=loaded_device.timeframe_device_reserved)
                loaded_device.set_timeframe_device_reserved(text_input_reservation_time)


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

ui_reservation_system()