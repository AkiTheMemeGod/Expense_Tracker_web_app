from functions import *
from streamlit_option_menu import option_menu
import Expenses, Income, Report, Account
from streamlit_extras.app_logo import add_logo
import shutil as sh

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
        c1, c2, c3 = st.sidebar.columns([0.63, 2.5, 0.1])
        with c2:
            side_title = '<h1 style="font-family:monospace; color:red; font-size: 50px;">$pend It.</h1>'
            st.markdown(side_title, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([0.31, 2.5,0.1])
        with c2:
            original_title = '<h1 style="font-family:monospace; color:lime; font-size: 100px;">$pend It.</h1>'
            st.markdown(original_title, unsafe_allow_html=True)
        with st.sidebar:

            st.sidebar.markdown("""
                    <style>
                    .st-emotion-cache-1v0mbdj > img{
                        border-radius: 50%;

                        }
                    </style>

                    """, unsafe_allow_html=True)
            st.sidebar.image("dependencies/logo.png")
            st.sidebar.markdown("###")

            st.sidebar.markdown("---")

            side_title = '<h1 style="font-family:monospace; color:red; font-size: 50px;">₹ NAVIGATION</h1><br>'
            st.sidebar.markdown(side_title, unsafe_allow_html=True)
            option = option_menu(
                menu_title=None,
                options=["Account", "Expense", "Income", "Report"],
                orientation="vertical",
                icons=["person-fill", "cash-coin", "cash", "file-earmark-bar-graph-fill"],
                default_index=0
            )
            st.sidebar.markdown("---")
            global new_pfp
            new_pfp = st.file_uploader(label="Change Profile picture", type=['png', 'jpeg', ])
            if new_pfp is not None:
                whatfile = {"FileName": new_pfp.name, "FileType": new_pfp.type}
            pfp = st.button('Change Profile Picture', use_container_width=True)
            if pfp:
                if new_pfp is not None:
                    os.remove(f"account/{str(st.session_state.username)}/pfp.png")
                    save_pfp(new_pfp, f"account/{str(st.session_state.username)}")
                else:
                    st.sidebar.error("Upload a file to change profile pic")

            st.sidebar.markdown("---")

            side_title = '<h1 style="font-family:monospace; color:red; font-size: 35px;">DELETE ALL MY DATA</h1><br>'
            st.sidebar.markdown(side_title, unsafe_allow_html=True)
            delete = st.sidebar.button('Delete my data', use_container_width=True,type="primary")
            if delete:
                st.sidebar.button("Are you sure ?", use_container_width=True, on_click=j,type="primary")
            st.sidebar.markdown("---")
            side_title = '<h1 style="font-family:monospace; color:#E23D9F; font-size: 60px;"> ₹    AUTHOR</h1><br>'
            st.sidebar.markdown(side_title, unsafe_allow_html=True)

            st.sidebar.link_button("Made by Akash",url="https://akashportfolio.streamlit.app/", use_container_width=True)
            st.sidebar.link_button("Contact Me", url="https://akashportfolio.streamlit.app/Contact_Me",
                                   use_container_width=True)
        if option == "Account":
            Account.app()
        if option == "Expense":

            Expenses.app()

        if option == "Income":
            Income.app()

        if option == "Report":
            Report.app()
    run()
