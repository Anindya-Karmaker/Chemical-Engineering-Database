import re
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import sqlite3
import tkinter as Tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import string
conn=sqlite3.connect('IR_DATA.sqlite')
cur=conn.cursor()   
ir_fg=[]#FUNCTIONAL GROUP STORAGE 
ir_vib=['all','stretching', 'bending']#TYPE OF VIBRATION
ir_vib_type='all'
ir_func_type='all'
cm=0
dat_check=0
cmdlineq=''
statement=''
list_item=''
def ir_func_group():
    global ir_fg
    global statement
    try:
        cmdlineq="SELECT * FROM IR_DATA"
        row=cur.fetchone()
        for row in cur.execute(cmdlineq):
               ir_fg.append(str(row[6]))
        ir_fg = list(dict.fromkeys(ir_fg))
        ir_fg.sort()
        ir_fg.insert(0,'all')
    except:
        statement="NO DATABASE FOUND PLEASE UPDATE DATABASE!"
def update_ir_db():
    ctx=ssl.create_default_context()
    ctx.check_hostname=False
    ctx.verify_mode=ssl.CERT_NONE
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    url='https://chem.libretexts.org/Bookshelves/Ancillary_Materials/Reference/Reference_Tables/Spectroscopic_Parameters/Infrared_Spectroscopy_Absorption_Table'
    temp=urllib.request.Request(url,None, headers)
    html = urllib.request.urlopen(temp, context=ctx).read()
    print("DONE DOWNLOADING")
    soup = BeautifulSoup(html, 'html.parser')
    tables=soup.find_all("table")
    command1="DROP TABLE IF EXISTS IR_DATA"
    command2="CREATE TABLE " +"IR_DATA"+" (wavenumber_upper INTEGER, wavenumber_lower INTEGER,intensity TEXT, peak TEXT, functional_group TEXT,type_of_vibration TEXT, group_name TEXT,other TEXT)"
    cur.execute(command1)
    cur.execute(command2)
    for i in range(len(tables)):
        group=tables[i].find('tbody').find_all('tr')    
        for j in range(len(group)):
            wavenumber_range=group[j].find_all('th')[0].get_text().split('\n')
            if(len(wavenumber_range)==1):
                if(len(wavenumber_range[0].split('-'))==2):
                    wavenumber_upper=wavenumber_range[0].split('-')[0].strip("()")
                    wavenumber_lower=wavenumber_range[0].split('-')[1].strip("()")
                else:
                    if("±" in wavenumber_range[0].strip().strip("()")):
                        val=wavenumber_range[0].strip().strip("()").split("±")[1]
                        wavenumber_upper=int(wavenumber_range[0].strip().strip("()").split("±")[0])+int(val)
                        wavenumber_lower=int(wavenumber_range[0].strip().strip("()").split("±")[0])-int(val)
                    else:
                        wavenumber_upper=wavenumber_range[0].strip().strip("()")
                        wavenumber_lower=wavenumber_upper
                intensity=group[j].find_all('td')[0].get_text()
                peak=group[j].find_all('td')[1].get_text()
                functional_group=group[j].find_all('td')[2].get_text()
                type_of_vibration=group[j].find_all('td')[3].get_text() 
                group_name=group[j].find_all('td')[4].get_text().replace('\n','').replace('           ','')
                other=group[j].find_all('td')[5].get_text().replace('\n','').replace('           ','')
                
                row=cur.fetchone()
                if row is None:
                    command3="INSERT INTO " +"IR_DATA"+" (wavenumber_upper, wavenumber_lower,intensity, peak, functional_group,type_of_vibration, group_name,other) VALUES(?,?,?,?,?,?,?,?)"
                    cur.execute(command3, (wavenumber_upper,wavenumber_lower,intensity,peak,functional_group,type_of_vibration,group_name,other))
            elif(len(wavenumber_range)>1):
                for k in range(len(wavenumber_range)):
                    if(len(wavenumber_range[0].split('-'))==2):
                        wavenumber_upper=wavenumber_range[k].split('-')[0].strip().strip("()")
                        wavenumber_lower=wavenumber_range[k].split('-')[1].strip().strip("()")
                    else:
                        if("±" in wavenumber_range[k].strip().strip("()")):
                            val=wavenumber_range[k].strip().strip("()").split("±")[1]
                            wavenumber_upper=int(wavenumber_range[k].strip().strip("()").split("±")[0])+int(val)
                            wavenumber_lower=int(wavenumber_range[k].strip().strip("()").split("±")[0])-int(val)
                        else:
                            wavenumber_upper=wavenumber_range[k].strip().strip("()")
                            wavenumber_lower=wavenumber_upper
                    intensity=group[j].find_all('td')[0].get_text()
                    peak=group[j].find_all('td')[1].get_text()
                    functional_group=group[j].find_all('td')[2].get_text()
                    type_of_vibration=group[j].find_all('td')[3].get_text()
                    group_name=group[j].find_all('td')[4].get_text().replace('\n','').replace('           ','')
                    other=group[j].find_all('td')[5].get_text().replace('\n','').replace('           ','')
                    row=cur.fetchone()
                    if row is None:
                        command3="INSERT INTO " +"IR_DATA"+" (wavenumber_upper, wavenumber_lower,intensity, peak, functional_group,type_of_vibration, group_name,other) VALUES(?,?,?,?,?,?,?,?)"
                        cur.execute(command3, (wavenumber_upper,wavenumber_lower,intensity,peak,functional_group,type_of_vibration,group_name,other))
        conn.commit()
    ir_func_group()

    
