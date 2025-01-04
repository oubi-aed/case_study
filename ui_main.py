#to start the Server with Git Bash you have to type in: python -m streamlit run ui_main.py

import streamlit as st
from queries import find_devices
from devices import Device

# Eine Überschrift der ersten Ebene
st.write("# Geräterverwaltung")

# Eine Überschrift der zweiten Ebene
st.write("## Geräteauswahl")

#erstellen der Buttons

button  = st.button("Geräte")
if button: 
    #weiterleitung auf ui_device

button = st.button("Nutzer")
if button:
    #weiterleitung auf ui_users

button = st.button("Wartungsmanagement")
if button:
    #weiterleitung auf ui_maintenance_manager

button = st.button("Reserviersystem")
if button:
    #weiterleitung auf ui_reservation_system



st.write("Session State:")
st.session_state