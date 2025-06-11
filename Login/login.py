import streamlit as st
from db import get_connection

def verificar_usuario(usuario, contrasena):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
    cursor.execute(query, (usuario, contrasena))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def login():
    st.title("Inicio de Sesión")

    # Inicializa el estado de login si no existe
    if 'logueado' not in st.session_state:
        st.session_state['logueado'] = False

    # Mostrar formulario solo si no está logueado
    if not st.session_state['logueado']:
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        login_boton = st.button("Iniciar sesión")

        if login_boton:
            user_data = verificar_usuario(usuario, contrasena)
            if user_data:
                st.session_state['usuario'] = user_data['nombre_usuario']
                st.session_state['rol'] = user_data['rol']
                st.session_state['logueado'] = True
                st.rerun()
                return
            else:
                st.error("El usuario o contraseña no existe, intente de nuevo")


if __name__ == "__main__":
    login()