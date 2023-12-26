from functions import *
import firebase_admin
# from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("dependencies/expense-tracker-769fe-56a85042b9fc.json")
# firebase_admin.initialize_app(cred)


def app():
    st.title("Your Account in $pend-it.")

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            user = auth.get_user_by_email(email)
            print(user.uid)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.user_csv = f"account/{str(st.session_state.username)}/report.csv"
            st.session_state.user_pdf = f"account/{str(st.session_state.username)}/report.pdf"

            global Usernm
            Usernm = (user.uid)

            st.session_state.signedout = True
            st.session_state.signout = True

        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ""
        st.session_state.useremail = ""
        st.session_state.user_csv = ""
        st.session_state.user_pdf = ""

        #logged_on_user_report = ""
        #  logged_on_user_pdf = ""
        # st.rerun()

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if choice == 'Sign up':
            username = st.text_input("Enter  your unique username")

            if st.button('Create my account',use_container_width=True):
                user = auth.create_user(email=email, password=password, uid=username)
                try:
                    try:
                        os.mkdir("account")
                    except:
                        pass
                    parent_path = 'account'
                    path = os.path.join(parent_path, str(user.uid))
                    print(path)
                    os.mkdir(path)
                    sh.copy("dependencies/report.csv", f"account/{str(user.uid)}")
                except:
                    pass
                st.success('Account created successfully!')
                st.success('Please Login using your email and password')
        else:
            st.button('Login', on_click=f,use_container_width=True)

    if st.session_state.signout:
        st.info(f'Name :  {str(st.session_state.username)}')
        st.info(f'E-Mail :  {str(st.session_state.useremail)}')
        st.button('Sign out', on_click=t, use_container_width=True)