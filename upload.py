import streamlit as st
import pandas as pd
import time

# Page title
st.set_page_config(page_title='KHM Archiv Dashboard', page_icon='📁', layout="wide")
st.title('📁 KHM –> arkumu.nrw')

# Liste benötigter Dateien, die hochgeladen werden müssen um alle Funktionen des Dashboards zu nutzen
required_files = [
    "00_Projekte.csv",
    "01_Grundereignis.csv",
    "02_Kreuz_Projekte_Personen.csv",
    "03_Personen_Akteurinnen.csv",
    "04_Kreuz_Betreuende_Projekte.csv",
    "05_PersonenBetreuende.csv",
    "06_Auszeichnungen_Projekte.csv",
    "07_Kreuz_Projekte_Keywords.csv",
    "08_Keywords.csv",
    "09_Kreuz_Projekte_Informationsträger.csv",
    "10_PhysMedien_Informationstraeger.csv",
    "11_Kreuz_DigitaleObjekte_Proj.csv",
    "12_Media_DigitaleObjekte.csv",
    "16_Kreuz_Events_Projekte.csv",
    "17_Events_weitereEreignisse.csv",
    "18_Kreuz_Projekte_EquipmentSoftware.csv",
    "19_Equipment_und_Software.csv",
    "20_Equipmentart.csv",
    "21_PhysischesObjekt.csv"
]

# Initialisiere Session-State-Zähler
if "uploaded_files_count" not in st.session_state:
    st.session_state.uploaded_files_count = 0

# Multi-File-Upload
uploaded_files = st.sidebar.file_uploader(
    "Choose CSV files to upload", 
    accept_multiple_files=True, 
    type='csv'
)

# Funktion zum Einlesen der CSV Dateien in dfs
def read_csv_file(files, target_name, sep=";"):
    for file in files:
         if file.name == target_name:
            try:
                return pd.read_csv(file, sep=sep)
            except Exception as e:
                st.error(f"Fehler beim Lesen von '{file.name}': {e}")
                return None
            return None
         
# Funktion zur Pflichtfeldprüfung
def check_required_columns(df, required_columns, filename):
    missing_report = {}
    for col in required_columns:
        if col not in df.columns:
            missing_report[col] = "Spalte fehlt"
        else:
            missing_count = df[col].isnull().sum() + (df[col] == "").sum()
            if missing_count > 0:
                missing_report[col] = f"{missing_count} fehlende(r) Wert(e)"
    if missing_report:
        st.warning(f"🚩 Pflichtfeldprüfung für **{filename}**:")
        for col, msg in missing_report.items():
            st.write(f"- **{col}**: {msg}")
    else:
        st.success(f"✅ Alle Pflichtfelder in **{filename}** sind vollständig.")

if uploaded_files:
    # Success Meldung mit Zähler der hochgeladenen Dateien anzeigen
    if len(uploaded_files) > st.session_state.uploaded_files_count:
        new_files = len(uploaded_files) - st.session_state.uploaded_files_count
        alert = st.sidebar.success(f"{new_files} Datei(en) erfolgreich hochgeladen!", icon="✅")
        st.session_state.uploaded_files_count = len(uploaded_files)
        time.sleep(1.5)
        alert.empty()

    # 
    uploaded_names = [file.name for file in uploaded_files]
    missing_files = set(required_files) - set(uploaded_names)

    # Falls Dateien fehlen liste mir diese sortiert auf
    if missing_files:
        st.sidebar.warning(f"Es fehlen {len(missing_files)} Datei(en):")
        for missing in sorted(missing_files):
            st.sidebar.write(f"- {missing}")
    else:
        alert_all_upload_success = st.sidebar.success("Alle erforderlichen Dateien wurden erfolgreich hochgeladen", icon="✅")
        time.sleep(1.5)
        alert_all_upload_success.empty()

        # Dataframes aus CSV Dateien
        df_projekte = read_csv_file(uploaded_files, "00_Projekte.csv")
        df_ereignisse = read_csv_file(uploaded_files, "01_Grundereignis.csv")
        df_akteurinnen = read_csv_file(uploaded_files, "03_Personen_Akteurinnen.csv")
        df_keywords = read_csv_file(uploaded_files, "07_Kreuz_Projekte_Keywords.csv")
        df_media = read_csv_file(uploaded_files, "12_Media_DigitaleObjekte.csv")

        # ----- DASHBOARD BEGINNT HIER ----- #
        # Tabs definieren
        tabs = st.tabs(["Übersicht", "Projekte", "Akteur:innen", "Keywords"])

        # Tab 1 – Übersicht
        with tabs[0]:
            st.subheader("Übersicht")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Anzahl Projekte", len(df_projekte))
            with col2:
                st.metric("Anzahl Akteur:innen", len(df_akteurinnen))
            with col3:
                st.metric("Anzahl Dateien", len(df_media))
            
        # Tab 2 - Projekte
        with tabs[1]:
            st.subheader("Projekte")
            required_columns_projekte = ["Originaltitel", "Originaltitel_Sprache", "Projektart_calc", "Projektkategorien_arkumu"]
            check_required_columns(df_projekte, required_columns_projekte, "00_Projekte.csv")


        # Tab 3 – Akteur:innen
        with tabs[2]:
            st.subheader("Akteur:innen-Statistiken")


        # Tab 3 – Keywords
        with tabs[3]:
            st.subheader("Keyword-Statistiken")


         # ----- DASHBOARD ENDE ----- #

else:
    st.session_state.uploaded_files_count = 0
    st.info("Bitte lade die CSV-Dateien hoch.")
