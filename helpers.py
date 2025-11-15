import streamlit as st
import os

def require_password():
    # Als al geauthenticeerd in deze sessie, ga door
    if st.session_state.get("auth_ok"):
        return

    expected = os.getenv("APP_PASSWORD", "")
    if not expected:
        st.error("APP_PASSWORD is not configured on the server.")
        st.stop()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("imgs/logo_valident.png", width=300)

        # Gebruik een form zodat er een duidelijke knop is
        with st.form("auth_form", clear_on_submit=False):
            pw = st.text_input(
                "Voer toegangscode in",
                type="password",
                placeholder="Voer toegangscode in",
                label_visibility="hidden"
            )
            submit = st.form_submit_button("Ga verder", type="primary") 

        # Alleen valideren als er op de knop is geklikt
        if submit:
            if not pw:
                st.error("Vul eerst je toegangscode in.")
            elif pw == expected:
                st.session_state["auth_ok"] = True
                st.rerun()
            else:
                st.error("Je code is onjuist of verlopen. Vraag een nieuwe code aan via support@doodler.app.")

    st.stop()