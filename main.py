from functions import *
from streamlit_option_menu import option_menu
import Expenses, Income, Report, Account
from streamlit_extras.app_logo import add_logo


st.set_page_config(page_title="Spend It", layout="centered", page_icon="💵")


class Multiapp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():

        # st.title("$pend It.")

        with st.sidebar:
            c1, c2, c3 = st.sidebar.columns(3)
            with c3:
                st.sidebar.title("💵 Spend-it.")
            st.sidebar.markdown("""
                    <style>
                    .st-emotion-cache-1v0mbdj > img{
                        border-radius: 50%;

                        }
                    </style>

                    """, unsafe_allow_html=True)
            st.sidebar.image("dependencies/logo.png")
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

    run()
