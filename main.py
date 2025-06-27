import streamlit as st
from Login.login import login
from Pages import V_Veterianario, V_Doctor, V_Secretaria, V_Paciente, V_Admin, Citas, Historial_Medico, Notas, Paciente, Prediccion_IA, Tratamientos, Usuarios, crud_usuarios
from streamlit_option_menu import option_menu


st.markdown("""
    <style>
    /* Oculta el menú de navegación de Streamlit multipage */
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

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
    # st.sidebar.write(f"Rol: {st.session_state['rol']}")


    PAGINAS_POR_ROL = {
        'admin': ['main', 'Citas', 'Historial Medico', 'Notas', 'Paciente', 'Prediccion IA', 'Tratamientos', 'Usuarios', 'V Admin'],
        'veterinario': ['main', 'Citas', 'Historial Medico', 'Notas', 'Paciente', 'Prediccion IA', 'Tratamientos', 'Usuarios'],
        'doctor': ['main', 'Citas', 'Historial Medico', 'Notas', 'Paciente', 'Prediccion IA', 'Tratamientos', 'Usuarios', 'V Doctor'],
        'paciente': ['main', 'Paciente', 'Citas', 'Tratamientos', 'V Paciente', 'Notas'],
        'secretaria': ['main', 'Usuarios', 'Paciente', 'Citas', 'V Secretaria']
    }

    # Obtenemos el rol actual
    rol_actual = st.session_state['rol']

    # Obtenemos las páginas permitidas para ese rol
    paginas_visibles = PAGINAS_POR_ROL.get(rol_actual, [])

    # Mostramos solo esas páginas en el menú
    with st.sidebar:
        seleccion = option_menu(
            menu_title=None,
            options=paginas_visibles,
            menu_icon="cast",
            default_index=0
        )

    st.write(f"Página seleccionada: {seleccion}")


    if seleccion == 'main':
        st.title(f"Ventana del {rol_actual.upper()}")
        st.write(f"Bienvenido : {st.session_state['usuario']}")
    elif seleccion == 'V Admin' and rol_actual == 'admin':
        V_Admin.main()
    elif seleccion == 'V Doctor' and rol_actual == 'doctor':
        V_Doctor.main()
    elif seleccion == 'V Paciente' and rol_actual == 'paciente':
        V_Paciente.main()
    elif seleccion == 'V Secretaria' and rol_actual == 'secretaria':
        V_Secretaria.main()
    elif seleccion == 'V Veterinario' and rol_actual == 'veterinario':
        V_Veterianario.main()
    elif seleccion == 'Citas':
        Citas.main()
    elif seleccion == 'Historial Medico':
        Historial_Medico.main()
    elif seleccion == 'Notas':
        Notas.main()
    elif seleccion == 'Paciente':
        Paciente.main()
    elif seleccion == 'Prediccion IA':
        Prediccion_IA.main()
    elif seleccion == 'Tratamientos':
        Tratamientos.main()
    elif seleccion == 'Usuarios':
        Usuarios.main()
