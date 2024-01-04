import struct

import streamlit

from functions import *

#test comment to check referesh
def app():
    try:
        df = pd.read_csv(filepath_or_buffer=st.session_state.user_csv, index_col=False)
        with st.sidebar:
            st.sidebar.markdown("---")
            side_title = '<h1 style="font-family:monospace; color:red; font-size: 35px;", align="center">🎯 FILTERS</h1><br>'
            st.sidebar.markdown(side_title, unsafe_allow_html=True)
            # st.sidebar.title("₹ :rainbow[FILTERS]")

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

            PDFbyte = generate_pdf(df_selection)
            st.sidebar.markdown("---")

            clicked = st.sidebar.download_button(label=":rainbow[Download Report]",
                                                 data=PDFbyte,
                                                 file_name=st.session_state.user_pdf,
                                                 mime='application/octet-stream',
                                                 on_click=lambda: generate_pdf(df_selection),
                                                 use_container_width=True)
            if clicked:
                st.sidebar.success("Downloaded Successfully")


        with st.container(border=False):

            side_title = '<h1 style="font-family:monospace; color:#E23D9F; font-size: 60px;", align="center"><br>📃Report</h1><br><br>'
            st.markdown(side_title, unsafe_allow_html=True)
            st.dataframe(df_selection, use_container_width=False,hide_index=True,width=800)


        # with st.container(border=True):
        side_title = '<h1 style="font-family:monospace; color:#E23D9F; font-size: 65px;", align="center"><br>📈Data</h1><br><br>'
        st.markdown(side_title, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        try:
            with c1:
                expense_df = df[df['Category'] == 'Expense']

                grouped_df = expense_df.groupby('Type')['Amount'].sum().reset_index()

                result_dict = dict(zip(grouped_df['Type'], grouped_df['Amount']))
                fig1 = px.bar(grouped_df,
                             x=grouped_df["Type"],
                             y=grouped_df["Amount"],
                             labels={"x": "Expenses", "y": "How much you spent"},
                             width=230)
                st.plotly_chart(fig1)

            with c2:
                expense_df = df[df['Category'] == 'Income']

                grouped_df = expense_df.groupby('Type')['Amount'].sum().reset_index()

                result_dict = dict(zip(grouped_df['Type'], grouped_df['Amount']))
                fig2 = px.bar(grouped_df,
                             x=grouped_df["Type"],
                             y=grouped_df["Amount"],
                             labels={"x": "Income", "y": "How much you Earned"},
                             width=230)
                st.plotly_chart(fig2)

            with c3:
                expense_df = df[df['Month'] == df_selection["Month"]].reset_index()
                expense_df1 = expense_df[expense_df['Category'] == 'Expense'].reset_index()
                # grouped_df = expense_df.groupby('Type')['Amount'].reset_index()

                # result_dict = dict(zip(grouped_df['Type'], grouped_df['Amount']))
                fig3 = px.line(expense_df1,
                               x=expense_df1["Type"],
                               y=expense_df1["Amount"],
                               labels={"x": "Expenses", "y": f"How much you spent on {expense_df1['Month']}"},
                               width=230)
                st.plotly_chart(fig3)
        except Exception:
            st.error("Enter at-least one entry in Income/Expenses")

        side_title = '<h1 style="font-family:monospace; color:#E23D9F; font-size: 60px;", align="center"><br>💰Total</h1><br><br>'
        st.markdown(side_title, unsafe_allow_html=True)
        with st.container(border=True):

            try:
                total_income = int(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][1])
                total_expense = int(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][0])
                savings = total_income - total_expense

                col4, col5, col6 = st.columns(3)
                with col4:
                    st.success(f"Total Income : {total_income}₹")
                with col5:
                    st.error(f"Total Expenses : {total_expense}₹")
                with col6:
                    if savings < 0:
                        st.error(f"Total Balance : {savings}₹")
                    if savings == 0:
                        st.warning(f"Total Balance : {savings}₹")
                    if savings > 0:
                        st.success(f"Total Balance : {savings}₹")

            except FutureWarning:
                pass
            except IndexError:
                st.error("Enter at-least one entry in Income/Expenses")
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
        st.error("You dont have any expense or income entries yet!", icon="⚠️")
