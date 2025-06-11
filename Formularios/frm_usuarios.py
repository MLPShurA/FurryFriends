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
def formulario_nuevo_usuario():
    st.subheader("Registro de Usuarios")

    # Campos del formulario
    nombres = st.text_input("Nombres")
    apellidos = st.text_input("Apellidos")
    cedula = st.text_input("Cédula")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo electrónico")
    mascota = st.text_input("Mascota")
    direccion = st.text_input("Dirección")
    rol = st.selectbox("Rol", ["paciente", "secretaria", "doctor", "veterinario"])

    # Botón para guardar el usuario
    if st.button("Guardar Usuario", key="guardar_usuario_btn"):
        # Validación mínima de campos
        if not nombres or not apellidos or not cedula or not correo:
            st.warning("Por favor complete todos los campos obligatorios.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # 1️⃣ Validar si la cédula ya existe
            query_check = "SELECT id FROM usuarios_detalle WHERE cedula = %s"
            cursor.execute(query_check, (cedula,))
            result = cursor.fetchone()

            if result:
                st.warning("Ya existe un usuario registrado con esta cédula.")
            else:
                # 2️⃣ Insertar en usuarios (login)
                contrasena = generar_contrasena(nombres, apellidos, cedula)
                nombre_usuario = correo  # usamos el correo como username

                query_usuarios = """
                    INSERT INTO usuarios (nombre_usuario, contrasena, rol)
                    VALUES (%s, %s, %s)
                """
                values_usuarios = (nombre_usuario, contrasena, rol)
                cursor.execute(query_usuarios, values_usuarios)
                conn.commit()

                usuario_id = cursor.lastrowid  # obtener el id generado

                # 3️⃣ Insertar en usuarios_detalle
                query_detalle = """
                    INSERT INTO usuarios_detalle (nombres, apellidos, cedula, telefono, correo_electronico, mascota, direccion, usuario_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values_detalle = (nombres, apellidos, cedula, telefono, correo, mascota, direccion, usuario_id)
                cursor.execute(query_detalle, values_detalle)
                conn.commit()

                st.success(f"✅ Usuario registrado exitosamente.\n\n**Usuario:** {nombre_usuario}\n**Contraseña:** {contrasena}")

                # Cambiar el estado para volver al listado
                st.session_state['mostrar_formulario_usuario'] = False

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            st.error(f"Error al registrar usuario: {e}")

    # Botón para volver al listado
    if st.button("Volver al listado", key="volver_listado_btn"):
        st.session_state['mostrar_formulario_usuario'] = False
