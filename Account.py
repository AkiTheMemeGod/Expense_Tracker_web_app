from functions import *
import shutil as sh
import firebase_admin
from firebase_admin import credentials, auth
from dependencies.encrypter import encrypt_file, decrypt_file


cred = credentials.Certificate("dependencies/expense-tracker-769fe-56a85042b9fc.json")
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    pass

# testing Crashes and fixes
# streamlit auto update feature not working
# visibile on GitHub test

def app():
    def j():
        parent_path = 'account'
        path = os.path.join(parent_path, str(st.session_state.username))
        sh.rmtree(path)
        t()
        st.error("ACCOUNT RESETTED")

    with st.sidebar:
        st.sidebar.markdown("---")
        global new_pfp
        side_title = '<h1 style="font-family:monospace; color:#E23D9F; font-size: 35px;", align="center">🖼️DISPLAY PICTURE</h1><br>'
        st.sidebar.markdown(side_title, unsafe_allow_html=True)
        new_pfp = st.file_uploader("profile pic",type=['png', 'jpeg', ],label_visibility="hidden")
        if new_pfp is not None:
            whatfile = {"FileName": new_pfp.name, "FileType": new_pfp.type}
        st.sidebar.markdown("###")
        pfp = st.button('Change Profile Picture', use_container_width=True)
        if pfp:
            if new_pfp is not None:
                os.remove(f"account/{str(st.session_state.username)}/pfp.png")
                save_pfp(new_pfp, f"account/{str(st.session_state.username)}")
            else:
                st.sidebar.error("Upload a file to change profile pic")

        st.sidebar.markdown("---")

        side_title = '<h1 style="font-family:monospace; color:red; font-size: 35px;", align="center">🗑️DELETE ALL MY DATA</h1><br>'
        st.sidebar.markdown(side_title, unsafe_allow_html=True)
        delete = st.sidebar.button('Delete my data', use_container_width=True, type="primary")
        if delete:
            st.sidebar.button("Are you sure ?", use_container_width=True, on_click=j, type="primary")
        st.sidebar.markdown("---")
        side_title = '<h1 style="font-family:monospace; color:#E23D9F; font-size: 35px;" align="center">✒️AUTHOR</h1><br>'
        st.sidebar.markdown(side_title, unsafe_allow_html=True)

        st.sidebar.link_button("Made by Akash", url="https://akashportfolio.streamlit.app/", use_container_width=True)
        st.sidebar.link_button("Contact Me", url="https://akashportfolio.streamlit.app/Contact_Me",
                               use_container_width=True)
        st.sidebar.link_button("Application testing", url="https://www.linkedin.com/in/rohith-fernando-86225b244/",
                               use_container_width=True)

    st.title("Your :red[Account] in :green[$pend-it.]")

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''



    def f():

        try:
            user = auth.get_user_by_email(email=email)
            decrypt_file("dependencies/passds.txt")
            check_pass = []
            check_pass = get_types("dependencies/passds.txt")
            encrypt_file("dependencies/passds.txt")

            if password+"\n" not in check_pass:
                st.error("Wrong Password")
                return
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.user_csv = f"account/{str(st.session_state.username)}/report.csv"
            st.session_state.user_pdf = f"account/{str(st.session_state.username)}/report.pdf"
            st.session_state.pfp = f"account/{str(st.session_state.username)}/pfp.png"

            parent_path = 'account'
            path = os.path.join(parent_path, str(user.uid))
            print(path)
            if os.path.exists(path):

                # save_pfp(datafile, f"account/{str(user.uid)}")
                pass
            else:
                os.mkdir(path)
                # save_pfp(datafile, f"account/{str(user.uid)}")
                sh.copy("dependencies/report.csv", f"account/{str(user.uid)}")
                sh.copy("dependencies/pfp.png", f"account/{str(user.uid)}")

            global Usernm
            Usernm = user.uid

            st.session_state.signedout = True
            st.session_state.signout = True

        except Exception as e:
            st.error("Enter a Valid Email")

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ""
        st.session_state.useremail = ""
        st.session_state.user_csv = ""
        st.session_state.user_pdf = ""
        st.session_state.pfp = ""
        # logged_on_user_report = ""
        #  logged_on_user_pdf = ""

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
            global datafile
            datafile = st.file_uploader(label="Profile picture", type=['png', 'jpeg', ])
            if datafile is not None:
                file_details = {"FileName": datafile.name, "FileType": datafile.type}

            if st.button('Create my account', use_container_width=True):

                try:
                    user = auth.create_user(email=email, password=password, uid=username)

                    decrypt_file("dependencies/passds.txt")
                    passds = []

                    passds = get_types("dependencies/passds.txt")

                    password += "\n"
                    passds.append(password)
                    put_todos(passds, "dependencies/passds.txt")
                    encrypt_file("dependencies/passds.txt")

                    try:
                        try:
                            os.mkdir("account")
                        except:
                            pass
                        parent_path = 'account'
                        path = os.path.join(parent_path, str(user.uid))
                        print(path)
                        try:
                            if os.path.exists(path):
                                sh.copy("dependencies/report.csv", f"account/{str(user.uid)}")
                                save_pfp(datafile, f"account/{str(user.uid)}")

                            else:
                                os.mkdir(path)
                                sh.copy("dependencies/report.csv", f"account/{str(user.uid)}")
                                save_pfp(datafile, f"account/{str(user.uid)}")
                        except Exception:
                            if not datafile:
                                sh.copy("dependencies/pfp.png", f"account/{username}")
                        st.success('Account created successfully!')
                        st.success('Please Login using your email and password')
                    except:
                        pass
                except auth.UidAlreadyExistsError:
                    st.error("User Already Exists")

        else:
            st.button('Login', on_click=f, use_container_width=True)

    if st.session_state.signout:
        st.markdown("""
        <style>
        .st-emotion-cache-1v0mbdj > img{
            border-radius: 50%;

            }
        </style>

        """, unsafe_allow_html=True)
        st.markdown("#")
        st.markdown("#")

        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            st.image(f"account/{str(st.session_state.username)}/pfp.png", width=200, caption=st.session_state.username)
        st.markdown("#")

        with st.container(border=True):
            st.info(f'Username :  {str(st.session_state.username)}')

            st.info(f'E-Mail :  {str(st.session_state.useremail)}')
            st.button('Sign out', on_click=t, use_container_width=True)

