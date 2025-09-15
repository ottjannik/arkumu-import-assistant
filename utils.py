# =============================================================
# utils.py
# Diese Datei enthält Hilfsfunktionen, die in verschiedenen Teilen der Anwendung zum Laden
# von Konfigurationen, Verarbeiten von Dateiuploads und Extrahieren von DataFrames benutzt werden.
# =============================================================

import streamlit as st
import io
import time
import pandas as pd

def handle_file_upload(required_files, selected_profile):
    """Funktion zum Hochladen von Dateien über die Sidebar.
    Zeigt eine Erfolgsmeldung an, wenn Dateien hochgeladen werden,
    und überprüft, ob alle erforderlichen Dateien vorhanden sind.

    Args:
        required_files (list): Liste der erforderlichen Dateinamen.
        selected_profile (str): Name des ausgewählten Profils, um spezifische Konfigurationen zu laden.
    Returns:
        list: Liste der hochgeladenen Dateien oder None, wenn nicht alle erforderlichen Dateien vorhanden
    """
    files = st.sidebar.file_uploader(
        "CSV-Dateien:",
        accept_multiple_files=True,
        type='csv'
    )

    if not files:
        st.session_state.uploaded_files_count = 0
        st.info("Bitte lade alle erforderlichen Dateien hoch, um fortzufahren.")
        with st.sidebar.expander(f"📄 Erforderliche CSV-Dateien ({selected_profile}):", expanded=False):
            for file in sorted(required_files):
                st.markdown(f"- {file}")
            return None

    if files:
        if len(files) > st.session_state.get("uploaded_files_count", 0):
            new_files = len(files) - st.session_state.get("uploaded_files_count", 0)
            alert = st.sidebar.success(f"{new_files} Datei(en) erfolgreich hochgeladen!", icon="✅")
            st.session_state.uploaded_files_count = len(files)
            time.sleep(2)
            alert.empty()

        uploaded_names = [file.name for file in files]
        missing_files = set(required_files) - set(uploaded_names)
        if missing_files:
            st.info("Bitte lade alle erforderlichen Dateien hoch, um fortzufahren.")
            st.sidebar.error(
            "❗ Es fehlen folgende Dateien:\n" +
            "\n".join(f"- {file}" for file in sorted(missing_files))
            )
            return None
        return files
    return None


def read_csv_file(files, target_name, sep=";"):
    """Funktion zum Lesen einer CSV-Datei aus den hochgeladenen Dateien.
    Args:
        files (list): Liste der hochgeladenen Dateien.
        target_name (str): Name der zu lesenden Datei.
        sep (str): Trennzeichen für die CSV-Datei, Standard ist ';'.
    Returns:
        pd.DataFrame: DataFrame der gelesenen CSV-Datei oder None, wenn die Datei nicht gefunden wurde oder ein Fehler auftrat.
    """
    for file in files:
         if file.name == target_name:
            try:
                return pd.read_csv(file, sep=sep)
            except Exception as e:
                st.error(f"Fehler beim Lesen von '{file.name}': {e}")
                return None
            return None


def load_all_dataframes(uploaded_files, required_files):
    """Funktion zum Laden aller erforderlichen DataFrames aus den hochgeladenen Dateien.
    Args:
        uploaded_files (list): Liste der hochgeladenen Dateien.
        required_files (list): Liste der erforderlichen Dateinamen.
    Returns:
        dict: Dictionary mit DataFrames, wobei die Schlüssel die Dateinamen sind.
    """
    dfs = {}
    for file_name in required_files:
        df = read_csv_file(uploaded_files, file_name)
        if df is not None:
            dfs[file_name] = df
    return dfs


def extract_named_dataframes(dfs, validation_targets):
    """Funktion zum Extrahieren und Benennen von DataFrames basierend auf den Validierungszielen,
    welche in den configs definiert sind.
    Args:
        dfs (dict): Dictionary mit DataFrames, wobei die Schlüssel die Dateinamen sind.
        validation_targets (list): Liste der Validierungsziele, die die DataFrame-Schlüssel enthalten.
    Returns:
        dict: Dictionary mit benannten DataFrames, wobei die Schlüssel die DataFrame-Schlüssel sind.
    """
    named_dfs = {}
    for target in validation_targets:
        df_key = target["df_key"]     # z.B. "projekte"
        filename = target["filename"] # z.B. "00_Projekte.csv"
        if filename in dfs:
            named_dfs[df_key] = dfs[filename]
    return named_dfs

def create_error_report(validation_results, validation_targets):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for df_key, result in validation_results.items():
            filename = validation_targets[df_key]["filename"]

            for rule_name, res in result.items():
                if not res["ok"]:  # nur Fehler speichern
                    sheet_name = f"{filename[:20]}_{rule_name}"  # Sheetname max. 31 Zeichen
                    df_errors = res["errors"]

                    df_errors.to_excel(writer, sheet_name=sheet_name, index=False)

                    # Worksheet holen und Spaltenbreite anpassen
                    worksheet = writer.sheets[sheet_name]
                    for i, col in enumerate(df_errors.columns):
                        max_len = max(
                            df_errors[col].astype(str).map(len).max(),
                            len(str(col))
                        ) + 2  # etwas Puffer
                        worksheet.set_column(i, i, max_len)

    output.seek(0)
    return output