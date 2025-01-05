#to start the Server with Git Bash you have to type in: python -m streamlit run src/ui_main.py

import streamlit as st
from queries import find_devices
from devices import Device

from ui_device import ui_dev
from ui_users import ui_use
from ui_maintenance_management import ui_maintenance_manage
from ui_reservation_system import ui_reservation_sys



import streamlit as st

# Auswahl der Seite


page = st.sidebar.selectbox("Navigation", ["Geräte", "Nutzer", "Wartungsmanagement", "Reserviersystem"])
if page == "Geräte":
    ui_dev()


elif page == "Nutzer":
    ui_use()

elif page == "Wartungsmanagement":
    ui_maintenance_manage()

elif page == "Reserviersystem":
    ui_reservation_sys()


st.write("Session State:")
st.session_state