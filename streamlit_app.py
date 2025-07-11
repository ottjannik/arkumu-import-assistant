import streamlit as st
import pandas as pd

# Page title
st.set_page_config(page_title='KHM Archiv Dashboard', page_icon='🎫', layout="wide")
st.title('🎫 KHM Archiv Dashboard')
st.info('Info')




uploaded_file = st.sidebar.file_uploader("Wählen Sie Ihre Datei aus", type=['csv', 'png', 'jpg'])
if uploaded_file is not None:
    # Um die Datei als Bytes zu lesen:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)
    
    # Zum Konvertieren in eine stringbasierte IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)
    
    # Zum Lesen der Datei als String:
    string_data = stringio.read()
    st.write(string_data)