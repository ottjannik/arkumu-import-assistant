# stats.py
import streamlit as st
import plotly.graph_objects as go

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