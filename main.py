import streamlit
from functions import *
from streamlit_option_menu import option_menu
import Expenses, Income, Report, Account
from streamlit_extras.app_logo import add_logo
import shutil as sh
# s
st.set_page_config(page_title="Spend It", layout="centered", page_icon="💵")


def j():
    parent_path = 'account'
    path = os.path.join(parent_path, str(st.session_state.username))
    sh.rmtree(path)
    t()
    st.error("ACCOUNT RESETTED")

def t():
    st.session_state.signout = False
    st.session_state.signedout = False
    st.session_state.username = ""
    st.session_state.useremail = ""
    st.session_state.user_csv = ""
    st.session_state.user_pdf = ""

class Multiapp:


    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():

        side_title = '<h1 style="font-family:monospace; color:crimson; font-size: 45px;", align="center">$pend It.</h1>'
        st.sidebar.markdown(side_title, unsafe_allow_html=True)

        c1, c2, c3 = st.sidebar.columns([4, 1, 1])

        with c1:
            try:
                if st.session_state.username:
                    side_title = f'<h3 style="font-family:monospace; color:white; font-size: 25px;">Welcome back : {st.session_state.username}</h3>'
                    st.markdown(side_title, unsafe_allow_html=True)
            except AttributeError:
                pass
        with c2:
            try:
                if st.session_state.pfp:
                    st.markdown("""<br>
                            <style>
                            .st-emotion-cache-1v0mbdj > img{
                                border-radius: 50%;
    
                                }
                            </style>
    
                            """, unsafe_allow_html=True)
                    st.image(st.session_state.pfp, width=50)
            except Exception:
                pass
        c1, c2, c3 = st.columns([0.20, 2.5, 0.1])

        with c2:
            original_title = '<h1 style="font-family:monospace; color:lime; font-size: 100px;", align="center">$pend It.</h1>'
            st.markdown(original_title, unsafe_allow_html=True)

        with st.sidebar:

            st.sidebar.markdown("---")

            side_title = '<h1 style="font-family:monospace; color:#E23D9F; font-size: 35px;", align="center">🧭NAVIGATION</h1><br>'
            st.sidebar.markdown(side_title, unsafe_allow_html=True)
            option = option_menu(
                menu_title=None,
                options=["Account", "Expense", "Income", "Report"],
                orientation="vertical",
                icons=["person-fill", "cash-coin", "cash", "file-earmark-bar-graph-fill"],
                default_index=0
            )

        if option == "Account":
            Account.app()
        if option == "Expense":

            Expenses.app()

        if option == "Income":
            Income.app()

        if option == "Report":
            Report.app()
        # st.session_state
    run()
