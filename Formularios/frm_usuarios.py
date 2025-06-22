import streamlit as st
import mysql.connector
from db import get_connection

# Función para generar la contraseña automática
def generar_contrasena(nombres, apellidos, cedula):
    parte_nombre = nombres[:3].lower()
    parte_apellido = apellidos[:3].lower()
    parte_cedula = cedula[-3:]
    return parte_nombre + parte_apellido + parte_cedula

# Formulario de nuevo usuario
def formulario_nuevo_usuario(usuario_data=None):
    st.subheader("Registro de Usuarios")

    # Extraer valores si estamos en modo edición
    nombres = st.text_input("Nombres", value=usuario_data.get('nombres') if usuario_data else "")
    apellidos = st.text_input("Apellidos", value=usuario_data.get('apellidos') if usuario_data else "")
    cedula = st.text_input("Cédula", value=usuario_data.get('cedula') if usuario_data else "")
    telefono = st.text_input("Teléfono", value=usuario_data.get('telefono') if usuario_data else "")
    correo = st.text_input("Correo electrónico", value=usuario_data.get('correo_electronico') if usuario_data else "")
    mascota = st.text_input("Mascota", value=usuario_data.get('mascota') if usuario_data else "")
    direccion = st.text_input("Dirección", value=usuario_data.get('direccion') if usuario_data else "")
    rol = st.selectbox("Rol", ["paciente", "secretaria", "doctor", "veterinario"],
                       index=["paciente", "secretaria", "doctor", "veterinario"].index(usuario_data.get('rol')) if usuario_data else 0)

    # Aquí puedes adaptar para guardar o actualizar según si hay usuario_data
    if st.button("Guardar Usuario", key="guardar_usuario_btn"):
        if not nombres or not apellidos or not cedula or not correo:
            st.warning("Por favor complete todos los campos obligatorios.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            if usuario_data:  # Modo editar
                query_update_detalle = """
                    UPDATE usuarios_detalle SET nombres=%s, apellidos=%s, cedula=%s, telefono=%s, correo_electronico=%s, mascota=%s, direccion=%s 
                    WHERE id=%s
                """
                values_detalle = (nombres, apellidos, cedula, telefono, correo, mascota, direccion, usuario_data['detalle_id'])
                cursor.execute(query_update_detalle, values_detalle)

                query_update_usuarios = "UPDATE usuarios SET rol=%s WHERE id=%s"
                cursor.execute(query_update_usuarios, (rol, usuario_data['usuario_id']))

                st.success("✅ Usuario actualizado exitosamente.")

            else:  # Modo nuevo
                from Formularios.frm_usuarios import generar_contrasena
                contrasena = generar_contrasena(nombres, apellidos, cedula)

                query_usuarios = "INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (%s, %s, %s)"
                cursor.execute(query_usuarios, (correo, contrasena, rol))
                usuario_id = cursor.lastrowid

                query_detalle = """
                    INSERT INTO usuarios_detalle (nombres, apellidos, cedula, telefono, correo_electronico, mascota, direccion, usuario_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_detalle, (nombres, apellidos, cedula, telefono, correo, mascota, direccion, usuario_id))

                st.success(f"✅ Usuario creado. Usuario: {correo} | Contraseña: {contrasena}")

            conn.commit()
            cursor.close()
            conn.close()

            st.session_state['mostrar_formulario_usuario'] = False
            st.session_state['usuario_editar'] = None
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {e}")

    if st.button("Volver al listado", key="volver_listado_btn"):
        st.session_state['mostrar_formulario_usuario'] = False
        st.session_state['usuario_editar'] = None
        st.rerun()
