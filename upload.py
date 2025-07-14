import streamlit as st
import pandas as pd

# Page title
st.set_page_config(page_title='KHM Archiv Dashboard', page_icon='📁', layout="wide")
st.title('📁 Multi-File-CSV-Upload')

# Initialisiere Session-State-Zähler
if "uploaded_files_count" not in st.session_state:
    st.session_state.uploaded_files_count = 0

# Multi-File-Upload
uploaded_files = st.file_uploader(
    "Choose CSV files to upload", 
    accept_multiple_files=True, 
    type='csv'
)

if uploaded_files:
    # Success Meldung mit Zähler der hochgeladenen Dateien anzeigen
    if len(uploaded_files) > st.session_state.uploaded_files_count:
        new_files = len(uploaded_files) - st.session_state.uploaded_files_count
        st.toast(f"{new_files} Datei(en) erfolgreich hochgeladen!", icon="✅")
        st.session_state.uploaded_files_count = len(uploaded_files)

    # Erstelle eine Liste der Dateinamen als Auswahloptionen
    file_names = [file.name for file in uploaded_files]
    
    # Multiselect der Dateien
    selected_files = st.multiselect(
        "Select files to preview",
        options=file_names
    )
    
    # Zeige die ersten 5 Zeilen der DataFrames der ausgewählten Dateien
    for file in uploaded_files:
        if file.name in selected_files:
            st.write(f"**{file.name}**")
            try:
                df = pd.read_csv(file, sep=';')
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Fehler beim Lesen der Datei '{file.name}': {e}")

# Wenn keine Dateien mehr hochgeladen werden, Zähler zurücksetzen
else:
    st.session_state.uploaded_files_count = 0