import streamlit as st
import pandas as pd
import time

# Page title
st.set_page_config(page_title='KHM Archiv Dashboard', page_icon='📁', layout="wide")
st.title('📁 Multi-File-CSV-Upload')

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
        st.sidebar.success("Alle erforderlichen Dateien wurden hochgeladen", icon="✅")

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
    
    # Tabs definieren
    tabs = st.tabs(["Übersicht", "Projekte", "Akteur:innen", "Keywords"])

    # Tab 1 – Übersicht
    with tabs[0]:
        st.subheader("Übersicht")

        df_projekte = read_csv_file(uploaded_files, "00_Projekte.csv")
        df_akteurinnen = read_csv_file(uploaded_files, "03_Personen_Akteurinnen.csv")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Anzahl Projekte", len(df_projekte.drop_duplicates()))
        with col2:
            st.metric("Anzahl Akteur:innen", len(df_akteurinnen.drop_duplicates()))
        


        if df_projekte is not None:
            st.metric("Anzahl Projekte", len(df_projekte.drop_duplicates()))
        else:
            st.info("Datei **01_Projekte.csv** nicht gefunden oder fehlerhaft.")

    # Tab 2 – Akteur:innen
    with tabs[1]:
        st.subheader("Akteur:innen-Statistiken")
        df_akteurinnen = read_csv_file(uploaded_files, "03_Personen_Akteurinnen.csv")
        if df_akteurinnen is not None:
            with col1:
                st.metric("Anzahl eindeutige Akteur:innen", len(df_akteurinnen.drop_duplicates()))
            with col2:
                st.metric("Anzahl eindeutige Akteur:innen", len(df_akteurinnen.drop_duplicates()))
        else:
            st.info("Datei **03_Personen_Akteurinnen.csv** nicht gefunden oder fehlerhaft.")

    # Tab 3 – Keywords
    with tabs[2]:
        st.subheader("Keyword-Statistiken")
        df_keywords = read_csv_file(uploaded_files, "07_Kreuz_Projekte_Keywords.csv")
        if df_keywords is not None:
            st.metric("Anzahl Keywords", len(df_keywords.drop_duplicates()))
            st.metric("Anzahl Keywords", len(df_keywords.drop_duplicates()))
        else:
            st.info("Datei **04_Projekte_Keywords.csv** nicht gefunden oder fehlerhaft.")



else:
    st.session_state.uploaded_files_count = 0
    st.info("Bitte lade die CSV-Dateien hoch.")










