from functions import *

# st.session_state.user_csv = f"account/{str(st.session_state.username)}/report.csv"
# st.session_state.user_pdf = f"account/{str(st.session_state.username)}/report.pdf"


def app():
    try:

        print(st.session_state.user_csv)
        df = pd.read_csv(filepath_or_buffer=st.session_state.user_csv, index_col=False)
        # st.dataframe(df, use_container_width=True)
        st.sidebar.title("🛞 FILTERS")

        month = st.sidebar.multiselect(label="Select a Month",
                                       options=df["Month"].unique(),
                                       default=df["Month"].unique(),
                                       )
        st.sidebar.markdown("---")

        category = st.sidebar.multiselect(label="Select a Category",
                                          options=df["Category"].unique(),
                                          default=df["Category"].unique(),
                                          )
        st.sidebar.markdown("---")

        exp_type = st.sidebar.multiselect(label="Select a Type",
                                          options=df["Type"].unique(),
                                          default=df["Type"].unique(),
                                          )
        color = '#da7070'
        df_selection = df.query(
            "Month == @month & Category == @category & Type == @exp_type")

        with st.container(border=True):
            st.title("Report")
            st.dataframe(df_selection, use_container_width=True)

        PDFbyte = generate_pdf()
        st.sidebar.markdown("---")
        clicked = st.sidebar.download_button(label="Download Report",
                                             data=PDFbyte,
                                             file_name=st.session_state.user_pdf,
                                             mime='application/octet-stream',
                                             on_click=generate_pdf,
                                             use_container_width=True)
        if clicked: st.sidebar.success("Downloaded Successfully")


        with st.container(border=True):
            st.title("Your Expenditure Spree :")
            st.markdown("#")
            st.markdown("#")

            col1, col2, col3 = st.columns(3)

            with col1:
                df_selection = df_selection.rename(
                    columns={'Type': 'index'}
                ).set_index('index')
                st.bar_chart(df_selection['Amount'],
                             color=color)
            with col2:
                st.markdown("#")
                df_selection = df_selection.rename(
                    columns={'Category': 'index'}
                ).set_index('index')
                st.bar_chart(df_selection['Amount'],
                             color=color)
            with col3:
                df_selection = df_selection.rename(
                    columns={'Date': 'index'}
                ).set_index('index')
                st.line_chart(df_selection['Amount'],
                              color=color)

        with st.container(border=True):

            st.title("Total:")
            st.markdown("#")
            st.markdown("#")
            try:
                total_income = int(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][1])
                total_expense = int(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][0])
                savings = total_income - total_expense
            except IndexError:
                st.error("Enter at-least one entry in Income/Expenses")
            col4, col5, col6 = st.columns(3)
            with col4:
                st.info(f"Total Income : {total_income}₹")
            with col5:
                st.info(f"Total Savings : {total_expense}₹")
            with col6:
                if savings < 0:
                    st.error(f"Savings : {savings}₹")
                if savings == 0:
                    st.warning(f"Savings : {savings}₹")
                if savings > 0:
                    st.success(f"Savings : {savings}₹")
    except AttributeError:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.error("Login to see your report", icon="⚠️")
    except FileNotFoundError:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.error("You dont have any expenses or income entries yet!", icon="⚠️")
