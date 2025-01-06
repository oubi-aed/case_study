#to start the Server with Git Bash you have to type in: python -m streamlit run src/ui_maintenance_management.py

import streamlit as st
from queries import find_devices
from devices import Device


def ui_maintenance_management():

    # Eine Überschrift der ersten Ebene
    st.write("# Wartungsmanager")


    # Eine Auswahlbox mit Datenbankabfrage, das Ergebnis wird in current_device gespeichert
    devices_in_db = find_devices()

    if devices_in_db:
        #Dropdown Menü
        current_device_name = st.selectbox(
            'Gerät auswählen',
            options=devices_in_db, key="sbDevice_maintenance")
        
        #überprüft ob gültiges Gerät ausgewählt ist
        if current_device_name in devices_in_db:
            #ladet Objekt aus der Datenbank
            loaded_device = Device.find_by_attribute("device_name", current_device_name)
            #Ausgabe ob Objekt gefunden wurde oder nicht
            if loaded_device:
                st.write(f"Loaded Device: {loaded_device}")
            else:
                st.error("Device not found in the database.")

            #laden des Textfeldes für Verantwortlichen
            with st.form(key="device_form"):
                st.write(loaded_device.device_name)
                #in value wird basierend auf Datenbank der eingegebene Wert gespeichert
                text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
                #Aktualisiert das Gerätedatenobjekt mit dem neuen wert den der Benutzer eingegeben hat
                loaded_device.set_managed_by_user_id(text_input_val)

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

ui_maintenance_management()