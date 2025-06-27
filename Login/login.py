import streamlit as st
from db import get_connection
from Login.security import verify_password

def verificar_usuario(usuario, contraseña):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM usuarios WHERE nombre_usuario = %s"
    cursor.execute(query, (usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        # Si existe hash, usarlo
        if resultado['contrasena_hash']:
            if verify_password(contraseña, resultado['contrasena_hash']):
                return resultado
        else:
            # Comparar contra la contraseña plana (solo si no hay hash)
            if contraseña == resultado['contrasena']:
                return resultado

    return None

def login():
    st.title("Inicio de Sesión")

    if 'logueado' not in st.session_state:
        st.session_state['logueado'] = False

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
                st.success("✅ Inicio de sesión correcto")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
    else:
        st.success(f"Bienvenido, {st.session_state['usuario']}")
