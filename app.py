import streamlit as st
import json

# --- Inicialización del estado de la sesión ---
# Streamlit maneja el estado de la aplicación.
# Aseguramos que nuestras variables clave existan en st.session_state.
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
# Añadir un usuario administrador para demostración
if 'admin' not in st.session_state.users_db:
    st.session_state.users_db['admin'] = {'password': 'adminpass', 'score': -1} # Score -1 para admin

# --- Funciones del sistema adaptadas para Streamlit ---

def register_user_st(username, password):
    if username in st.session_state.users_db:
        st.error(f"El usuario '{username}' ya existe. Por favor, elige otro. " +
                 "Si eres administrador, puedes gestionar usuarios existentes en el panel de administrador.")
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
    if username in st.session_state.users_db and username != 'admin': # No actualizar score del admin directamente
        st.session_state.users_db[username]['score'] = new_score
        st.success(f"Puntaje de {username} actualizado a {new_score}.")
    elif username == 'admin':
        st.warning("No se puede actualizar el puntaje del usuario administrador.")
    else:
        st.error(f"El usuario '{username}' no existe.")

def reset_user_score_st(username):
    if username in st.session_state.users_db and username != 'admin':
        st.session_state.users_db[username]['score'] = 0
        st.success(f"El puntaje de '{username}' ha sido restablecido a 0.")
    elif username == 'admin':
        st.warning("No se puede restablecer el puntaje del usuario administrador.")
    else:
        st.error(f"El usuario '{username}' no existe.")

def delete_user_st(username):
    if username in st.session_state.users_db:
        if username == 'admin':
            st.error("No se puede eliminar el usuario administrador.")
            return False
        del st.session_state.users_db[username]
        st.success(f"Usuario '{username}' eliminado exitosamente.")
        if st.session_state.logged_in_user == username:
            st.session_state.logged_in_user = None
            st.info("Sesión cerrada para el usuario eliminado.")
        return True
    else:
        st.error(f"El usuario '{username}' no existe y no puede ser eliminado.")
        return False

# --- Diseño de la interfaz de usuario con Streamlit ---

st.set_page_config(layout="centered", page_title="Sistema de Puntajes")
st.title("🎮 Sistema de Gestión de Puntajes")

# --- Lógica de la aplicación ---

if st.session_state.logged_in_user:
    if st.session_state.logged_in_user == 'admin':
        # --- Panel de administrador ---
        st.subheader(f"Bienvenido Administrador: {st.session_state.logged_in_user}!")
        st.divider()

        admin_tab1, admin_tab2 = st.tabs(["Dashboard", "Gestión de Usuarios"])

        with admin_tab1:
            st.markdown("### Dashboard de Administración")
            
            users_scores = [data['score'] for u, data in st.session_state.users_db.items() if u != 'admin']

            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Usuarios", len(users_scores))
            col2.metric("Puntaje Promedio", f"{sum(users_scores) / len(users_scores) if users_scores else 0:.2f}")
            col3.metric("Puntaje Total", sum(users_scores))

            st.divider()

            if users_scores:
                highest_score = max(users_scores)
                users_with_highest_score = [u for u, data in st.session_state.users_db.items() if data['score'] == highest_score and u != 'admin']
                
                lowest_score = min(users_scores)
                users_with_lowest_score = [u for u, data in st.session_state.users_db.items() if data['score'] == lowest_score and u != 'admin']

                st.info(f"**Puntaje Más Alto:** {highest_score} (Usuarios: {', '.join(users_with_highest_score)})")
                st.info(f"**Puntaje Más Bajo:** {lowest_score} (Usuarios: {', '.join(users_with_lowest_score)})")
            else:
                st.warning("No hay usuarios registrados para mostrar estadísticas (excepto el administrador).")

        with admin_tab2:
            st.markdown("### Gestión de Usuarios")

            st.write("**Usuarios Registrados:**")
            users_for_display = {u: data['score'] for u, data in st.session_state.users_db.items() if u != 'admin'}
            if users_for_display:
                st.dataframe(users_for_display)

                st.divider()
                st.markdown("### Gestionar Usuario Específico")
                # Selección de usuario para gestionar
                user_to_manage = st.selectbox(
                    "Selecciona un usuario para gestionar:",
                    options=[u for u in st.session_state.users_db.keys() if u != 'admin']
                )

                if user_to_manage:
                    st.write(f"**Gestionando a: {user_to_manage}** (Puntaje actual: {st.session_state.users_db[user_to_manage]['score']})")
                    
                    # Actualizar puntaje
                    new_score_admin = st.number_input(f"Nuevo puntaje para {user_to_manage}", value=st.session_state.users_db[user_to_manage]['score'], min_value=0, key=f"admin_new_score_{user_to_manage}")
                    if st.button(f"Actualizar Puntaje de {user_to_manage}", key=f"admin_update_score_{user_to_manage}"):
                        update_score_st(user_to_manage, new_score_admin)
                        st.rerun()

                    # Restablecer puntaje
                    if st.button(f"Restablecer Puntaje de {user_to_manage} a 0", key=f"admin_reset_score_{user_to_manage}"):
                        reset_user_score_st(user_to_manage)
                        st.rerun()

                    # Eliminar usuario
                    if st.button(f"Eliminar Usuario {user_to_manage}", key=f"admin_delete_user_{user_to_manage}"):
                        delete_user_st(user_to_manage)
                        st.rerun()
            else:
                st.info("No hay usuarios registrados para gestionar (excepto el administrador).")

        st.divider()
        # Opción para cerrar sesión del administrador
        if st.button("Cerrar Sesión de Administrador", key="admin_logout_btn"):
            logout_user_st()
            st.rerun()

    else:
        # Si el usuario está logueado (y NO es el administrador)
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

