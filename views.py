# ============================================================
# views.py
# Diese Datei enthält die Logik für die verschiedenen Tabs der Streamlit-Anwendung und rendert die entsprechenden Inhalte.
# ============================================================

import streamlit as st
import pandas as pd

# from validation import (
#     validate_required_columns
# #     check_required_columns_short,
# #     check_required_columns_detailed,
# #     check_conditional_required_columns,
# )
# # from stats import (
#     # plot_projekt_nr_donut,
# #     plot_file_extension_distribution
# #)


def render_overview_tab(named_dfs, validation_targets, required_columns, conditional_required_columns, either_or_columns):
    """Rendert den Übersichts-Tab der Anwendung mit grundlegenden Statistiken, Metriken
    und einer Kurzversion der Pflichtfeldprüfung.
    Args:
        named_dfs (dict): Dictionary mit DataFrames für die verschiedenen Metadaten.
        required_columns (dict): Dictionary mit erforderlichen Spalten für die Validierung.
    Returns:
            None
    """    
    st.subheader("Übersicht")
    st.write("Hier findest du eine Übersicht über den Inhalt der hochgeladenen Metadaten.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Projekte", len(named_dfs["projekte"]), border=True)
        st.metric("Auszeichnungen", len(named_dfs["auszeichnungen"]), border=True)
        len_all_events = len(named_dfs["events"]) + len(named_dfs["grundereignis"])
        st.metric("Ereignisse (Grundereignis + Events)", len_all_events, border=True)
    with col2:
        st.metric("Akteur:innen", len(named_dfs["akteurinnen"]), border=True)
        st.metric("Keywords", len(named_dfs["keywords"]), border=True)
        st.metric("Equipment & Software", len(named_dfs["equipmentundsoftware"]), border=True)
    with col3:
        st.metric("Digitale Objekte", len(named_dfs["media_digitale_objekte"]), border=True)
        st.metric("Informationsträger", len(named_dfs["physmedien_informationstraeger"]), border=True)
        st.metric("Physische Objekte", len(named_dfs["physischesobjekt"]), border=True)

    st.divider()

    # Liste der hochgeladenen Dateien
    st.subheader("CSV-Dateien")
    st.write("Hier findest du eine Übersicht über die hochgeladenen CSV-Dateien und deren Inhalt.")
    for df_key, df in named_dfs.items():
        filename = validation_targets[df_key]["filename"]
        with st.expander(f"**{filename}** ({len(df)} Zeilen, {len(df.columns)} Spalten)", expanded=False):
            st.dataframe(df)

    # Todo: Kurze Ausgabe der Pflichtfeldprüfung. Keine detaillierte Prüfung hier, nur Info in welchen Dateien die Prüfung erfolgreich war/fehler aufgetraten sind.


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

    

  






    # check_required_columns_short(df_projekte, required_columns["projekte"], "00_Projekte.csv")
    # check_required_columns_short(df_akteurinnen, required_columns["akteurinnen"], "03_Personen_Akteurinnen.csv")

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