import streamlit as st
from Login.login import login
from Pages import V_Doctor

if 'usuario' not in st.session_state:
    # Oculta barra lateral hasta que se haga login el usuario
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)
    login()
else:
    st.sidebar.write(f"Usuario: {st.session_state['usuario']}")
    #st.sidebar.write(f"Rol: {st.session_state['rol']}")

    if st.session_state['rol'] == 'doctor':
        V_Doctor.main()
