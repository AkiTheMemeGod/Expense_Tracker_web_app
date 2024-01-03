import pandas as pd
from fpdf import FPDF
import os
import streamlit as st
import time as tt
import plotly.express as px


def reset_fields():
    st.session_state["type1"] = None
    st.session_state["amt"] = None
    st.session_state["desc"] = None


def track(cat: str, typ: str, amt: str, desc: str):
    if amt.startswith("0"):
        amt = amt[1:]

    if not all([cat, typ, amt, desc]):
        st.warning("Please fill in all fields before adding an entry.")
        return

    rd_csv(d=int(tt.strftime("%d")), m=tt.strftime("%B"), c=cat, t=typ, a=int(amt), des=desc)


def get_types(filepath):
    """This function helps to read the todos you enter into a text file"""
    try:
        with open(filepath, 'r') as file:
            todos = file.readlines()
        return todos
    except FileNotFoundError:
        open("dependencies/passds.txt", "w+")

def put_todos(tds, filepath):
    """This function helps to put the todos you enter into a text file"""
    with open(filepath, 'w') as file:
        file.writelines(tds)


def wrt_csv(date: list, month: list, cat: list, typ: list, amt: list, desc: list):

    data = {
        "Date": date,
        "Month": month,
        "Category": cat,
        "Type": typ,
        "Amount": amt,
        "Description": desc
    }
    df = pd.DataFrame(data)
    df.to_csv(path_or_buf=st.session_state.user_csv, index=False, index_label=None)


def rd_csv(d: int, m, c, t, a: int, des: str):
    try:
        x = pd.read_csv(filepath_or_buffer=st.session_state.user_csv, sep=",")

        date = list(x["Date"])
        month = list(x["Month"])
        cat = list(x["Category"])
        typ = list(x["Type"])
        amt = list(x["Amount"])
        desc = list(x["Description"])

        date.append(d)
        month.append(m)
        cat.append(c)
        typ.append(t)
        amt.append(a)
        desc.append(des)
        x.reset_index(drop=True, inplace=True)
        x.to_csv(st.session_state.user_csv, index=False, index_label=None)
        wrt_csv(date, month, cat, typ, amt, desc)
    except AttributeError:

        st.error("Login to save your inputs", icon="⚠️")


def generate_pdf(df):
    # df = pd.read_csv(filepath_or_buffer=st.session_state.user_csv, sep=",", index_col=None)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    pdf.set_font(family="Times", size=40, style="B")
    pdf.image(name="Untitled design.png", type="png", w=30, h=30, link="https://spend-it.streamlit.app")
    pdf.cell(w=20, h=10, txt='', align="C", ln=1)
    pdf.cell(w=20, h=10, txt='', align="C", ln=1)
    pdf.cell(w=20, h=10, txt='', align="C", ln=1)
    pdf.cell(w=20, h=10, txt='', align="C", ln=1)

    pdf.set_text_color(243, 18, 18)
    pdf.text(txt="$pend-It.", x=75, y=20)

    pdf.set_text_color(100, 100, 100)
    pdf.set_font(family="Times", size=20, style="B")
    pdf.text(txt="Expense Report", x=77, y=35)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family="Times", size=18, style="B")
    pdf.text(txt=st.session_state.username, x=156, y=25)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family="Times", size=18, style="B")
    pdf.text(txt=tt.strftime("Date : %d/%m/%y"), x=165, y=35)
    pdf.line(x1=10, x2=200, y1=45, y2=45)

    pdf.set_font(family="times", size=25, style="B")
    pdf.set_text_color(50, 50, 50)
    pdf.cell(w=20, h=10, txt='Date', align="C")

    pdf.cell(w=50, h=10, txt='Month', align="C")
    pdf.cell(w=40, h=10, txt='Category', align="C")
    pdf.cell(w=55, h=10, txt='Type', align="C")
    pdf.cell(w=32, h=10, txt='Amount', ln=1, align="C")
    pdf.cell(w=20, h=3, txt='', align="C")
    pdf.cell(w=50, h=3, txt='', align="C")
    pdf.cell(w=40, h=3, txt='', align="C")
    pdf.cell(w=55, h=3, txt='', align="C")
    pdf.cell(w=32, h=3, txt='', ln=1, align="C")

    for index, row in df.iterrows():
        try:
            pdf.set_font(family="Times", size=25)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(w=20, h=10, txt=str(row['Date']), border=1, align="C")
            pdf.cell(w=50, h=10, txt=str(row['Month']), border=1, align="C")
            pdf.cell(w=40, h=10, txt=str(row['Category']), border=1, align="C")
            pdf.set_font(family="Times", size=15)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(w=55, h=10, txt=str(row['Type']), border=1, align="C")
            pdf.set_font(family="Times", size=25)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(w=32, h=10, txt=str(row['Amount']), border=1, ln=1, align="C")
        except KeyError:
            pass
    try:
        total_income = str(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][1])
        total_expense = str(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][0])


        pdf.set_font(family="Times", size=25, style="B")
        pdf.cell(w=20, h=3, txt='', align="C")
        pdf.cell(w=50, h=3, txt='', align="C")
        pdf.cell(w=40, h=3, txt='', align="C")
        pdf.cell(w=55, h=3, txt='', align="C")
        pdf.cell(w=32, h=3, txt='', ln=1, align="C")
        pdf.set_text_color(33, 179, 42)
        pdf.cell(w=20, h=10, txt='', align="C")
        pdf.cell(w=50, h=10, txt='', align="C")
        pdf.cell(w=40, h=10, txt='Total', align="R")
        pdf.cell(w=55, h=10, txt='Income : ', align="L")
        pdf.cell(w=32, h=10, txt=total_income, ln=1, align="L")
        pdf.set_font(family="Times", size=25, style="B")

        pdf.cell(w=20, h=3, txt='', align="C")
        pdf.cell(w=50, h=3, txt='', align="C")
        pdf.cell(w=40, h=3, txt='', align="C")
        pdf.cell(w=55, h=3, txt='', align="C")
        pdf.cell(w=32, h=3, txt='', ln=1, align="C")
        pdf.set_text_color(255, 0, 0)
        pdf.cell(w=20, h=10, txt='', align="C")
        pdf.cell(w=50, h=10, txt='', align="C")
        pdf.cell(w=40, h=10, txt='Total', align="R")
        pdf.cell(w=55, h=10, txt='Expense : ', align="L")
        pdf.cell(w=32, h=10, txt=total_expense, ln=1, align="L")
    except Exception:
        pass
    pdf.output(st.session_state.user_pdf)

    with open(st.session_state.user_pdf, "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    os.remove(st.session_state.user_pdf)
    return PDFbyte


def save_pfp(uploadedfile, dest):
    path = os.path.join(dest, uploadedfile.name)
    with open(path, "wb") as f:
        f.write(uploadedfile.getbuffer())

    rename_image(path, os.path.join(dest, "pfp.png"))


def rename_image(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"File renamed from {old_name} to {new_name}")
    except FileNotFoundError:
        print(f"The file {old_name} does not exist.")
    except FileExistsError:
        print(f"The file {new_name} already exists.")