def interface_user():
    global statement
    global cm
    window = Tk()
    window.geometry("870x350")
    window.title("CHEMICAL ENGINEERING TOOLKIT")
    window.resizable(False, False)
    TC= ttk.Notebook(window)
    ESTIMATE = ttk.Frame(TC) 
    INFO = ttk.Frame(TC) 
    TC.add(ESTIMATE, text='Infrared Spectroscopy')     
    TC.add(INFO, text='Information')
    TC.pack(expand=1, fill="both") 
    IR_ESTIMATE=Frame(ESTIMATE)
    IR_ESTIMATE.pack()
    infoview=Frame(INFO)
    infoview.pack()
    lbl5 = Label(infoview, text="CHEMICAL ENGINEERING TOOLKIT V1.1", font=("Arial Bold", 14))
    lbl5.pack(fill=X)
    lbl6 = Label(infoview, text="Software Created by Anindya Karmker", font=("Arial Bold", 12))
    lbl6.pack(fill=X)
    lbl6 = Label(infoview, text="DATABASE PROVIDER", font=("Arial Bold", 14))
    lbl6.pack(fill=X)
    lble1 = ScrolledText(infoview, font=("Arial Bold", 12))
    lble1.insert(INSERT,"https://chem.libretexts.org/Bookshelves/Ancillary_Materials/Reference/Reference_Tables/Spectroscopic_Parameters/Infrared_Spectroscopy_Absorption_Table")
    lble1.config(width=860,height=2)
    lble1.config(state='disabled')
    lble1.pack(fill=X)

    enteroption = Frame(IR_ESTIMATE)
    enteroption.grid(row=0,column=0, padx=5,pady=5,sticky=N)
    optlabel=Label(enteroption, text="IR wavenumber (per cm)", justify='center',font=("Arial", 13,"bold")).pack(side=TOP)
    option=Entry(enteroption, width=25,font=("Arial", 12))
    option.pack(anchor=NW,fill="x")
    solve_ir=Button(enteroption, text="Estimate Functional Group", font=("Arial", 13,"bold"), height=1, width=23)
    solve_ir.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    updatedb=Button(enteroption, text="Update Database", font=("Arial", 13,"bold"), height=1, width=23)
    updatedb.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    help1=Button(enteroption, text="Help", font=("Arial", 13,"bold"), height=1, width=23)
    help1.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    typevib=Frame(IR_ESTIMATE)
    typevib.grid(row=0,column=2,padx=5,pady=5,sticky=N)
    lb1=Label(typevib, text="Choose Type of Vibration", justify='center',font=("Arial", 13,"bold")).pack(side=TOP)
    listvib = Listbox(typevib, width=23, height=8, justify='center',font=("Helvetica", 12),selectmode=BROWSE,exportselection=False)
    listvib.pack(side=LEFT, fill="x")
    typeir_fg=Frame(IR_ESTIMATE)
    typeir_fg.grid(row=0,column=1,padx=5,pady=5,sticky=N)
    lb1=Label(typeir_fg, text="Choose Chemical Group",justify='center', font=("Arial", 13,"bold")).pack(side=TOP)
    option2=Entry(typeir_fg, width=23,font=("Arial", 12))
    option2.pack(side=TOP, anchor=NW,fill="x")
    search=Button(typeir_fg, text="Search", font=("Arial", 13,"bold"), height=1, width=23)
    search.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    
    listfunc = Listbox(typeir_fg, width=40, height=5,justify='center', font=("Helvetica", 12),selectmode=BROWSE,exportselection=False)
    listfunc.pack(side=LEFT, fill="x")
    scrollbar = Scrollbar(typeir_fg, orient="vertical")
    scrollbar.config(command=listfunc.yview)
    scrollbar.pack(side=RIGHT,anchor=N, fill="y")
    lbdisp=ScrolledText(ESTIMATE,width=300, height=10,padx=5,pady=5,font=("Arial", 12))
    lbdisp.pack(side=LEFT,fill='none')      
    lbdisp.configure(state='disabled')
    while cm!=1:
        ir_func_group() 
        listfunc.delete('0','end')
        for items in range(len(ir_vib)):
            listvib.insert(items, ir_vib[items])
        for items in range(len(ir_fg)):
            listfunc.insert(items, ir_fg[items])
        lbdisp.configure(state='normal')
        lbdisp.delete('1.0', END)
        lbdisp.insert(INSERT,statement)
        lbdisp.configure(state='disabled')
        cm=1 
    def ir_update():
        update_ir_db()
        lbdisp.configure(state='normal')
        listfunc.delete('0','end')
        for items in range(len(ir_fg)):
            listfunc.insert(items, ir_fg[items])
        statement="---------------DATABASE STATUS---------------\nDATABASE UPDATED SUCCESSFULLY\n"+'-'*60
        lbdisp.delete('1.0', END)
        lbdisp.insert(INSERT,statement)
        lbdisp.configure(state='disabled')
        print(statement)
    def ir_vib_type_choosen(evt):
        global ir_vib_type
        ir_vib_type=str((listvib.get(ANCHOR)))
    def ir_func_type_choosen(evt):
        global ir_func_type
        ir_func_type=str((listfunc.get(ANCHOR)))
    def solvefunc():
        lbdisp.configure(state='normal')
        x=option.get()
        if(x==''):
            x=0
        global statement
        global dat_check
        global ir_vib_type
        global ir_func_type
        lbdisp.delete('1.0', END)
        global cmdlineq
        dat_check=0
        if(ir_vib_type=='all' and ir_func_type=='all' or ir_func_type==''):
            cmdlineq="SELECT * FROM IR_DATA WHERE wavenumber_upper>="+str(x)+" AND wavenumber_lower<="+str(x)
        elif(ir_vib_type!='all' and ir_func_type=='all'):
            cmdlineq="SELECT * FROM IR_DATA WHERE type_of_vibration='"+str(ir_vib_type)+"' AND wavenumber_upper>="+str(x)+" AND wavenumber_lower<="+str(x)
        elif(ir_vib_type=='all' and ir_func_type!='all'):
            cmdlineq="SELECT * FROM IR_DATA WHERE group_name='"+str(ir_func_type)+"' AND wavenumber_upper>="+str(x)+" AND wavenumber_lower<="+str(x)
        elif(ir_vib_type!='all' and ir_func_type!='all'):
            cmdlineq="SELECT * FROM IR_DATA WHERE type_of_vibration='"+str(ir_vib_type)+"' AND group_name='"+str(ir_func_type)+"' AND wavenumber_upper>="+str(x)+" AND wavenumber_lower<="+str(x) 
        
        for row in cur.execute(cmdlineq):
            statement="---------------------------------------------------\n"+"WAVENUMBER RANGE: "+str(row[0])+"-"+str(row[1])+"\n"+"FUNCTIONAL GROUP: "+str(row[4])+"\n"+"TYPE OF VIBRATION: "+str(row[5]).upper()+"\n"+"PROBABLE CHEMICAL GROUP: "+str(row[6]).upper()+"\n"+"OTHER PROPERTY: "+str(row[7]).upper()+"\n"
            print(statement)
            lbdisp.insert(INSERT,statement)
            dat_check+=1;
        if(dat_check<1):
            statement="NO DATA FOUND WITHIN RANGE"
            print(statement)
            lbdisp.insert(INSERT,statement)
        statement="\n---------------------------------------------------\n"+'TOTAL NUMBER OF MATCHES: '+str(dat_check).zfill(2)+"\n---------------------------------------------------"
        lbdisp.insert(INSERT,statement)
        lbdisp.configure(state='disabled')
    solve_ir.configure(command=solvefunc)
    def ir_new_list_find(event):
        listfunc.delete('0','end')
        global list_item
        global ir_fg
        list_item=option2.get()
        indices = [i for i, s in enumerate(ir_fg) if list_item in s]
        new_list=list()
        for i in indices:
            new_list.append(ir_fg[i])
        for items in range(len(new_list)):
            listfunc.insert(items, new_list[items])
    def ir_help_me():
        lbdisp.configure(state='normal')
        lbdisp.delete('1.0', END)
        statement='-'*50+"HELP"+'-'*50+"\nEnter the infrared spectrum wavenumber. Then select Estimate Functional Group button to show the corresponding matching functional groups. You can also limit the chemical group and type of vibration by choosing the options from the listbox. Once in a year or two, you can update the database for any new compounds\n"+'-'*51+"END"+'-'*51
        lbdisp.insert(INSERT,statement)
        lbdisp.configure(state='disabled')
    help1.configure(command=ir_help_me)
    updatedb.configure(command=ir_update)
    option2.bind('<Key-Return>',ir_new_list_find)
    listvib.bind('<<ListboxSelect>>',ir_vib_type_choosen)
    listfunc.bind('<<ListboxSelect>>',ir_func_type_choosen)
    search.bind('<Button-1>',ir_new_list_find)
    window.mainloop()


interface_user()