file_content = """
import streamlit as st

# --- Funciones del sistema adaptadas para Streamlit ---
# Se asume que users_db y logged_in_user son manejados por st.session_state

def register_user_st(username, password):
    if username in st.session_state.users_db:
        st.error(f"El usuario '{username}' ya existe. Por favor, elige otro. " +
                 "Si eres administrador, puedes gestionar usuarios existentes en el panel de administrador.")
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
    if username in st.session_state.users_db and username != 'admin': # No actualizar score del admin directamente
        st.session_state.users_db[username]['score'] = new_score
        st.success(f"Puntaje de {username} actualizado a {new_score}.")
    elif username == 'admin':
        st.warning("No se puede actualizar el puntaje del usuario administrador.")
    else:
        st.error(f"El usuario '{username}' no existe.")

def reset_user_score_st(username):
    if username in st.session_state.users_db and username != 'admin':
        st.session_state.users_db[username]['score'] = 0
        st.success(f"El puntaje de '{username}' ha sido restablecido a 0.")
    elif username == 'admin':
        st.warning("No se puede restablecer el puntaje del usuario administrador.")
    else:
        st.error(f"El usuario '{username}' no existe.")

def delete_user_st(username):
    if username in st.session_state.users_db:
        if username == 'admin':
            st.error("No se puede eliminar el usuario administrador.")
            return False
        del st.session_state.users_db[username]
        st.success(f"Usuario '{username}' eliminado exitosamente.")
        if st.session_state.logged_in_user == username:
            st.session_state.logged_in_user = None
            st.info("Sesión cerrada para el usuario eliminado.")
        return True
    else:
        st.error(f"El usuario '{username}' no existe y no puede ser eliminado.")
        return False

# --- Configuración y Diseño de la interfaz de usuario con Streamlit ---

st.set_page_config(layout="centered", page_title="Sistema de Puntajes")
st.title("🎮 Sistema de Gestión de Puntajes")

# Inicialización del estado de la sesión si no existe
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
# Añadir un usuario administrador para demostración
if 'admin' not in st.session_state.users_db:
    st.session_state.users_db['admin'] = {'password': 'adminpass', 'score': -1} # Score -1 para admin


# --- Lógica de la aplicación ---

if st.session_state.logged_in_user:
    if st.session_state.logged_in_user == 'admin':
        # --- Panel de administrador ---
        st.subheader(f"Bienvenido Administrador: {st.session_state.logged_in_user}!")
        st.divider()

        admin_tab1, admin_tab2 = st.tabs(["Dashboard", "Gestión de Usuarios"])

        with admin_tab1:
            st.markdown("### Dashboard de Administración")
            
            users_scores = [data['score'] for u, data in st.session_state.users_db.items() if u != 'admin']

            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Usuarios", len(users_scores))
            col2.metric("Puntaje Promedio", f"{sum(users_scores) / len(users_scores) if users_scores else 0:.2f}")
            col3.metric("Puntaje Total", sum(users_scores))

            st.divider()

            if users_scores:
                highest_score = max(users_scores)
                users_with_highest_score = [u for u, data in st.session_state.users_db.items() if data['score'] == highest_score and u != 'admin']
                
                lowest_score = min(users_scores)
                users_with_lowest_score = [u for u, data in st.session_state.users_db.items() if data['score'] == lowest_score and u != 'admin']

                st.info(f"**Puntaje Más Alto:** {highest_score} (Usuarios: {', '.join(users_with_highest_score)})")
                st.info(f"**Puntaje Más Bajo:** {lowest_score} (Usuarios: {', '.join(users_with_lowest_score)})")
            else:
                st.warning("No hay usuarios registrados para mostrar estadísticas (excepto el administrador).")

        with admin_tab2:
            st.markdown("### Gestión de Usuarios")

            st.write("**Usuarios Registrados:**")
            users_for_display = {u: data['score'] for u, data in st.session_state.users_db.items() if u != 'admin'}
            if users_for_display:
                st.dataframe(users_for_display)

                st.divider()
                st.markdown("### Gestionar Usuario Específico")
                # Selección de usuario para gestionar
                user_to_manage = st.selectbox(
                    "Selecciona un usuario para gestionar:",
                    options=[u for u in st.session_state.users_db.keys() if u != 'admin']
                )

                if user_to_manage:
                    st.write(f"**Gestionando a: {user_to_manage}** (Puntaje actual: {st.session_state.users_db[user_to_manage]['score']})")
                    
                    # Actualizar puntaje
                    new_score_admin = st.number_input(f"Nuevo puntaje para {user_to_manage}", value=st.session_state.users_db[user_to_manage]['score'], min_value=0, key=f"admin_new_score_{user_to_manage}")
                    if st.button(f"Actualizar Puntaje de {user_to_manage}", key=f"admin_update_score_{user_to_manage}"):
                        update_score_st(user_to_manage, new_score_admin)
                        st.rerun()

                    # Restablecer puntaje
                    if st.button(f"Restablecer Puntaje de {user_to_manage} a 0", key=f"admin_reset_score_{user_to_manage}"):
                        reset_user_score_st(user_to_manage)
                        st.rerun()

                    # Eliminar usuario
                    if st.button(f"Eliminar Usuario {user_to_manage}", key=f"admin_delete_user_{user_to_manage}"):
                        delete_user_st(user_to_manage)
                        st.rerun()
            else:
                st.info("No hay usuarios registrados para gestionar (excepto el administrador).")

        st.divider()
        # Opción para cerrar sesión del administrador
        if st.button("Cerrar Sesión de Administrador", key="admin_logout_btn"):
            logout_user_st()
            st.rerun()

    else:
        # Si el usuario está logueado (y NO es el administrador)
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

