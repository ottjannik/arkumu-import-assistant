# views.py
# Diese Datei enthält die Logik für die verschiedenen Tabs der Streamlit-Anwendung

import streamlit as st
import pandas as pd
from validation import (
    check_required_columns_short,
    check_required_columns_detailed,
    check_conditional_required_columns,
)
from config import (
    required_columns, 
    conditional_required_columns, 
    validation_targets
)
from stats import (
    plot_projekt_nr_donut,
    plot_file_extension_distribution
)


def render_overview_tab(df_projekte, df_akteurinnen, df_media, df_grundereignis):
    st.subheader("Übersicht")
    st.write("Hier findest du eine Übersicht über die hochgeladenen Metadaten.")
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
    st.write("Hier kannst du die Pflichtfelder der hochgeladenen Metadaten überprüfen.")

    for target in validation_targets:
        df = dfs.get(target["filename"])
        rule_key = target["rule_key"]

        if "required" in target["checks"]:
            check_required_columns_detailed(df, required_columns[rule_key], target["filename"])

        if "conditional" in target["checks"]:
            check_conditional_required_columns(df, conditional_required_columns[rule_key], target["filename"])

        # Optional: if "either_or" in target["checks"]:
        #     check_either_or_columns(df, either_or_required_columns[rule_key], target["filename"])


def render_projects_tab(df_projekte, df_akteurinnen):
    st.subheader("Projekte")
    st.write("Hier findest du verschiedene Statistiken zu den hochgeladenen Metadaten der Projekte.")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Anzahl Projekte", len(df_projekte), border=True)
    with col2:
        projekte_mit_nr = df_projekte["Projekt_Nr"].value_counts().sum()
        st.metric("Projekte mit Projektnummer", projekte_mit_nr, border=True)
        plot_projekt_nr_donut(df_projekte)
    with col3:
        projekte_ohne_nr = df_projekte["Projekt_Nr"].isna().sum()
        st.metric("Projekte ohne Projektnummer", projekte_ohne_nr, border=True)
    

def render_files_tab(df_media):
    st.subheader("Dateien")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Anzahl Dateien", len(df_media), border=True)
    with col2:
        st.metric("Anzahl Dateien", len(df_media), border=True)

    plot_file_extension_distribution(df_media)

    st.divider()