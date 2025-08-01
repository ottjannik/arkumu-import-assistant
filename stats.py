import streamlit as st
import pandas as pd

def count_projects_with_number(df_projects):
    return ((df_projects["Projekt_Nr"].notnull()) & (df_projects["Projekt_Nr"] != "")).sum()