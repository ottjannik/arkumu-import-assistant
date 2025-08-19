# =============================================================
# validation.py
# Diese Datei enthält die Validierungslogik für die verschiedenen CSV-Dateien
# =============================================================

import streamlit as st
import pandas as pd

import pandas as pd

import pandas as pd

def validate_dataframe(df: pd.DataFrame, rules: dict) -> dict:
    """
    Prüft ein DataFrame anhand der Regeln aus validation_targets.
    Gibt Dict mit Fehlermeldungs-DataFrames zurück.
    """

    results = {
        "required": {"ok": True, "errors": pd.DataFrame()},
        "conditional": {"ok": True, "errors": pd.DataFrame()},
        "either_or": {"ok": True, "errors": pd.DataFrame()},
    }

    # 1. Required Columns
    error_rows = []
    for col in rules.get("required_columns", []):
        if col in df.columns:
            mask = df[col].isna() | (df[col] == "")
            if mask.any():
                results["required"]["ok"] = False
                error_rows.append(df.loc[mask].assign(fehlende_spalte=col))
        else:
            results["required"]["ok"] = False
            error_rows.append(pd.DataFrame({
                "fehlende_spalte": [col],
                "hinweis": ["Spalte nicht vorhanden"]
            }))
    if error_rows:
        results["required"]["errors"] = pd.concat(error_rows, ignore_index=True)

    # 2. Conditional Columns
    error_rows = []
    for cond in rules.get("conditional", []):
        if_col = cond["if_filled"]
        then_cols = cond["then_required"]

        if if_col in df.columns:
            mask = df[if_col].notna() & (df[if_col] != "")
            for col in then_cols:
                if col in df.columns:
                    submask = mask & (df[col].isna() | (df[col] == ""))
                    if submask.any():
                        results["conditional"]["ok"] = False
                        error_rows.append(df.loc[submask, [if_col, col]].assign(fehlende_spalte=col))
                else:
                    results["conditional"]["ok"] = False
                    error_rows.append(pd.DataFrame({
                        if_col: ["Wert vorhanden"],
                        "fehlende_spalte": [col],
                        "hinweis": ["Spalte nicht vorhanden"]
                    }))
    if error_rows:
        results["conditional"]["errors"] = pd.concat(error_rows, ignore_index=True)

    # 3. Either/Or
    error_rows = []
    for group in rules.get("either_or", []):
        mask = pd.Series(True, index=df.index)
        for col in group:
            if col in df.columns:
                mask = mask & (df[col].isna() | (df[col] == ""))
            else:
                mask = mask & True  # Spalte fehlt = automatisch leer

        if mask.any():
            results["either_or"]["ok"] = False
            error_rows.append(df.loc[mask, group].assign(fehlende_gruppe=str(group)))

    if error_rows:
        results["either_or"]["errors"] = pd.concat(error_rows, ignore_index=True)

    return results

# # Funktion zur Pflichtfeldprüfung, welche leere Felder wie NaN oder None durchsucht, aber auch leere Strings ("")
# def check_required_columns_short(df, required_columns, filename):
#     missing_report = {}
#     for col in required_columns:
#         if col not in df.columns:
#             missing_report[col] = "Spalte fehlt"
#         else:
#             missing_count = df[col].isnull().sum() + (df[col] == "").sum()
#             if missing_count > 0:
#                 missing_report[col] = f"{missing_count} fehlende(r) Wert(e)"
#     if missing_report:
#         st.error(f"Fehlende Werte bei Pflichtfeldern in **{filename}**")
#     else:
#         st.success(f"Alle Pflichtfelder in **{filename}** sind befüllt.")


# def check_required_columns_detailed(df, required_columns, filename):
#     missing_entries = []

#     for col in required_columns:
#         if col not in df.columns:
#             missing_entries.append({"Projekt_ID": None, "Fehlende_Spalte": col, "Status": "Spalte fehlt"})
#         else:
#             missing_rows = df[df[col].isnull() | (df[col] == "")]
#             for _, row in missing_rows.iterrows():
#                 missing_entries.append({
#                     "Projekt_ID": row["Projekt_ID"],
#                     "Fehlende_Spalte": col,
#                     "Status": "Wert fehlt"
#                 })

#     if missing_entries:
#         st.error(f"Fehlende Werte bei Pflichtfeldern in **{filename}**")
#         with st.expander("Details anzeigen", expanded=True):
#             st.dataframe(pd.DataFrame(missing_entries))
#     else:
#         st.success(f"Alle Pflichtfelder in **{filename}** sind vollständig.")

# def check_conditional_required_columns(df, conditional_rules, filename):
#     """
#     Prüft für jedes 'if_filled' Feld, ob bei Befüllung auch alle zugehörigen 'then_required' Felder vorhanden sind.

#     Args:
#         df (pd.DataFrame): Das zu prüfende DataFrame.
#         conditional_rules (list): Liste von Regeln mit 'if_filled' und 'then_required' (Liste!).
#         filename (str): Dateiname für Kontext im Reporting.

#     Gibt bei Fehlern eine Streamlit-Warnung mit den betroffenen Zeilen aus.
#     """
#     for rule in conditional_rules:
#         if_col = rule.get("if_filled")
#         then_cols = rule.get("then_required", [])

#         if if_col not in df.columns:
#             st.warning(f"Spalte '{if_col}' fehlt in {filename}.")
#             continue

#         for then_col in then_cols:
#             if then_col not in df.columns:
#                 st.warning(f"Spalte '{then_col}' fehlt in {filename}.")
#                 continue

#             missing_rows = df[
#                 df[if_col].notna() & (df[if_col].astype(str).str.strip() != "") &
#                 (df[then_col].isna() | (df[then_col].astype(str).str.strip() == ""))
#             ]

#             if not missing_rows.empty:
#                 with st.expander(f"'{then_col}' fehlt, wenn '{if_col}' gesetzt ist ({filename}, {len(missing_rows)} Zeilen)"):
#                     st.dataframe(missing_rows[[if_col, then_col]])