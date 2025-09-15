# ============================================================
# views.py
# Diese Datei enthält die Logik für die verschiedenen Tabs der Streamlit-Anwendung und rendert die entsprechenden Inhalte.
# ============================================================

import streamlit as st
import pandas as pd
import datetime as dt

from validation import (
    validate_dataframe
)

from stats import (
    plot_file_extension_distribution
)

from utils import (
    create_error_report
)

import streamlit as st

def render_overview_tab(named_dfs, validation_targets):
    """Rendert den Übersichts-Tab der Anwendung mit grundlegenden Statistiken
    und einer Kurzversion der hochgeladenen CSV-Dateien.

    Args:
        named_dfs (dict): Dictionary mit DataFrames für die verschiedenen Metadaten.
        validation_targets (dict): Dictionary mit den Validierungszielen, enthält z.B. Dateinamen.
    Returns:
        None
    """
    st.header("Übersicht")
    st.info("Hier findest du eine Übersicht über den Inhalt der hochgeladenen Metadaten.")

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

    st.subheader("Dateiendungen")
    st.info("Hier siehst du die Verteilung der Dateiendungen der digitalen Objekte.")
    plot_file_extension_distribution(named_dfs["media_digitale_objekte"])


def render_validation_tab(named_dfs, validation_targets):
    """
    Rendert den Tab für die Pflichtfeldprüfung.
    Nutzt die Validierungsregeln aus der Config und zeigt Ergebnisse in Expandern.
    Args:
        named_dfs (dict): Dictionary mit DataFrames für die verschiedenen Metadaten.
        validation_targets (dict): Dictionary mit den Validierungszielen, enthält z.B. Dateinamen.
    Returns:
        None
    """


    st.header("Pflichtfeldprüfung")
    st.info("""
    Die App prüft die hochgeladenen CSV-Dateien auf **Vollständigkeit** und das Erfüllen der **Pflichtfelder**.  
    Die CSV-Dateien können hier nur **eingesehen** werden.  
    Änderungen an den Daten müssen in der **Quelldatenbank** erfolgen.  

    **Legende:**  
    🟢 = alle Prüfungen bestanden  
    🔴 = es gibt Fehler / unvollständige Felder
    """)
    validation_results = {}

    # 1. Validation durchführen
    for df_key, df in named_dfs.items():
        rules = validation_targets[df_key]
        validation_results[df_key] = validate_dataframe(df, rules)

    # 2. Fehlerbericht erstellen und Download-Button anbieten
    error_report = create_error_report(validation_results, validation_targets)
    today = dt.date.today().strftime("%Y-%m-%d")
    st.download_button(
        label="Gesamten Fehlerbericht herunterladen",
        data=error_report,
        file_name=f"{today}_validierungsfehler.xlsx",
        type="primary",
        icon="📥",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # 3. Ergebnisse pro Datei darstellen
    for df_key, result in validation_results.items():
        filename = validation_targets[df_key]["filename"]

        # Gesamtstatus prüfen
        overall_ok = all([
            result["required"]["ok"],
            result["conditional"]["ok"],
            result["either_or"]["ok"]
        ])
        overall_icon = "🟢" if overall_ok else "🔴"

        # Icons für die einzelnen Prüftypen
        icon_required = "🟢" if result["required"]["ok"] else "🔴"
        icon_conditional = "🟢" if result["conditional"]["ok"] else "🔴"
        icon_either_or = "🟢" if result["either_or"]["ok"] else "🔴"

        with st.expander(f"{overall_icon} {filename}", expanded=False):
            # Tabs mit Icons in den Labels
            tab_required, tab_conditional, tab_either_or, tab_csv = st.tabs([
                f"{icon_required} Pflichtfelder",
                f"{icon_conditional} Bedingte Pflichtfelder",
                f"{icon_either_or} Entweder-Oder Pflichtelder",
                f"{'📄'} CSV-Datei anzeigen"
            ])

            with tab_required:
                if result["required"]["ok"]:
                    st.success("Alle Pflichtfelder ausgefüllt")
                else:
                    st.error("Fehler bei Pflichtfeldern")
                    df_errors = result["required"]["errors"]
                    st.dataframe(df_errors)
                    
                    # Download-Link für Fehler-CSV
                    csv_errors = df_errors.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Fehler als CSV herunterladen",
                        data=csv_errors,
                        file_name=f"{today}_{filename}_pflichtfelder_fehler.csv",
                        mime="text/csv"
                    )

            with tab_conditional:
                if result["conditional"]["ok"]:
                    st.success("Alle bedingte Pflichtfelder sind ausgefüllt")
                else:
                    st.error("Fehler bei bedingten Pflichtfeldern")
                    df_errors = result["conditional"]["errors"]
                    st.dataframe(df_errors)

                    # Download-Link für Fehler-CSV
                    csv_errors = df_errors.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Fehler als CSV herunterladen",
                        data=csv_errors,
                        file_name=f"{today}_{filename}_conditional_fehler.csv",
                        mime="text/csv"
                    )

            with tab_either_or:
                if result["either_or"]["ok"]:
                    st.success("Alle Entweder-Oder Pflichtfelder sind ausgefüllt")
                else:
                    st.error("Fehler bei Entweder-Oder Pflichtfeldern")
                    df_errors = result["either_or"]["errors"]
                    st.dataframe(df_errors)

                    # Download-Link für Fehler-CSV
                    csv_errors = df_errors.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Fehler als CSV herunterladen",
                        data=csv_errors,
                        file_name=f"{today}_{filename}_either_or_fehler.csv",
                        mime="text/csv"
                    )

            with tab_csv:
                st.info(f"Ansicht: **{filename}**")
                st.dataframe(named_dfs[df_key])
  
# def render_csv_view_tab(named_dfs, validation_targets):
#     """
#     Rendert den Tab für die CSV-Ansicht.
#     Zeigt die hochgeladenen CSV-Dateien in einem DataFrame an.
#     Args:
#         named_dfs (dict): Dictionary mit DataFrames für die verschiedenen Metadaten.
#         validation_targets (dict): Dictionary mit den Validierungszielen, enthält z.B. Dateinamen.
#     Returns:
#         None
#     """
#     st.header("CSV-Dateien ")
#     st.write("Hier kannst du die hochgeladenen CSV-Dateien einsehen.")

#     for df_key, df in named_dfs.items():
#         filename = validation_targets[df_key]["filename"]
#         with st.expander(f"**{filename}** ({len(df)} Zeilen, {len(df.columns)} Spalten)", expanded=False):
#             st.dataframe(df)



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