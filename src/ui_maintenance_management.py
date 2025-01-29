#to start the Server with Git Bash you have to type in: python -m streamlit run src/ui_maintenance_management.py

import streamlit as st
from queries import find_devices
from devices import Device
from maintenance_plan import MaintenancePlan
from datetime import datetime, timedelta

def get_next_maintenance_date(last_maintenance_date, maintenance_frequency):
    # Dummy implementation, replace with actual logic
    return last_maintenance_date + timedelta(days=365 // maintenance_frequency)

def calculate_quarterly_costs(maintenance_cost, maintenance_frequency):
    # Dummy implementation, replace with actual logic
    return maintenance_cost / 4

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
                
                # Ensure last_maintenance_date attribute exists
                if hasattr(loaded_device, 'last_maintenance_date') and loaded_device.last_maintenance_date:
                    try:
                        last_maintenance_date = datetime.strptime(loaded_device.last_maintenance_date, '%d.%m.%Y')
                        next_maintenance_date = get_next_maintenance_date(last_maintenance_date, int(loaded_device.maintenance_frequency))
                        st.write(f"Nächster Wartungstermin: {next_maintenance_date.strftime('%d.%m.%Y')}")

                        quarterly_costs = calculate_quarterly_costs(float(loaded_device.maintenance_cost), int(loaded_device.maintenance_frequency))
                        st.write(f"Wartungskosten pro Quartal: {quarterly_costs:.2f} EUR")
                    except ValueError:
                        st.error("Invalid date format for last maintenance date. Please use dd.mm.yyyy.")
                else:
                    st.error("Device does not have a last maintenance date.")

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