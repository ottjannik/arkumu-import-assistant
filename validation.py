# =============================================================
# validation.py
# Diese Datei enthält die Validierungslogik für die verschiedenen CSV-Dateien
# =============================================================

import streamlit as st
import pandas as pd

def validate_dataframe(df: pd.DataFrame, rules: dict) -> dict:
    """
    Validiert ein DataFrame nach Required, Conditional und Either/Or Regeln.
    Gibt ein Dictionary mit OK-Status und Fehler-DataFrames zurück.
    Zusätzlich wird eine Spalte 'Fehlerbeschreibung' hinzugefügt.
    """
    result = {
        "required": {"ok": True, "errors": pd.DataFrame()},
        "conditional": {"ok": True, "errors": pd.DataFrame()},
        "either_or": {"ok": True, "errors": pd.DataFrame()}
    }

    # Hilfsfunktion: betroffene Spalten + ID extrahieren + Fehlerbeschreibung
    def extract_error_rows(rows_df, cols, description):
        """
        Gibt die ID-Spalte (Projekt_ID oder erste Spalte) + Fehlerbeschreibung zurück.
        """
        if rows_df.empty:
            return pd.DataFrame()  # nichts zu tun

        # ID-Spalte bestimmen (Projekt_ID oder erste Spalte)
        id_col = "Projekt_ID" if "Projekt_ID" in rows_df.columns else rows_df.columns[0]

        # Nur ID + Fehlerbeschreibung behalten
        error_df = rows_df[[id_col]].copy()
        error_df["Fehlerbeschreibung"] = description

        return error_df

    # -------------------
    # Required prüfen
    # -------------------
    required_cols = rules.get("required", [])
    missing_entries = []
    for col in required_cols:
        if col not in df.columns:
            missing_entries.append(pd.DataFrame({"Fehlende_Spalte": [col], "Fehlerbeschreibung": ["Spalte fehlt"]}))
        else:
            missing_rows = df[df[col].isnull() | (df[col] == "")]
            if not missing_rows.empty:
                missing_entries.append(extract_error_rows(missing_rows, [col], f"{col} fehlt"))

    if missing_entries:
        result["required"]["ok"] = False
        result["required"]["errors"] = pd.concat(missing_entries, ignore_index=True)

    # -------------------
    # Conditional prüfen
    # -------------------
    conditional_rules = rules.get("conditional", [])
    conditional_errors = []
    for rule in conditional_rules:
        if_col = rule.get("if_filled")
        then_cols = rule.get("then_required", [])
        if if_col in df.columns:
            for then_col in then_cols:
                if then_col not in df.columns:
                    conditional_errors.append(pd.DataFrame({"Fehlende_Spalte": [then_col], "Fehlerbeschreibung": ["Spalte fehlt"]}))
                    continue
                missing_rows = df[
                    df[if_col].notna() & (df[if_col].astype(str).str.strip() != "") &
                    (df[then_col].isna() | (df[then_col].astype(str).str.strip() == ""))
                ]
                if not missing_rows.empty:
                    conditional_errors.append(extract_error_rows(
                        missing_rows, [if_col, then_col],
                        f"Wenn {if_col} ausgefüllt ist, muss {then_col} ebenfalls ausgefüllt sein"
                    ))
    if conditional_errors:
        result["conditional"]["ok"] = False
        result["conditional"]["errors"] = pd.concat(conditional_errors, ignore_index=True)

    # -------------------
    # Either/Or prüfen
    # -------------------

    either_or_rules = rules.get("either_or", [])
    either_or_errors = []

    for rule in either_or_rules:
        cols = rule.get("columns", [])

        # prüft pro Zeile: sind ALLE relevanten Spalten leer oder NaN?
        missing_rows = df[df[cols].apply(
            lambda row: all((pd.isna(v) or str(v).strip() == "") for v in row),
            axis=1
        )]

        if not missing_rows.empty:
            either_or_errors.append(extract_error_rows(
                missing_rows, cols,
                f"Mindestens eine der Spalten {', '.join(cols)} muss ausgefüllt sein"
            ))

    if either_or_errors:
        result["either_or"]["ok"] = False
        result["either_or"]["errors"] = pd.concat(either_or_errors, ignore_index=True)

    return result