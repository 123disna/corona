from tkinter import *
from tkinter import messagebox,filedialog
import requests
from bs4 import BeautifulSoup
import plyer

def dataCollect():
    def notification(title,message):
        plyer.notification.notify(
            title=title,
            message=message,
            timeout=15
        )

    url="https://www.worldometers.info/coronavirus/"           #scrap data from worldometer
    res=requests.get(url)
    soup=BeautifulSoup(res.content,'html.parser')
    tbody=soup.find('tbody')
    count_r=tbody.find_all('tr')
    countrynotify=cntdata.get()

    if(countrynotify==""):
        countrynotify="world"

    serial_number,countries,total_cases,new_cases,total_deaths,new_deaths,total_recovered,active_cases=[],[],[],[],[],[],[],[]
    serious_critical,total_cases_permn,total_deaths_permn,total_tests,total_test_permillion,total_pop=[],[],[],[],[],[]

    header=['serial_number','countries','total_cases','new_cases','total_deaths','new_deaths','total_recovered','active_cases',
        'serious_critical','total_cases_permn','total_deaths_permn','total_tests','total_test_permillion','total_pop']
    for i in count_r:
        id=i.find_all_next('td')
        if(id[1].text.strip().lower()==countrynotify):
            totalcases=id[2].text.strip()
            newcases=id[3].text.strip()
            totaldeaths=id[4].text.strip()
            newdeaths=id[5].text.strip()
            notification("CORONA RECENT UPDATES {}".format(countrynotify),
                         "Total cases : {}\nNew cases : {}\nTotal deaths : {}\nNew deaths : {}".format(
                        totalcases,newcases,totaldeaths,newdeaths
                ))

        serial_number.append(id[0].text.strip())
        countries.append(id[1].text.strip())
        total_cases.append(id[2].text.strip())
        new_cases.append(id[3].text.strip())
        total_deaths.append(id[4].text.strip())
        new_deaths.append(id[5].text.strip())
        total_recovered.append(id[6].text.strip())
        active_cases.append(id[7].text.strip())
        serious_critical.append(id[8].text.strip())
        total_cases_permn.append(id[9].text.strip())
        total_deaths_permn.append(id[10].text.strip())
        total_tests.append(id[11].text.strip())
        total_test_permillion.append(id[12].text.strip())
        total_pop.append(id[13].text.strip())

    dataframe=pd.DataFrame(list(zip(serial_number,countries,total_cases,new_cases,total_deaths,new_deaths,
                                    total_recovered,active_cases,serious_critical,total_cases_permn,total_deaths_permn,
                                    total_tests,total_test_permillion,total_pop)),columns=header)

    sorts=dataframe.sort_values('total_cases',ascending=False)
    for a in flist:
        if(a=='html'):
            path2='{}/coronadata.html'.format(path)
            sorts.to_html(r'{}'.format(path2))

        if (a == 'json'):
            path2 = '{}/coronadata.json'.format(path)
            sorts.to_json(r'{}'.format(path2))

        if (a == 'csv'):
            path2 = '{}/coronadata.csv'.format(path)
            sorts.to_csv(r'{}'.format(path2))

        if(len(flist) != 0):
            messagebox.showinfo('Notification','Corona Record is saved {}'.format(path2),parent=root)

def downloaddata():
    global path
    if(len(flist) != 0):
        path=filedialog.askdirectory()
    else:
        pass
    dataCollect()
    flist.clear()
    Inhtml.configure(state='normal')
    Injson.configure(state='normal')
    Incsv.configure(state='normal')

def inhtmldownload():
    flist.append('html')
    Inhtml.configure(state='disabled')

def injsondownload():
    flist.append('json')
    Injson.configure(state='disabled')

def inexceldownload():
    flist.append('csv')
    Incsv.configure(state='disabled')


import pandas as pd
root=Tk()
root.title("Corona Virus")
root.configure(bg="#008000")
root.geometry('800x500')
root.resizable(False,False)
image_icon=PhotoImage(file="corona1.png")
root.iconphoto(False,image_icon)
flist=[]
path=''


label1=Label(root,text="Corona Virus Live Tracker",font=('Times new roman',30,'bold'),bg="#008000",fg="white")
label1.place(x=150,y=0)

label1=Label(root,text="Country Name",font=('arial',20,'bold'),bg="#008000",fg="yellow")
label1.place(x=50,y=70)

cntdata=StringVar()
entry1=Entry(root,textvariable=cntdata,justify='center',font=('arial',20,'bold'),bg="white",fg="black",width=30,border=5)
entry1.place(x=300,y=70)

label2=Label(root,text="Download File in",font=('arial',20,'bold'),bg="#008000",fg="yellow")
label2.place(x=50,y=140)

button1=Button(root,text="HTML",bg="#02023E",fg="white",width=6,font=("arial",15,"bold"),activebackground="white",activeforeground="#02023E",command=inhtmldownload)
button1.place(x=300,y=140)

button2=Button(root,text="JSON",bg="#02023E",fg="white",width=6,font=("arial",15,"bold"),activebackground="white",activeforeground="#02023E",command=injsondownload)
button2.place(x=300,y=200)

button1=Button(root,text="EXCEL",bg="#02023E",fg="white",width=6,font=("arial",15,"bold"),activebackground="white",activeforeground="#02023E",command=inexceldownload)
button1.place(x=300,y=260)

button3=Button(root,text="SUBMIT",bg="#FF0945",fg="white",width=10,font=("arial",15,"bold"),activebackground="white",activeforeground="#FF0945",command=downloaddata)
button3.place(x=500,y=200)

root.mainloop()