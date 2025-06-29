import streamlit as st
from Login.login import login
from Pages import V_Veterianario, V_Doctor, V_Secretaria, V_Paciente, V_Admin, Citas, Historial_Medico, Notas, Paciente, Prediccion_IA, Tratamientos, Usuarios
from streamlit_option_menu import option_menu
import base64

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

image_path = "Recursos/Kuromi.jpg"
image_base64 = image_to_base64(image_path)

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="Medical Pets", layout="wide")

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    body, .main, .block-container {
        background-color: #C9F7F7;
        color: #000000;
    }

    [data-testid="stSidebar"] {
        background-color: #34CACA;
        color: white;
    }

    [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: bold;
    }

    .stButton>button {
        background-color: #00C2C2;
        color: black;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #008C8C;
        color: white;
    }

    .stSelectbox, .stTextInput>div>input {
        border-radius: 8px !important;
    }

    h1, h2, h3, h4 {
        color: #1B1B1B;
    }

    [data-testid="stSidebarNav"] { display: none; }

    div[data-testid="stButton"] > button.logout-btn {
        position: absolute;
        top: 10px;
        right: 25px;
        background-color: #00C2C2;
        color: black;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
        border-radius: 6px;
        z-index: 100;
    }

    div[data-testid="stButton"] > button.logout-btn:hover {
        background-color: #00a3a3;
    }

    .css-18e3th9 {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- VERIFICACIÓN DE SESIÓN ---
if 'usuario' not in st.session_state:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)
    login()

else:
    # --- Botón de logout funcional en la misma página ---
    col1, col2 = st.columns([0.9, 0.1])
    with col2:
        logout_btn = st.button("Cerrar sesión", key="logout_btn", help="Cerrar sesión", type="primary")
        st.markdown("""<style>button.logout-btn {}</style>""", unsafe_allow_html=True)

    if logout_btn:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Sesión cerrada correctamente")
        st.rerun()

    # --- MENÚ LATERAL CON OPCIONES POR ROL ---
    st.sidebar.write(f"Usuario: {st.session_state['usuario']}")

    PAGINAS_POR_ROL = {
        'admin': ['main', 'Citas', 'Historial Medico', 'Notas', 'Paciente', 'Prediccion IA', 'Tratamientos', 'Usuarios', 'V Admin'],
        'veterinario': ['main', 'Citas', 'Historial Medico', 'Notas', 'Paciente', 'Prediccion IA', 'Tratamientos', 'Usuarios'],
        'doctor': ['main', 'Citas', 'Historial Medico', 'Notas', 'Paciente', 'Prediccion IA', 'Tratamientos', 'Usuarios', 'V Doctor'],
        'paciente': ['main', 'Paciente', 'Citas', 'Tratamientos', 'V Paciente', 'Notas'],
        'secretaria': ['main', 'Usuarios', 'Paciente', 'Citas', 'V Secretaria']
    }

    rol_actual = st.session_state['rol']
    paginas_visibles = PAGINAS_POR_ROL.get(rol_actual, [])

    with st.sidebar:
        seleccion = option_menu(
            menu_title=None,
            options=paginas_visibles,
            menu_icon="cast",
            default_index=0
        )

    st.write(f"Página seleccionada: {seleccion}")

    # --- CONTENIDO PRINCIPAL (encabezado bonito) ---
    if seleccion == 'main':
        st.markdown(f"""
            <div style="text-align:center; margin-top: 50px;">
                <h1 style="color:#004D4D;">¡Bienvenido/a <span style='color:#00C2C2;'>{st.session_state['usuario'].capitalize()}</span>!</h1>
                <img src="data:image/jpeg;base64,{image_base64}" width="120"/>
                <h2 style="color:#004D4D;">Medical <span style='color:#00C2C2;'>Pets</span></h2>
            </div>
        """, unsafe_allow_html=True)

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
