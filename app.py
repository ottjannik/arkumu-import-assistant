# app.py

import streamlit as st
import pandas as pd
import time
from config import required_files, required_columns, conditional_required_columns, validation_targets
from utils import read_csv_file, load_all_dataframes
from validation import check_required_columns_short, check_required_columns_detailed, check_conditional_required_columns
from views import plot_file_extension_distribution


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
            for missing in sorted(missing_files):
                st.markdown(f"- {missing}")

    else:
        # Dataframes aus CSV Dateien laden
        dfs = load_all_dataframes(uploaded_files, required_files)
        df_projekte = dfs.get("00_Projekte.csv")
        df_grundereignis = dfs.get("01_Grundereignis.csv")
        df_akteurinnen = dfs.get("03_Personen_Akteurinnen.csv")
        df_keywords = dfs.get("07_Kreuz_Projekte_Keywords.csv")
        df_media = dfs.get("12_Media_DigitaleObjekte.csv")

        # ----- DASHBOARD BEGINNT HIER ----- #
        # Tabs definieren
        tabs = st.tabs(["Übersicht", "Pflichtfeldprüfung", "Stats", "Keywords"])

        # Tab 1 – Übersicht
        with tabs[0]:
            st.subheader("Übersicht")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Anzahl Projekte", len(df_projekte), border=True)
            with col2:
                st.metric("Anzahl Akteur:innen", len(df_akteurinnen), border=True)
            with col3:
                st.metric("Anzahl Dateien", len(df_media), border=True)
            st.divider()

            st.subheader("Pflichtfelder")
            check_required_columns_short(df_projekte, required_columns["projekte"], "00_Projekte.csv")
            check_required_columns_short(df_grundereignis, required_columns["grundereignis"], "01_Grundereignis.csv")
            check_required_columns_short(df_akteurinnen, required_columns["akteurinnen"], "03_Personen_Akteurinnen.csv")
            
        # Tab 2 - Pflichtfeldprüfung
        with tabs[1]:
            st.subheader("Pflichtfeldprüfung")
            st.write("Hier kannst du die Pflichtfelder der hochgeladenen Dateien überprüfen.")

            # Prüfe alle Dateien auf Pflichtfelder
            for target in validation_targets:
                df = dfs.get(target["filename"])
                rule_key = target["rule_key"]

                # Required checks
                if "required" in target["checks"]:
                    check_required_columns_detailed(df, required_columns[rule_key], target["filename"])
               
                # Conditional checks
                if "conditional" in target["checks"]:
                    check_conditional_required_columns(df, conditional_required_columns[rule_key], target["filename"])
               

               
                # Uncomment if you have an 'either_or' check
#                if "either_or" in target["checks"]:
#                    check_either_or_columns(df, either_or_required_columns[rule_key], target["filename"])

            
        # Tab 3 – Sats
        with tabs[2]:
            st.subheader("Stats")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Anzahl Projekte", len(df_projekte), border=True)
                st.metric("Anzahl Akteur:innen", len(df_akteurinnen), border=True)
            with col2:
                st.metric("Anzahl Dateien", len(df_media), border=True)
            with col3:
                st.metric("Anzahl Dateien", len(df_media), border=True)

            st.divider()
            plot_file_extension_distribution(df_media)


        # Tab 3 – Keywords
        with tabs[3]:
            st.subheader("Keyword-Statistiken")
            
         # ----- DASHBOARD ENDE ----- #

else:
    st.session_state.uploaded_files_count = 0
    st.info("Bitte lade die benötigten CSV-Dateien hoch.")
    with st.sidebar.expander("📄 Benötigte CSV-Dateien", expanded=True):
        for file in sorted(required_files):
            st.markdown(f"- {file}")