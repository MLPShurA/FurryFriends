import streamlit as st
from db import get_connection
from Formularios.frm_usuarios import formulario_nuevo_usuario

def main():
    st.title("Listado de Usuarios")

    # Estado para controlar si estamos en modo 'Nuevo Usuario'
    if 'mostrar_formulario_usuario' not in st.session_state:
        st.session_state['mostrar_formulario_usuario'] = False

    # Botón + Nuevo → lo mostramos SOLO si no estamos en modo formulario
    if not st.session_state['mostrar_formulario_usuario']:
        if st.button("➕ Nuevo", key="nuevo_usuario_btn"):
            st.session_state['mostrar_formulario_usuario'] = True

    # Si estamos en modo formulario → mostrar el formulario
    if st.session_state['mostrar_formulario_usuario']:
        formulario_nuevo_usuario()

    # Si NO estamos en modo formulario → mostrar la lista
    else:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Obtener datos de los usuarios
        query = """
            SELECT ud.nombres, ud.cedula, ud.telefono, ud.mascota, u.rol
            FROM usuarios_detalle ud
            JOIN usuarios u ON ud.usuario_id = u.id
        """
        cursor.execute(query)
        usuarios = cursor.fetchall()

        cursor.close()
        conn.close()

        st.subheader("Usuarios registrados")

        if usuarios:
            # Cabecera de la tabla
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
            col1.write("**Nombre**")
            col2.write("**Cédula**")
            col3.write("**Celular**")
            col4.write("**Mascota**")
            col5.write("**Rol**")

            # Mostrar los usuarios
            for usuario in usuarios:
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                col1.write(usuario['nombres'])
                col2.write(usuario['cedula'])
                col3.write(usuario['telefono'])
                col4.write(usuario['mascota'])
                col5.write(usuario['rol'])
        else:
            st.info("No hay usuarios registrados.")
