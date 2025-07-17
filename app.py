import streamlit as st
import pandas as pd
import time
from config import required_files, required_columns, conditional_required_columns
from utils import read_csv_file
from validation import check_required_columns_short, check_required_columns_detailed, check_conditional_required_columns

# Page title
st.set_page_config(page_title='KHM → arkumu.nrw', page_icon='📁', layout="wide")
st.title('📁 KHM → arkumu.nrw')



# Initialisiere Session-State-Zähler für hochgeladene Dateien
if "uploaded_files_count" not in st.session_state:
    st.session_state.uploaded_files_count = 0

# Multi-File-Upload
uploaded_files = st.sidebar.file_uploader(
    "Choose CSV files to upload", 
    accept_multiple_files=True, 
    type='csv'
)

if uploaded_files:
    # Success Meldung mit Zähler der hochgeladenen Dateien anzeigen
    if len(uploaded_files) > st.session_state.uploaded_files_count:
        new_files = len(uploaded_files) - st.session_state.uploaded_files_count
        alert = st.sidebar.success(f"{new_files} Datei(en) erfolgreich hochgeladen!", icon="✅")
        st.session_state.uploaded_files_count = len(uploaded_files)
        time.sleep(2)
        alert.empty()

    # Falls benötigte Dateien fehlen liste diese sortiert auf
    uploaded_names = [file.name for file in uploaded_files]
    missing_files = set(required_files) - set(uploaded_names)

    if missing_files:
        with st.sidebar.expander(f"❗ Es fehlen {len(missing_files)} Datei(en):", expanded=True):
            st.markdown("\n".join([f"- {missing}" for missing in sorted(missing_files)]))

    else:
        # alert_all_upload_success = st.sidebar.success("Alle erforderlichen Dateien wurden hochgeladen", icon="🎉")
        # time.sleep(1.5)
        # alert_all_upload_success.empty()

        # Dataframes aus CSV Dateien
        df_projekte = read_csv_file(uploaded_files, "00_Projekte.csv")
        df_grundereignis = read_csv_file(uploaded_files, "01_Grundereignis.csv")
        df_akteurinnen = read_csv_file(uploaded_files, "03_Personen_Akteurinnen.csv")
        df_keywords = read_csv_file(uploaded_files, "07_Kreuz_Projekte_Keywords.csv")
        df_media = read_csv_file(uploaded_files, "12_Media_DigitaleObjekte.csv")

        # ----- DASHBOARD BEGINNT HIER ----- #
        # Tabs definieren
        tabs = st.tabs(["Übersicht", "Pflichtfeldprüfung", "Akteur:innen", "Keywords"])

        # Tab 1 – Übersicht
        with tabs[0]:
            st.subheader("Übersicht")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Anzahl Projekte", len(df_projekte), border=True)
                st.metric("Anzahl Akteur:innen", len(df_akteurinnen), border=True)
            with col2:
                projekte_mit_projekt_nr = ((df_projekte["Projekt_Nr"].notnull()) & (df_projekte["Projekt_Nr"] != "")).sum()
                st.metric("Anzahl Projektnummern", projekte_mit_projekt_nr, border=True)
            with col3:
                st.metric("Anzahl Dateien", len(df_media), border=True)

            st.subheader("Pflichtfelder")
            check_required_columns_short(df_projekte, required_columns["projekte"], "00_Projekte.csv")
            check_required_columns_short(df_grundereignis, required_columns["grundereignis"], "01_Grundereignis.csv")
            
        # Tab 2 - Pflichtfeldprüfung
        with tabs[1]:
            st.subheader("Pflichtfeldprüfung")
            check_required_columns_detailed(df_projekte, required_columns["projekte"], "00_Projekte.csv")
            check_required_columns_detailed(df_grundereignis, required_columns["grundereignis"], "01_Grundereignis.csv")


            #'missing_conditional = check_conditional_required_columns(df_projekte, conditional_required_columns["projekte"])
            #if missing_conditional:
            #    st.error("Es fehlen bedingte Pflichtfelder:")
            #    for col, msg in missing_conditional.items():
            #        st.write(f"- {col}: {msg}")"""
            


        # Tab 3 – Akteur:innen
        with tabs[2]:
            st.subheader("Akteur:innen-Statistiken")


        # Tab 3 – Keywords
        with tabs[3]:
            st.subheader("Keyword-Statistiken")
            
         # ----- DASHBOARD ENDE ----- #

else:
    st.session_state.uploaded_files_count = 0
    st.info("Bitte lade die benötigten CSV-Dateien hoch.")
    with st.sidebar.expander("📄 Benötigte CSV-Dateien", expanded=True):
        st.markdown("\n".join([f"- {file}" for file in sorted(required_files)]))