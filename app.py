import streamlit as st
import json

# --- Inicialización del estado de la sesión --- 
# Streamlit maneja el estado de la aplicación. 
# Aseguramos que nuestras variables clave existan en st.session_state.
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# --- Funciones del sistema adaptadas para Streamlit --- 

def register_user_st(username, password):
    if username in st.session_state.users_db:
        st.error(f"El usuario '{username}' ya existe. Por favor, elige otro.")
        return False
    else:
        st.session_state.users_db[username] = {'password': password, 'score': 0}
        st.success(f"Usuario '{username}' registrado exitosamente con un puntaje inicial de 0.")
        return True

def login_user_st(username, password):
    if username in st.session_state.users_db and st.session_state.users_db[username]['password'] == password:
        st.session_state.logged_in_user = username
        st.success(f"¡Bienvenido, {username}! Has iniciado sesión exitosamente.")
        return True
    else:
        st.error("Nombre de usuario o contraseña incorrectos.")
        return False

def logout_user_st():
    st.session_state.logged_in_user = None
    st.info("Has cerrado sesión.")

def update_score_st(username, new_score):
    if username in st.session_state.users_db:
        st.session_state.users_db[username]['score'] = new_score
        st.success(f"Puntaje de {username} actualizado a {new_score}.")
    else:
        st.error(f"El usuario '{username}' no existe.")

def reset_user_score_st(username):
    if username in st.session_state.users_db:
        st.session_state.users_db[username]['score'] = 0
        st.success(f"El puntaje de '{username}' ha sido restablecido a 0.")
    else:
        st.error(f"El usuario '{username}' no existe.")

def delete_user_st(username):
    if username in st.session_state.users_db:
        del st.session_state.users_db[username]
        st.success(f"Usuario '{username}' eliminado exitosamente.")
        if st.session_state.logged_in_user == username:
            st.session_state.logged_in_user = None
            st.info("Sesión cerrada para el usuario eliminado.")
    else:
        st.error(f"El usuario '{username}' no existe y no puede ser eliminado.")

# --- Diseño de la interfaz de usuario con Streamlit --- 

st.set_page_config(layout="centered", page_title="Sistema de Puntajes")
st.title("🎮 Sistema de Gestión de Puntajes")

# Mostrar el estado actual de la base de datos (para depuración y demostración)
# st.sidebar.header("Base de Datos (DEBUG)")
# st.sidebar.json(st.session_state.users_db)

# --- Lógica de la aplicación --- 

if st.session_state.logged_in_user:
    # Si el usuario está logueado
    st.subheader(f"Bienvenido, {st.session_state.logged_in_user}!")
    user_data = st.session_state.users_db[st.session_state.logged_in_user]
    st.metric(label=f"Tu puntaje actual es:", value=user_data['score'])

    st.divider()

    # Opción para cerrar sesión
    if st.button("Cerrar Sesión", key="logout_btn"):
        logout_user_st()
        st.rerun()

    # Sección para administradores o para que el usuario gestione su propio puntaje (opcional)
    # Por simplicidad, todos pueden 'editar' su propio puntaje si están logueados.
    st.subheader("Gestionar Puntaje")
    new_score = st.number_input("Nuevo puntaje", value=user_data['score'], min_value=0, key="new_score_input")
    if st.button("Actualizar mi Puntaje", key="update_my_score_btn"):
        update_score_st(st.session_state.logged_in_user, new_score)

    if st.button("Restablecer mi Puntaje a 0", key="reset_my_score_btn"):
        reset_user_score_st(st.session_state.logged_in_user)

    if st.button("Eliminar mi Cuenta", key="delete_my_account_btn"):
        delete_user_st(st.session_state.logged_in_user)
        st.rerun()


else:
    # Si nadie está logueado, mostrar opciones de registro e inicio de sesión
    st.subheader("Iniciar Sesión o Registrarse")

    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])

    with tab1:
        st.markdown("### Iniciar Sesión")
        login_username = st.text_input("Nombre de usuario", key="login_username")
        login_password = st.text_input("Contraseña", type="password", key="login_password")
        if st.button("Iniciar Sesión", key="do_login_btn"):
            if login_user_st(login_username, login_password):
                st.rerun()

    with tab2:
        st.markdown("### Registrarse")
        register_username = st.text_input("Nuevo nombre de usuario", key="register_username")
        register_password = st.text_input("Nueva contraseña", type="password", key="register_password")
        if st.button("Registrarse", key="do_register_btn"):
            register_user_st(register_username, register_password)


# Para que Streamlit sepa que es un archivo que debe ejecutar
# Escribe este código en un archivo 'app.py' y ejecútalo con `streamlit run app.py`
# En Colab, usaremos `%%writefile` y `!streamlit run`

