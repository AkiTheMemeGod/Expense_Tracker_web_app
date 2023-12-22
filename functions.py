import time as t
def get_types(filepath="income_types.txt"):
    """This function helps to read the todos you enter into a text file"""
    with open(filepath, 'r') as file:
        todos = file.readlines()
    return todos



def put_todos(tds, filepath="income_types.txt"):
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


