import pandas as pd
from fpdf import FPDF


def get_types(filepath):
    """This function helps to read the todos you enter into a text file"""
    with open(filepath, 'r') as file:
        todos = file.readlines()
    return todos


def put_todos(tds, filepath):
    """This function helps to put the todos you enter into a text file"""
    with open(filepath, 'w') as file:
        file.writelines(tds)


def send_mail(msg):
    import smtplib as sm
    # = "This
    s = sm.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('akis.pwdchecker@gmail.com', 'tjjqhaifdobuluhg')
    s.sendmail('akis.pwdchecker@gmail.com', 'k.akashkumar@gmail.com', msg=msg)


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
    df.to_csv("report.csv",index=False,index_label=None)


def rd_csv(d: int, m, c, t, a: int, des: str):
    x = pd.read_csv("report.csv", sep=",")

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
    x.reset_index(drop=True,inplace=True)
    x.to_csv("report.csv",index=False,index_label=None)
    wrt_csv(date, month, cat, typ, amt, desc)


def create_report():
    df = pd.read_csv("report.csv", sep=",")
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    for index, row in df.iterrows():
        pdf.set_font(family="Times", style="B", size=24)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(w=0, h=12, text=row["Type"]) #, align="L")

    pdf.output("report.pdf")


def wrt_acc(usrs: list, pwds: list, emails: list):

    data = {
        "Email": emails,
        "Usernames": usrs,
        "Passwords": pwds,
    }
    df = pd.DataFrame(data)
    df.to_csv("dependencies/accounts.csv", index=False, index_label=None)


def rd_acc(u: str, p: str, e: str):
    x = pd.read_csv("dependencies/accounts.csv", sep=",")

    email = list(x["Email"])
    usrs = list(x["Usernames"])
    pwds = list(x["Passwords"])

    email.append(e)
    usrs.append(u)
    pwds.append(p)

    x.reset_index(drop=True,inplace=True)
    x.to_csv("dependencies/accounts.csv",index=False,index_label=None)
    wrt_acc(usrs, pwds, email)


def fetch_acc():
    x = pd.read_csv("dependencies/accounts.csv", sep=",")

    email = list(x["Email"])
    usrs = list(x["Usernames"])
    pwds = list(x["Passwords"])

    return email, usrs, pwds