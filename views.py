import pandas as pd
import streamlit as st
import os
from collections import Counter



def plot_file_extension_distribution(df_media):
    st.subheader("Dateiendungen")
    st.write("Die Verteilung der Dateiendungen in den Media-Dateien zeigt, welche Formate am häufigsten verwendet werden.")

    if "Dateipfad_absolut" not in df_media.columns:
        st.error("Die Spalte 'Dateipfad_absolut' fehlt in der Datei.")
        return

    # Dateiendungen extrahieren
    file_extensions = df_media["Dateipfad_absolut"].dropna().apply(
        lambda x: os.path.splitext(x)[-1].lower().lstrip(".")
    )

    # Häufigkeit zählen
    extension_counts = Counter(file_extensions)
    ext_df = pd.DataFrame.from_dict(extension_counts, orient="index", columns=["Anzahl"])

    # Balkendiagramm mit Streamlit
    st.bar_chart(ext_df)
