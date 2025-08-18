# ============================================================
# views.py
# Diese Datei enthält die Logik für die verschiedenen Tabs der Streamlit-Anwendung und rendert die entsprechenden Inhalte.
# ============================================================

import streamlit as st
import pandas as pd

# from validation import (
#     check_required_columns_short,
#     check_required_columns_detailed,
#     check_conditional_required_columns,
# )
# from stats import (
#     plot_projekt_nr_donut,
#     plot_file_extension_distribution
# )


def render_overview_tab(named_dfs, required_columns):
    """Rendert den Übersichts-Tab der Anwendung mit grundlegenden Statistiken und Metriken.
    Args:
        named_dfs (dict): Dictionary mit DataFrames für die verschiedenen Metadaten.
        required_columns (dict): Dictionary mit erforderlichen Spalten für die Validierung.
    Returns:
            None
    """    
    st.subheader("Übersicht")
    st.write("Hier findest du eine Übersicht über die hochgeladenen Metadaten.")

    df_projekte = named_dfs.get("projekte")
    df_akteurinnen = named_dfs.get("akteurinnen")
    df_media = named_dfs.get("media_digitale_objekte")
    df_auszeichnungen = named_dfs.get("auszeichnungen")
    df_keywords = named_dfs.get("keywords")
    df_informationstraeger = named_dfs.get("physmedien_informationstraeger")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Projekte", len(df_projekte), border=True)
        st.metric("Auszeichnungen", len(df_auszeichnungen), border=True)
    with col2:
        st.metric("Akteur:innen", len(df_akteurinnen), border=True)
        st.metric("Keywords", len(df_keywords), border=True)
    with col3:
        st.metric("Dateien", len(df_media), border=True)
        st.metric("Informationsträger", len(df_informationstraeger), border=True)

    st.divider()

    # st.subheader("Pflichtfelder")
    # check_required_columns_short(df_projekte, required_columns["projekte"], "00_Projekte.csv")
    # check_required_columns_short(df_akteurinnen, required_columns["akteurinnen"], "03_Personen_Akteurinnen.csv")


# def render_validation_tab(
#     dfs,
#     required_columns,
#     conditional_required_columns,
#     validation_targets
# ):
#     st.subheader("Pflichtfeldprüfung")
#     st.write("Hier kannst du die Pflichtfelder der hochgeladenen Metadaten überprüfen.")

#     for target in validation_targets:
#         df = dfs.get(target["filename"])
#         rule_key = target["rule_key"]

#         if "required" in target["checks"]:
#             check_required_columns_detailed(df, required_columns[rule_key], target["filename"])

#         if "conditional" in target["checks"]:
#             check_conditional_required_columns(df, conditional_required_columns[rule_key], target["filename"])

# def render_projects_tab(df_projekte, df_akteurinnen):
#     st.subheader("Projekte")
#     st.write("Hier findest du verschiedene Statistiken zu den hochgeladenen Metadaten der Projekte.")
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.metric("Anzahl Projekte", len(df_projekte), border=True)
#     with col2:
#         projekte_mit_nr = df_projekte["Projekt_Nr"].value_counts().sum()
#         st.metric("Projekte mit Projektnummer", projekte_mit_nr, border=True)
#         plot_projekt_nr_donut(df_projekte)
#     with col3:
#         projekte_ohne_nr = df_projekte["Projekt_Nr"].isna().sum()
#         st.metric("Projekte ohne Projektnummer", projekte_ohne_nr, border=True)
    

# def render_files_tab(df_media):
#     st.subheader("Dateien")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric("Anzahl Dateien", len(df_media), border=True)
#     with col2:
#         st.metric("Anzahl Dateien", len(df_media), border=True)

#     plot_file_extension_distribution(df_media)

#     st.divider()