file_content = """
import streamlit as st

# --- Funciones del sistema adaptadas para Streamlit --- 
# Se asume que users_db y logged_in_user son manejados por st.session_state

def register_user_st(username, password):
    if username in st.session_state.users_db:
        st.error(f"El usuario '{username}' ya existe. Por favor, elige otro.")
        return False
    else:
        st.session_state.users_db[username] = {'password': password, 'score': 0}
        st.success(f"Usuario '{username}' registrado exitosamente con un puntaje inicial de 0.")
        return True

def login_user_st(username, password):
    if username in st.session_state.users_db and st.session_state.users_db[username]['password'] == password:
        st.session_state.logged_in_user = username
        st.success(f"¡Bienvenido, {username}! Has iniciado sesión exitosamente.")
        return True
    else:
        st.error("Nombre de usuario o contraseña incorrectos.")
        return False

def logout_user_st():
    st.session_state.logged_in_user = None
    st.info("Has cerrado sesión.")

def update_score_st(username, new_score):
    if username in st.session_state.users_db:
        st.session_state.users_db[username]['score'] = new_score
        st.success(f"Puntaje de {username} actualizado a {new_score}.")
    else:
        st.error(f"El usuario '{username}' no existe.")

def reset_user_score_st(username):
    if username in st.session_state.users_db:
        st.session_state.users_db[username]['score'] = 0
        st.success(f"El puntaje de '{username}' ha sido restablecido a 0.")
    else:
        st.error(f"El usuario '{username}' no existe.")

def delete_user_st(username):
    if username in st.session_state.users_db:
        del st.session_state.users_db[username]
        st.success(f"Usuario '{username}' eliminado exitosamente.")
        if st.session_state.logged_in_user == username:
            st.session_state.logged_in_user = None
            st.info("Sesión cerrada para el usuario eliminado.")
    else:
        st.error(f"El usuario '{username}' no existe y no puede ser eliminado.")

# --- Configuración y Diseño de la interfaz de usuario con Streamlit --- 

st.set_page_config(layout="centered", page_title="Sistema de Puntajes")
st.title("🎮 Sistema de Gestión de Puntajes")

# Inicialización del estado de la sesión si no existe
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None


# --- Lógica de la aplicación --- 

if st.session_state.logged_in_user:
    # Si el usuario está logueado
    st.subheader(f"Bienvenido, {st.session_state.logged_in_user}!")
    user_data = st.session_state.users_db[st.session_state.logged_in_user]
    st.metric(label=f"Tu puntaje actual es:", value=user_data['score'])

    st.divider()

    # Opción para cerrar sesión
    if st.button("Cerrar Sesión", key="logout_btn"):
        logout_user_st()
        st.rerun()

    # Sección para que el usuario gestione su propio puntaje
    st.subheader("Gestionar mi Puntaje")
    new_score = st.number_input("Nuevo puntaje", value=user_data['score'], min_value=0, key="new_score_input")
    if st.button("Actualizar mi Puntaje", key="update_my_score_btn"):
        update_score_st(st.session_state.logged_in_user, new_score)
        st.rerun() # Recargar para ver el cambio reflejado

    if st.button("Restablecer mi Puntaje a 0", key="reset_my_score_btn"):
        reset_user_score_st(st.session_state.logged_in_user)
        st.rerun()

    st.divider()
    st.subheader("Gestión de Cuenta")
    if st.button("Eliminar mi Cuenta", key="delete_my_account_btn"):
        delete_user_st(st.session_state.logged_in_user)
        st.rerun()


else:
    # Si nadie está logueado, mostrar opciones de registro e inicio de sesión
    st.subheader("Iniciar Sesión o Registrarse")

    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])

    with tab1:
        st.markdown("### Iniciar Sesión")
        login_username = st.text_input("Nombre de usuario", key="login_username")
        login_password = st.text_input("Contraseña", type="password", key="login_password")
        if st.button("Iniciar Sesión", key="do_login_btn"):
            if login_user_st(login_username, login_password):
                st.rerun()

    with tab2:
        st.markdown("### Registrarse")
        register_username = st.text_input("Nuevo nombre de usuario", key="register_username")
        register_password = st.text_input("Nueva contraseña", type="password", key="register_password")
        if st.button("Registrarse", key="do_register_btn"):
            if register_user_st(register_username, register_password):
                pass # No recargar, dejar al usuario en la pestaña de registro para otra acción

# Información de depuración (opcional)
st.sidebar.header("Estado de la Sesión (DEBUG)")
st.sidebar.write("Usuario logueado:", st.session_state.logged_in_user)
st.sidebar.json(st.session_state.users_db)

"""

