# stats.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from collections import Counter

# Funktion zum Plotten der Dateiendungsverteilung
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

def plot_projekt_nr_donut(df_projekte):
    total = len(df_projekte)
    with_projekt_nr = df_projekte["Projekt_Nr"].notna().sum()
    without_projekt_nr = total - with_projekt_nr

    values = [with_projekt_nr, without_projekt_nr]
    labels = ["Mit Projekt_Nr", "Ohne Projekt_Nr"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        textinfo='percent+label',
        insidetextorientation='radial'
    )])

    fig.update_layout(
        title_text="Projekt_Nr-Verteilung",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)