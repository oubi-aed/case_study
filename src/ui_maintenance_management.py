#to start the Server with Git Bash you have to type in: python -m streamlit run src/ui_maintenance_management.py

import streamlit as st
from queries import find_devices
from devices import Device
from maintenance_plan import MaintenancePlan


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
            with st.form(key="maintenance_form"):
                st.write(loaded_device.device_name)
                
                #st.write(f"Datum der ersten Wartung: {loaded_device.maintenance_plan.first_maintenance}")
                #st.write(f"Datum der nächsten Wartung: {loaded_device.maintenance_plan.next_maintenance}")
                #st.write(f"Wartungsintervall: {loaded_device.maintenance_plan._maintenance_interval}")
                #st.write(f"Wartungskosten: {loaded_device.maintenance_plan._maintenance_cost}")  
                #st.write(f"Wartungskosten: {loaded_device.maintenance_plan._maintenance_cost_per_quarter()}")              
                
                #nur für Frontend
                st.write(f"Datum der ersten Wartung: Morgen")
                st.write(f"Datum der nächsten Wartung: Morgen 2027")
                st.write(f"Wartungsintervall: 2 Jahre")
                st.write(f"Wartungskosten: teuer")
                st.write(f"Wartungskosten pro Quartal: sehr euer")

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