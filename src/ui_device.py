#to start the Server with Git Bash you have to type in: python -m streamlit run src/ui_device.py

import streamlit as st
from queries import find_devices
from devices import Device

def ui_device():

    # Eine Überschrift der ersten Ebene
    st.write("# Gerätemanagement")

    # Auswahl der Aktion
    action = st.selectbox("Aktion auswählen", ["Gerät anlegen/ändern", "Geräteauswahl"])

    if action == "Gerät anlegen/ändern":
        st.write("## Neues Gerät anlegen oder bestehendes Gerät ändern")

        with st.form(key="device_form"):
            device_name = st.text_input("Gerätename")
            device_type = st.text_input("Gerätetyp")
            device_manager = st.text_input("Geräteverantwortlicher")
            last_maintenance_date = st.text_input("Letztes Wartungsdatum (dd.mm.yyyy)")
            maintenance_cost = st.text_input("Wartungskosten")
            maintenance_frequency = st.text_input("Wartungsfrequenz (z.B. 1 oder 2 mal im Jahr)")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Gerät speichern")
            if submitted:
                new_device = Device(device_name, device_manager, last_maintenance_date, maintenance_cost, maintenance_frequency)
                new_device.store_data()
                st.write(f"Device {device_name} has been saved.")

    elif action == "Geräteauswahl":
        st.write("## Geräteauswahl")

        # Eine Auswahlbox mit Datenbankabfrage, das Ergebnis wird in current_device gespeichert
        devices_in_db = find_devices()

        if devices_in_db:
            current_device_name = st.selectbox(
                'Gerät auswählen',
                options=devices_in_db, key="sbDevice_dev")

            if current_device_name in devices_in_db:
                loaded_device = Device.find_by_attribute("device_name", current_device_name)
                if loaded_device:
                    st.write(f"Loaded Device: {loaded_device}")
                else:
                    st.error("Device not found in the database.")

                with st.form(key="update_device_form"):
                    st.write(loaded_device.device_name)

                    text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
                    loaded_device.set_managed_by_user_id(text_input_val)

                    last_maintenance_date = st.text_input("Letztes Wartungsdatum (dd.mm.yyyy)", value=loaded_device.last_maintenance_date)
                    loaded_device.last_maintenance_date = last_maintenance_date

                    maintenance_cost = st.text_input("Wartungskosten", value=loaded_device.maintenance_cost)
                    loaded_device.maintenance_cost = maintenance_cost

                    maintenance_frequency = st.text_input("Wartungsfrequenz (z.B. 1 oder 2 mal im Jahr)", value=loaded_device.maintenance_frequency)
                    loaded_device.maintenance_frequency = maintenance_frequency

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        loaded_device.store_data()
                        st.write("Data stored.")
                        st.rerun()
        else:
            st.write("No devices found.")
            st.stop()

    st.write("Session State:")
    st.session_state

ui_device()