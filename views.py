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
    st.markdown("Hier findest du eine Übersicht über den Inhalt der hochgeladenen Metadaten.")

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
    st.markdown("Hier siehst du die Verteilung der Dateiendungen der digitalen Objekte.")
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
    st.markdown("""
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

        # Anzahl Fehler für jeweilige Datei berechnen
        error_count = sum([
            0 if result["required"]["ok"] else len(result["required"]["errors"]),
            0 if result["conditional"]["ok"] else len(result["conditional"]["errors"]),
            0 if result["either_or"]["ok"] else len(result["either_or"]["errors"]),
        ])

        # Expander-Label mit Fehleranzahl
        if error_count == 0:
            expander_label = f"{overall_icon} {filename}"
        else:
            expander_label = f"{overall_icon} {filename} ({error_count} Fehler)"

        # Expander für jede Datei
        with st.expander(expander_label, expanded=False):
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
                    required_errors = len(result["required"]["errors"])
                    st.error(f"{required_errors} Fehler bei Pflichtfeldern")
                    df_errors = result["required"]["errors"]
                    st.dataframe(df_errors)

            with tab_conditional:
                if result["conditional"]["ok"]:
                    st.success("Alle bedingte Pflichtfelder sind ausgefüllt")
                else:
                    conditional_errors = len(result["conditional"]["errors"])
                    st.error(f"{conditional_errors} Fehler bei bedingten Pflichtfeldern")
                    df_errors = result["conditional"]["errors"]
                    st.dataframe(df_errors)

            with tab_either_or:
                if result["either_or"]["ok"]:
                    st.success("Alle Entweder-Oder Pflichtfelder sind ausgefüllt")
                else:
                    either_or_errors = len(result["either_or"]["errors"])
                    st.error(f"{either_or_errors} Fehler bei Entweder-Oder Pflichtfeldern")
                    df_errors = result["either_or"]["errors"]
                    st.dataframe(df_errors)

            with tab_csv:
                st.info(f"Ansicht: **{filename}**")
                st.dataframe(named_dfs[df_key])