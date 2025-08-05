import pandas as pd
import streamlit as st
import os
from collections import Counter
from validation import (
    check_required_columns_short,
    check_required_columns_detailed,
    check_conditional_required_columns,
)
from config import required_columns, conditional_required_columns, validation_targets

def render_overview_tab(df_projekte, df_akteurinnen, df_media, df_grundereignis):
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


def render_validation_tab(dfs):
    st.subheader("Pflichtfeldprüfung")
    st.write("Hier kannst du die Pflichtfelder der hochgeladenen Dateien überprüfen.")

    for target in validation_targets:
        df = dfs.get(target["filename"])
        rule_key = target["rule_key"]

        if "required" in target["checks"]:
            check_required_columns_detailed(df, required_columns[rule_key], target["filename"])

        if "conditional" in target["checks"]:
            check_conditional_required_columns(df, conditional_required_columns[rule_key], target["filename"])

        # Optional: if "either_or" in target["checks"]:
        #     check_either_or_columns(df, either_or_required_columns[rule_key], target["filename"])


def render_stats_tab(df_projekte, df_akteurinnen, df_media):
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


def render_keywords_tab():
    st.subheader("Keyword-Statistiken")
    st.info("Noch keine Visualisierung vorhanden.")

#
def plot_file_extension_distribution(df_media):
    st.subheader("Dateiendungen")

    if "Dateipfad_absolut" not in df_media.columns:
        st.error("Die Spalte 'Dateipfad_absolut' fehlt in der Datei.")
        return

    # Dateiendungen extrahieren
    file_extensions = df_media["Dateipfad_absolut"].dropna().apply(
        lambda x: os.path.splitext(x)[-1].lower().lstrip(".")
    )

    # Medienkategorien definieren
    video_exts = {"mp4", "mov", "avi", "mkv", "wmv", "flv", "mpeg", "webm"}
    image_exts = {"jpg", "jpeg", "png", "gif", "tiff", "bmp", "webp"}

    # Filteroption
    filter_option = st.selectbox("Medien-Typ filtern", ["Alle", "Nur Videos", "Nur Bilder"])

    if filter_option == "Nur Videos":
        file_extensions = file_extensions[file_extensions.isin(video_exts)]
    elif filter_option == "Nur Bilder":
        file_extensions = file_extensions[file_extensions.isin(image_exts)]

    # Häufigkeit zählen
    extension_counts = Counter(file_extensions)
    if not extension_counts:
        st.warning("Keine Dateien für den gewählten Filter gefunden.")
        return

    ext_df = pd.DataFrame.from_dict(extension_counts, orient="index", columns=["Anzahl"])

    # Balkendiagramm anzeigen
    st.bar_chart(ext_df)