import re
import urllib.request, urllib.parse, urllib.error
import ssl
import sqlite3
import tkinter as Tk
import time
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.scrolledtext import ScrolledText
import collections
import string
import random
from tabulate import tabulate
from iapws import IAPWS97
import threading
import concurrent.futures
import math
conn=sqlite3.connect('Master.db')
cur=conn.cursor()   
thermotablename=['Saturated Steam (Pressure Based)','Saturated Steam (Temperature Based)','Single Phase Property(Compressed Water and Superheated Steam)']
pressureunit=["MPa","kPa","PSI","Bar","Atm","mmHg"]
temperatureunit=["Celsius","Fahrenheit","Kelvin","Rankine"]
P_unitselection=0
T_unitselection=0
thermouserinp=0
IAPWSVER=["IAPWS'95","IAPWS'97"]
ir_fg=[]#FUNCTIONAL GROUP STORAGE 
ir_vib=['all','stretching', 'bending']#TYPE OF VIBRATION
ir_vib_type='all'
ir_func_type='all'
protein_list=[]
tempvarlow=[]
tempvarhigh=[]
tempvarinterpolate=[]
iapwsversion=95
outputunit=['SI Units','US customary Units']
chooseunit=0
ant_chem={}
crt_chem={}
critical_constants={}
antoine_constants={}
chosen_ant_chem=''
chosen_crt_chem=''
T_UNITDISP='°C'
P_UNITDISP='MPa'
ant_tmin=''
ant_tmax=''
cm=0
find_type_ant=0
find_type_crt=0
dat_check=0
cmdlineq=''
statement=''
list_item=''
readingframe=0
seqtype=0
addRE_VAL=0
sequence=""
sequencetab=0
codonseq={'UUU': 'Phe',
 'UUC': 'Phe',
 'UUA': 'Leu',
 'UUG': 'Leu',
 'CUU': 'Leu',
 'CUC': 'Leu',
 'CUA': 'Leu',
 'CUG': 'Leu',
 'AUU': 'Ile',
 'AUC': 'Ile',
 'AUA': 'Ile',
 'AUG': 'Met',
 'GUU': 'Val',
 'GUC': 'Val',
 'GUA': 'Val',
 'GUG': 'Val',
 'UCU': 'Ser',
 'UCC': 'Ser',
 'UCA': 'Ser',
 'UCG': 'Ser',
 'CCU': 'Pro',
 'CCC': 'Pro',
 'CCA': 'Pro',
 'CCG': 'Pro',
 'ACU': 'Thr',
 'ACC': 'Thr',
 'ACA': 'Thr',
 'ACG': 'Thr',
 'GCU': 'Ala',
 'GCC': 'Ala',
 'GCA': 'Ala',
 'GCG': 'Ala',
 'UAU': 'Tyr',
 'UAC': 'Tyr',
 'UAA': 'STP',
 'UAG': 'STP',
 'UGA': 'STP',
 'CAU': 'His',
 'CAC': 'His',
 'CAA': 'Gln',
 'CAG': 'Gln',
 'AAU': 'Asn',
 'AAC': 'Asn',
 'AAA': 'Lys',
 'AAG': 'Lys',
 'GAU': 'Asp',
 'GAC': 'Asp',
 'GAA': 'Glu',
 'GAG': 'Glu',
 'UGU': 'Cys',
 'UGC': 'Cys',
 'UGG': 'Trp',
 'CGU': 'Arg',
 'CGC': 'Arg',
 'CGA': 'Arg',
 'CGG': 'Arg',
 'AGA': 'Arg',
 'AGG': 'Arg',
 'AGU': 'Ser',
 'AGC': 'Ser',
 'GGU': 'Gly',
 'GGC': 'Gly',
 'GGA': 'Gly',
 'GGG': 'Gly'} 
shortseqprot={
"Ala": "A",
"Arg": "R",
"Asn": "N",
"Asp": "D",
"Cys": "C",
"Glu": "E",
"Gln": "Q",
"Gly": "G",
"His": "H",
"Ile": "I",
"Leu": "L",
"Lys": "K",
"Met": "M",
"Phe": "F",
"Pro": "P",
"Ser": "S",
"Thr": "T",
"Trp": "W",
"Tyr": "Y",
"Val": "V",
"STP":"-"}
def kj_kg_to_btu_lbm(value):
    val=float(value)*0.429922614
    return val
def m3_kg_to_ft3_lbm(value):
    val=float(value)*16.01846337
    return val
def kj_kg_k_to_btu_lbm_F(value):
    val=float(value)*0.23884589662749592
    return val
def N_M_to_lbf_in(value):
    val=float(value)*8.8507454566470800000
    return val
def m_s_to_ft_s(value):
    val=float(value)*3.2808398950131233595
    return val
def W_m_k_to_BTU_h_ft_F(value):
    val=float(value)*0.5781759824
    return val
def C_to_other(value,unit):
    try:
        if(unit==0):
            val=float(value)
        elif(unit==1):
            val=float(value)*(9/5)+32
        elif(unit==2):
            val=float(value)+273.15
        elif(unit==3):
            val=float(value)*(9/5)+491.67
        return val
    except:
        return 'N/A'
    
def Mpa_to_other(value,unit):
    try:
        val=float(value)
        if(unit==0):
            val=val
        elif(unit==1):
            val=float(value)*1000
        elif(unit==2):
            val=float(value)/0.006894757293
        elif(unit==3):
            val=float(value)*10
        elif(unit==4):
            val=float(value)*9.8692326671601283
        elif(unit==5):
            val=float(value)*7500.6157584565623439424245176757
        return val
    except:
        return 'N/A'
def P_sat_funct(Pin):
    x=[]
    hvap1=0.0
    svap1=0.0
    try:
        sat_steam=IAPWS97(P=Pin,x=1)                #saturated steam with known P
        sat_liquid=IAPWS97(P=Pin,x=0)        
        if(sat_steam.h==sat_liquid.h):
            hvap1=0.0
            svap1=0.0
        else:
            hvap1= (IAPWS97(P=Pin,x=0.2)).Hvap 
            svap1=(IAPWS97(P=Pin,x=0.2)).Svap #saturated liquid with known T   #steam with known P and T
        x.append([(float(sat_steam.T)-273.15),sat_steam.P,sat_liquid.v,sat_steam.v,sat_liquid.u,sat_steam.u,sat_liquid.h,sat_steam.h,hvap1,sat_liquid.s,sat_steam.s,svap1,sat_liquid.cp,sat_steam.cp,sat_liquid.cv,sat_steam.cv,sat_liquid.Z,sat_steam.Z,sat_liquid.w,sat_steam.w,sat_liquid.k,sat_steam.k,sat_liquid.sigma,sat_steam.sigma,sat_liquid.Prandt,sat_steam.Prandt])
    except:
        x.append("NONE")
    return x
def T_sat_funct(Tin):
    x=[]
    hvap1=0.0
    svap1=0.0
    try:
        Tin=float(Tin)+273.15        
        sat_steam=IAPWS97(T=Tin,x=1)                #saturated steam with known P
        sat_liquid=IAPWS97(T=Tin,x=0)        
        if(sat_steam.h==sat_liquid.h):
            hvap1=0.0
            svap1=0.0
        else:
            hvap1= (IAPWS97(T=Tin,x=0.2)).Hvap 
            svap1=(IAPWS97(T=Tin,x=0.2)).Svap #saturated liquid with known T
                    #steam with known P and T
        x.append([(float(sat_steam.T)-273.15),sat_steam.P,sat_liquid.v,sat_steam.v,sat_liquid.u,sat_steam.u,sat_liquid.h,sat_steam.h,hvap1,sat_liquid.s,sat_steam.s,svap1,sat_liquid.cp,sat_steam.cp,sat_liquid.cv,sat_steam.cv,sat_liquid.Z,sat_steam.Z,sat_liquid.w,sat_steam.w,sat_liquid.k,sat_steam.k,sat_liquid.sigma,sat_steam.sigma,sat_liquid.Prandt,sat_steam.Prandt])
    except:
        x.append("NONE")
    return x
def P_T_REG(Pin,Tin):
    x=[]
    Tin=float(Tin)+273.15
    Pin=float(Pin)
    try:
        sat_steam=IAPWS97(P=Pin,T=Tin)                #saturated steam with known P
      #saturated liquid with known T
                    #steam with known P and T
        x.append([(float(sat_steam.T)-273.15),sat_steam.P,sat_steam.v,sat_steam.u,sat_steam.h,sat_steam.s])
    except:
        x.append("NONE")
    return x
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

def t_conversion(val,unit):#converting all temperature units to Celsius first
    try:
        val=float(val)
        if(unit==0):
            out=val
        elif(unit==1):
            out=(val-32)*(5/9)
        elif(unit==2):
            out=val-273.15
        elif(unit==3):
            out=(val-491.67)*(5/9)
        return out
    except:
        return 'N/A'
    

def p_conversion(val,unit):#converting all pressure units to MPa first
    try:
        val=float(val)
        if(unit==0):
            out=val
        elif(unit==1):
            out=float(val)/1000
        elif(unit==2):
            out=float(val)*0.006894757293
        elif(unit==3):
            out=float(val)/10
        elif(unit==4):
            out=float(val)/9.8692326671601283
        elif(unit==5):
            out=float(val)/7500.6157584565623439424245176757
        return out
    except:
        return 'N/A'

def interpolate_var(processval, var1, t_low, t_high):
        global tempvarinterpolate
        tempvarinterpolate=[]
        x1=float(t_low[var1])
        x2=float(t_high[var1])
        for i in range(len(t_low)):
            try:
                sol_inter=float(t_low[i])+(processval-x1)*(float(t_high[i])-float(t_low[i]))/(x2-x1)
                tempvarinterpolate.append(sol_inter)
            except:
                tempvarinterpolate.append("NONE")
        if(t_low==t_high):
            tempvarinterpolate=[]
            tempvarinterpolate=t_high    

def Clicker(e):
    try:
        def Click_Select_all(e):            
            e.widget.event_generate('<Control-a>')
            
        def Click_Cut(e):
            e.widget.event_generate('<Control-x>')

        def Click_Copy(e):
            e.widget.event_generate('<Control-c>')

        def Click_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()
        right_click_menu=Menu(None,tearoff=False,takefocus=0)
        right_click_menu.add_command(label="Select all",command=lambda e=e: Click_Select_all(e))
        right_click_menu.add_separator()
        right_click_menu.add_command(label="Cut",command=lambda e=e: Click_Cut(e))
        right_click_menu.add_command(label="Copy",command=lambda e=e: Click_Copy(e))
        right_click_menu.add_command(label="Paste",command=lambda e=e: Click_Paste(e))

        right_click_menu.tk_popup(e.x_root, e.y_root,0)

    except TclError:
        pass

    return "break"

def Clickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=Clicker, add='')
    except TclError:
        print (' - Clickbinder, something wrong')
        pass
    
 



def interface_user():
    global statement
    global cm 
     
    
    window = ThemedTk(theme='adapta')
    window.geometry("900x370")
    window.title("Chemical Engineering Toolkit")
    window.resizable(False, False)
    window.withdraw()
    style_config=ttk.Style()
    style_config.theme_use('adapta')
    style_config.configure("Tab", focuscolor='00bcd4',padx=2,pady=2)
    style_config.configure("TButton", font=("Arial", 12),anchor=CENTER)
    style_config.configure("TMenubutton", font=("Arial", 12),anchor=CENTER)
    
   
    window.attributes('-alpha',0.96)
    #style.configure(".")["background"]
    # window['bg']='#f0f0f0'
    splash_root = Toplevel()
    splash_root.attributes('-alpha',0.96)
    splash_root.geometry("400x100")
    splash_label1 = ttk.Label(splash_root,text="CHEMICAL ENGINEERING TOOLKIT",font=("Arial Bold",14))
    splash_label1.pack() 
    splash_label1 = ttk.Label(splash_root,text="Software Version: 3.0",font=("Arial Bold",14))
    splash_label1.pack() 
    splash_label1 = ttk.Label(splash_root,text="Developed by Anindya Karmaker",font=("Arial Bold",14))
    splash_label1.pack() 
    splash_label2 = ttk.Label(splash_root,text="Loading database please wait",font=("Arial Bold",14))
    splash_label2.pack()
    
     
    splash_root.overrideredirect(True)
    style_config=ttk.Style()
    style_config.theme_use('adapta')
    style_config.configure("Tab", focuscolor='00bcd4',padx=2,pady=2)
    style_config.configure("TButton", font=("Arial", 12),anchor=CENTER)
    style_config.configure("TMenubutton", font=("Arial", 12),anchor=CENTER)
      
    
    splash_root.attributes('-topmost', True)
    splash_root.lift()
    splash_root.update()
    
    window.bind('<Button-3>',Clicker, add='')
    TC= ttk.Notebook(window,takefocus=0)
    ESTIMATE = ttk.Frame(TC) 
    CLONING =  ttk.Frame(TC)
    STEAMTAB= ttk.Frame(TC)
    ANTOINETAB=ttk.Frame(TC)
    CRITICALTAB=ttk.Frame(TC)
    INFO = ttk.Frame(TC) 
    TC.add(ESTIMATE, text='Infrared Spectroscopy')      
    TC.add(CLONING, text='DNA Cloning/Primer Design')
    TC.add(STEAMTAB, tex='Steam Tables')
    TC.add(ANTOINETAB, text='Antoine Tables') 
    TC.add(CRITICALTAB, text='Critical Data') 
    TC.add(INFO, text='Information')    
    TC.pack(expand=1, fill="both")    
    IR_ESTIMATE=ttk.Frame(ESTIMATE)
    IR_ESTIMATE.pack()
    DNA_Clone=ttk.Frame(CLONING)
    DNA_Clone.pack()
    Steam_tables=ttk.Frame(STEAMTAB)
    Steam_tables.pack()
    Antoine_tables=ttk.Frame(ANTOINETAB)
    Antoine_tables.pack()
    critical_tables=ttk.Frame(CRITICALTAB)
    critical_tables.pack()
    infoview=ttk.Frame(INFO)
    infoview.pack()
    lbl5 = ttk.Label(infoview, text="Chemical Engineering Toolkit V3.0", font=("Arial Bold", 14))
    lbl5.pack(fill='x')
    lbl6 = ttk.Label(infoview, text="Software Created by Anindya Karmaker", font=("Arial", 12))
    lbl6.pack(fill=X)
    lbl7 = ttk.Label(infoview, text="Dedicated to my loving parents and my Department of Chemical Engineering,", font=("Arial", 12))
    lbl7.pack(fill=X)
    lbl7p = ttk.Label(infoview, text="Bangladesh University of Engineering and Technology(BUET)", font=("Arial", 12))
    lbl7p.pack(fill=X)
    
    label9p = ttk.Label(infoview,text="ACKNOWLEDGEMENT",font=("Arial Bold",14))
    label9p.pack(fill='x')
    label0p = ttk.Label(infoview,text="I would like to acknowledge the sincere efforts and encouragement by Professor Dr. Shoeb Ahmed and Ahaduzzaman Nahid",font=("Arial", 12))
    label0p.pack(fill='x') 
    lbl8 = ttk.Label(infoview, text="References", font=("Arial Bold", 14))
    lbl8.pack(fill=X)
    lble1 = ScrolledText(infoview, wrap=WORD,font=("Arial", 12))
    statementinfo='Infrared Spectroscopy Data is based on the website\nhttps://chem.libretexts.org/Bookshelves/Ancillary_Materials/Reference/Reference_Tables/Spectroscopic_Parameters/Infrared_Spectroscopy_Absorption_Table\n\nThe steam properties are based on IAPWS 95 and IAPWS 97. IAPWS 95 is based on the NIST DATABASE\nhttp://www.nist.gov/srd/upload/NISTIR5078.htm\n\nCOPYRIGHT INFORMATION:\nUse of NIST Information: These World Wide Web pages are provided as a public service by the National Institute of Standards and Technology (NIST). With the exception of material marked as copyrighted, information presented on these pages is considered public information and may be distributed or copied. Use of appropriate byline/photo/image credits is requested\n\nIAPWS 97 is based on the Python implementation of standards from The International Association for the Properties of Water and Steam(IAPWS)\nhttps://pypi.org/project/iapws/\n\nAntoine tables and its database is based on the work by \nYaws, C.  L.  and Yang, H.  C. "To estimate vapor pressure easily, antoine coefficients relate vapor pressure to temperature for almost 700 major organic compounds", Hydrocarbon Processing, 68(10), p65-68, 1989\n\nCritical Properties and Accentric Factors are based on the work by \nC. L. Yaws and P. K. Narasimhan, “Critical properties and acentric factor—organic compounds,” in Thermophysical properties of chemicals and hydrocarbons, Elsevier, 2009, pp. 1–95.\nAnd\nC. L. Yaws, “Critical Properties and Acentric Factor – Organic Compounds,” in Thermophysical properties of chemicals and hydrocarbons, 2nd ed., William Andrew, 2014\n'
    lble1.insert(INSERT,statementinfo)
    lble1.config(width=860,height=12,padx=2,pady=2)
    lble1.config(state='disabled')
    lble1.pack(fill='x')
    enteroption = ttk.Frame(DNA_Clone)
    enteroption.grid(row=0,column=0, padx=5,pady=5,sticky=N)
    optttkLabel=ttk.Label(enteroption, text="Enter DNA OR RNA Sequence(5' to 3')",font=("Arial", 13,"bold"),justify=LEFT).pack(pady=5,anchor=W)
    seqzone=ScrolledText(enteroption, width=32,height=12,font=("Consolas", 12))
    seqzone.pack(pady=2,anchor=W)
    tkRE_seq=StringVar(window)
    restriction_enzyme=ttk.Label(enteroption, text="Restriction Enzyme (RE) (5' to 3')",font=("Arial", 13,"bold"),justify=LEFT).pack(pady=2,anchor=W)
    RE_select=Entry(enteroption,width=32,font=("Consolas", 13,"bold"),textvariable=tkRE_seq, justify=LEFT).pack(pady=2,anchor=W,fill='both',expand=TRUE)
    tkRF = StringVar(window)
    
    
    choices_RF = { 'Reading Frame 1','Reading Frame 2','Reading Frame 3'}
    choices_RF =sorted(choices_RF)
    def OptionMenu_SelectionEvent_RF(event):
        global readingframe
        if(tkRF.get()==choices_RF[0]):
            readingframe=0
        elif(tkRF.get()==choices_RF[1]):
            readingframe=1
        elif(tkRF.get()==choices_RF[2]):
            readingframe=2
        pass
    choices_RE = ['Add RE to Primer','Do not add RE to Primer']
    choices_RE =sorted(choices_RE,reverse=True)
    tkRE_opt = StringVar(window)
    def OptionMenu_SelectionEvent_RE(event):
        global addRE_VAL
        if(tkRE_opt.get()==choices_RE[0]):
            addRE_VAL=0
            print("ONE")
        elif(tkRE_opt.get()==choices_RE[1]):
            addRE_VAL=1
            print("TWO")
        print(addRE_VAL)
        pass
    enteroption2 = ttk.Frame(DNA_Clone)
    enteroption2.grid(row=0,column=1, padx=5,pady=30,ipadx=5,ipady=5,sticky='nsew')
    

    tkRE_opt.set(choices_RE[0]) # set the default option
    popupMenuRE = ttk.OptionMenu(enteroption2, tkRE_opt,choices_RE[0], *choices_RE, command = OptionMenu_SelectionEvent_RE)
    # popupMenuRE.configure(width=23,font=("Arial", 13,"bold"))
    popupMenuRE.pack(side=TOP,fill='both',expand=TRUE,anchor=N)
    
    tkRF.set(choices_RF[0]) # set the default option
    popupMenu = ttk.OptionMenu(enteroption2, tkRF,choices_RF[0], *choices_RF, command = OptionMenu_SelectionEvent_RF)
    # popupMenu.configure(width=23,font=("Arial", 13,"bold"))
    popupMenu.pack(side=TOP,fill='both',expand=TRUE,anchor=N)
    
    tkAAS = StringVar(window)
    def OptionMenu_SelectionEvent_SEQTYPE(event):
        global seqtype
        if(tkAAS.get()=="Short amino acid sequence"):
            seqtype=1
        elif(tkAAS.get()=="Long amino acid sequence"):
            seqtype=0
        print(seqtype)
        print(tkAAS.get())
        pass
    choices_AAS = { 'Short amino acid sequence','Long amino acid sequence'}
    choices_AAS =sorted(choices_AAS)
    tkAAS.set('Long amino acid sequence') # set the default option
    popupMenu2 = ttk.OptionMenu(enteroption2, tkAAS, choices_AAS[0],*choices_AAS, command = OptionMenu_SelectionEvent_SEQTYPE)
    popupMenu2.pack(side=TOP,fill='both',expand=TRUE,anchor=N)
    solve_dna_prot=ttk.Button(enteroption2, text="Show Amino acid Sequence",takefocus=0)
    solve_dna_prot.pack(side=TOP,anchor=N,fill='both',expand=TRUE)
    
    Primer_design=ttk.Button(enteroption2, text="Determine Forward Primer",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    Primer_design.pack(side=TOP,anchor=N,fill='both',expand=TRUE)
    Primer_design2=ttk.Button(enteroption2, text="Determine Reverse Primer",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    Primer_design2.pack(side=TOP,anchor=N,fill='both',expand=TRUE)
    Check_SEQ=ttk.Button(enteroption2, text="Check RE Sequence",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    Check_SEQ.pack(side=TOP,anchor=N,fill='both',expand=True) 
    cloneopt=ttk.Frame(DNA_Clone)
    cloneopt.grid(row=0,column=2,padx=5,pady=5,sticky=N)
    
    lb1=ttk.Label(cloneopt, text="Results(5' to 3')", justify='center',font=("Arial", 13,"bold")).pack(pady=5,side=TOP)

    solution_seq=ScrolledText(cloneopt, wrap=WORD, padx=5,width=32,height=15,font=("Consolas", 12))
    solution_seq.pack(pady=2,anchor=NW)

       
    def check_SEQ_LOC():
        solution_seq.delete("1.0", END)
        global sequence
        sequence=str(seqzone.get("1.0", END))
        seq=re.sub('[^atgcuATGCU]','',sequence).upper()   
        RE_seq=str(tkRE_seq.get()).upper()  
        position=[]
        if(RE_seq!=''):
            for loc in re.finditer(RE_seq, seq):
                position.append(int(loc.start()+1))
            print(position)
        if(len(position)>0):
            result="FOUND SEQUENCE AT POSITION "
            for i in range(len(position)):
                result+=str(position[i])
                if(len(position)-i>2):
                    result+=','
                elif(len(position)-i==2):
                    result+=' and '
        else:
            result="SEQUENCE NOT FOUND"
        solution_seq.insert(INSERT, result)
    Check_SEQ.configure(command=check_SEQ_LOC)
    def solve_sequence():
        global sequence
        global readingframe
        global seqtype
        global protein_list
        global sequencetab
        sequencetab=0
        protein_list=[]
        protein_sequence_list=[]
        sequence=str(seqzone.get("1.0", END))
        sequence=str(sequence.replace("\n",""))
        seq=re.sub('[^atgcuATGCU]','',sequence)
        seq=seq[readingframe:].upper()
        print(seq)
        countseq=0
        seqlist=[]
        resultseq=""
        for i in range(len(seq)):
            if(seq[i]=='T'):
                resultseq+='U'
            else:
                resultseq+=seq[i]
            countseq+=1
            if(countseq>2):
                countseq=0
                seqlist.append(resultseq)
                resultseq=""
                # print(i)
        aminoacidseq=""
        aminoacidshortseq=""
        for i in range(len(seqlist)):
            aminoacidshortseq+=shortseqprot[codonseq[seqlist[i]]]
            aminoacidshortseq+="  "
            aminoacidseq+=codonseq[seqlist[i]]
            aminoacidseq+="  "
            pass
        solution_seq.delete("1.0", END)            
        if(seqtype==0):
            n=0;
            last=aminoacidseq
            lastf=''

            while(n<len(last)):
                lastf=last
                locate_start_l=0
                locate_stop_l=0
                if('Met' in last):
                    locate_start_l=last.find("Met")
                    # print("START")
                    
                    if('STP' in last[locate_start_l::]):
                        locate_stop_l=int(last[locate_start_l::].find("STP"))
                        locate_stop_l+=int(locate_start_l)
                        # print("STOP")  
                        sequencetab=int(locate_stop_l/5)
                    else:               
                        part1=last   
                        sequencetab=int(len(part1)/5)
                        solution_seq.insert(INSERT, part1)
                        if(lastf==last):
                            break
                    if(locate_start_l!=locate_stop_l and locate_stop_l>locate_start_l):
                        part1=last[0:locate_start_l]
                        protein=last[locate_start_l:locate_stop_l+4]
                        protein_list.append(protein)
                        last=last[locate_stop_l+4::]
                        print("STARTED AT ",int(locate_start_l/5)+sequencetab)
                        print("STOPPED AT ",int(locate_stop_l/5)+sequencetab)
                        print("Protein:")
                        print(protein)
                        print("EXCESS PART", part1)
                        print(len(part1))
                        # try:
                        #     protseq=''
                        #     protseq+=str((int(locate_start_l/5)+sequencetab)*3+1) 
                        #     protseq+=' '
                        #     for i in range(int(locate_start_l/5)+sequencetab,int(locate_stop_l/5)+1+sequencetab):
                        #         protseq+=seqlist[i]
                        #     protseq+=' '
                        #     protseq+=str((int(locate_stop_l/5)+1+sequencetab)*3)
                        #     sequencetab=int(locate_stop_l/5)+1
                        #     print(protseq)
                        #     protein_sequence_list.append(protseq)
                        # except:
                        #     pass
                        print("--------------------------------------------------------")                        
                        solution_seq.insert(INSERT, part1)
                        solution_seq.insert(INSERT, protein,'sequence_found')
                        solution_seq.tag_configure('sequence_found',background='#f9b1b6')    
                        
                else:            
                    print("P1:")        
                    print(last)
                    part1=last
                    sequencetab=int(len(part1)/5)
                    solution_seq.insert(INSERT, part1)
                    if(lastf==last):
                        break
                n+=1 
                        
            # print(aminoacidseq)
        elif(seqtype==1):
            n=0;
            last=aminoacidshortseq
            lastf=''
            while(n<len(last)):
                lastf=last
                locate_start_l=0
                locate_stop_l=0
                if('M' in last):
                    locate_start_l=last.find("M")
                    # print("START")
                    # print(locate_start_l)
                    if('-' in last[locate_start_l::]):
                        locate_stop_l=int(last[locate_start_l::].find("-"))
                        locate_stop_l+=int(locate_start_l)
                        # print("STOP")  
                        # print(locate_stop_l)
                    else:            
                        print("P1:")        
                        print(last)
                        part1=last
                        solution_seq.insert(INSERT, part1)
                        if(lastf==last):
                            break
                    if(locate_start_l!=locate_stop_l and locate_stop_l>locate_start_l):
                        part1=last[0:locate_start_l]
                        protein=last[locate_start_l:locate_stop_l+2]
                        protein_list.append(protein)
                        last=last[locate_stop_l+2::]
                        print("P1:")
                        print(part1)
                        print("Protein:")
                        print(protein)
                        print("--------------------------------------------------------")                        
                        solution_seq.insert(INSERT, part1)
                        solution_seq.insert(INSERT, protein,'sequence_found')
                        solution_seq.tag_configure('sequence_found',background='#f9b1b6')
                else:            
                    print("P1:")        
                    print(last)
                    part1=last
                    solution_seq.insert(INSERT, part1)
                    if(lastf==last):
                        break
                n+=1  

        finalstatement="\n\n"
        solution_seq.insert(INSERT, finalstatement) 
        finalstatement="Number of Proteins Found: "+str(len(protein_list))
        solution_seq.insert(INSERT, finalstatement,'user_info') 
        solution_seq.tag_configure('user_info',background='green',foreground='white')
        solution_seq.insert(INSERT, '\n')
        finalstatement="List of Proteins: "
        solution_seq.insert(INSERT, '\n')
        solution_seq.insert(INSERT, finalstatement, 'user_info') 
        for i in range(len(protein_list)):
            solution_seq.insert(INSERT, '\n')
            finalstatement=str(protein_list[i])
            solution_seq.insert(INSERT, str('Protein '+str(i+1)+': \n'))
            solution_seq.insert(INSERT, finalstatement,'sequence_underline')
            solution_seq.tag_configure('sequence_underline',background='blue',foreground='white')
            solution_seq.insert(INSERT, '\n')
            # solution_seq.insert(INSERT, str(protein_sequence_list[i]),'sequence_underline')
            # solution_seq.tag_configure('sequence_underline',background='blue',foreground='white')
            # solution_seq.insert(INSERT, '\n')
            
    solve_dna_prot.configure(command=solve_sequence)
    def solve_forward_primer():
        solution_seq.delete("1.0", END)
        global sequence
        global readingframe
        global seqtype
        global addRE_VAL
        RE_seq=''
        if(addRE_VAL==1):
            RE_seq=str(tkRE_seq.get()).upper()
        count_excess_nucleotide=4
        excess_nucleotide=''
        GClist=['G','C']
        ATlist=['A','T']
        totalAT=0;
        totalGC=0;
        sequence=str(seqzone.get("1.0", END))
        sequence=str(sequence.replace("\n",""))
        if(sequence!=''):
            seq=re.sub('[^atgcuATGCU]','',sequence)
            seq=seq[readingframe:].upper()
            result=''
            countAT=0;
            countGC=0;
            lengthseq=0;
            sequence=''
            for i in range(len(RE_seq)):
                if(RE_seq[i]=='A' or RE_seq[i]=='T'):
                    totalAT+=1;
                elif(RE_seq[i]=='U'):
                    totalAT+=1;
                elif(RE_seq[i]=='G' or RE_seq[i]=='C'):
                    totalGC+=1;
            for i in range(len(seq)):
                if(seq[i]=='A' or seq[i]=='T'):
                    countAT+=1;
                    lengthseq+=1;
                    sequence+=seq[i]
                elif(seq[i]=='U'):
                    countAT+=1;
                    lengthseq+=1;
                    sequence+='T'
                elif(seq[i]=='G' or seq[i]=='C'):
                    countGC+=1;
                    lengthseq+=1;
                    sequence+=seq[i]
            totalAT+=countAT
            totalGC+=countGC
            while(len(excess_nucleotide)<count_excess_nucleotide and addRE_VAL==1):
                if(totalAT==totalGC):
                    excess_nucleotide+=str(random.choice(GClist))
                    totalGC+=1;
                elif(totalAT>totalGC):
                    excess_nucleotide+=str(random.choice(GClist))
                    totalGC+=1;
                elif(totalAT<totalGC):
                    excess_nucleotide+=str(random.choice(ATlist))
                    totalAT+=1;        
            if(addRE_VAL==0):
                result="Sequence: \n5' "+str(sequence)+" 3'"+"\nBinding Sequence Length: "+str(lengthseq)+"\nBinding part A and T COUNT: "+str(countAT)+"\nBinding part G and C COUNT: "+str(countGC)+"\nMelting point of binding sequence(°C): "+ str(4*countGC+2*countAT)
                solution_seq.insert(INSERT, result)
            elif(addRE_VAL==1):
                result="Sequence: \n5' "
                solution_seq.insert(INSERT, result)
                result1=str(excess_nucleotide.upper())
                solution_seq.insert(INSERT, result1,'extra_nuc')
                solution_seq.tag_configure('extra_nuc',foreground='red')
                result2=str(RE_seq.upper())
                solution_seq.insert(INSERT, result2,'primer')
                solution_seq.tag_configure('primer',foreground='blue')
                result3=str(sequence)+" 3'"+"\nBinding Sequence Length: "+str(lengthseq)+"\nBinding part A and T COUNT: "+str(countAT)+"\nBinding part G and C COUNT: "+str(countGC)+"\nMelting point of binding sequence(°C): "+ str(4*countGC+2*countAT)+"\nTotal A+T="+str(totalAT)+"\nTotal G+C="+str(totalGC)
                solution_seq.insert(INSERT, result3)
        else:
            result='PLEASE ENTER SEQUENCE IN ORDER TO CALCULATE PRIMER'
            solution_seq.insert(INSERT, result)
        
        
    Primer_design.configure(command=solve_forward_primer)
    def solve_reverse_primer():
        solution_seq.delete("1.0", END)
        global sequence
        global readingframe
        global seqtype
        global addRE_VAL
        RE_seq=''
        if(addRE_VAL==1):
            RE_seq=tkRE_seq.get().upper()
        count_excess_nucleotide=4
        excess_nucleotide=''
        GClist=['G','C']
        ATlist=['A','T']
        totalAT=0;
        totalGC=0;
        for i in range(len(RE_seq)):
            if(RE_seq[i]=='A' or RE_seq[i]=='T'):
                totalAT+=1;
            elif(RE_seq[i]=='U'):
                totalAT+=1;
            elif(RE_seq[i]=='G' or RE_seq[i]=='C'):
                totalGC+=1;        
        sequence=str(seqzone.get("1.0", END))
        sequence=str(sequence.replace("\n",""))
        if(sequence!=''):            
            seq=re.sub('[^atgcuATGCU]','',sequence)
            seq=seq[readingframe::].upper()
            result=''
            countAT=0;
            countGC=0;
            lengthseq=0;
            sequence=''
            orisequence=''
            comsequence=''
            for i in range(len(seq)):
                if(seq[i]=='A'):
                    lengthseq+=1;
                    countAT+=1;
                    comsequence+='T'
                    orisequence+=seq[i]
                elif(seq[i]=='T' or seq[i]=='U'):
                    lengthseq+=1;
                    countAT+=1;
                    comsequence+='A'
                    orisequence+=seq[i]
                elif(seq[i]=='G'):
                    lengthseq+=1;
                    countGC+=1;
                    comsequence+='C'
                    orisequence+=seq[i]
                elif(seq[i]=='C'):
                    lengthseq+=1;
                    countGC+=1;
                    comsequence+='G'
                    orisequence+=seq[i]
            totalAT+=countAT
            totalGC+=countGC
            while(len(excess_nucleotide)<count_excess_nucleotide and addRE_VAL==1):
                if(totalAT==totalGC):
                    excess_nucleotide+=str(random.choice(GClist))
                    totalGC+=1;
                elif(totalAT>totalGC):
                    excess_nucleotide+=str(random.choice(GClist))
                    totalGC+=1;
                elif(totalAT<totalGC):
                    excess_nucleotide+=str(random.choice(ATlist))
                    totalAT+=1;
            if(addRE_VAL==0):
                result="Reverse Complementary \nSequence: \n5' "+str(comsequence[::-1])+" 3'"+"\nBinding Sequence Length: "+str(lengthseq)+"\nBinding part A and T COUNT: "+str(countAT)+"\nBinding part G and C COUNT: "+str(countGC)+"\nMelting point of binding sequence(°C): "+ str(4*countGC+2*countAT)
                solution_seq.insert(INSERT, result)
            elif(addRE_VAL==1):
                result="Reverse Complementary  \nSequence: \n5' "
                solution_seq.insert(INSERT, result)
                result1=str(excess_nucleotide.upper())
                solution_seq.insert(INSERT, result1,'extra_nuc')
                solution_seq.tag_configure('extra_nuc',foreground='red')
                result2=str(RE_seq.upper())
                solution_seq.insert(INSERT, result2,'primer')
                solution_seq.tag_configure('primer',foreground='blue')
                result3=str(comsequence[::-1])+" 3'"+"\nBinding Sequence Length: "+str(lengthseq)+"\nBinding part A and T COUNT: "+str(countAT)+"\nBinding part G and C COUNT: "+str(countGC)+"\nMelting point of binding sequence(°C): "+ str(4*countGC+2*countAT)+"\nTotal A+T="+str(totalAT)+"\nTotal G+C="+str(totalGC)        
                solution_seq.insert(INSERT, result3)
        else:
            result='PLEASE ENTER SEQUENCE IN ORDER TO CALCULATE PRIMER'
            solution_seq.insert(INSERT, result)
        
    Primer_design2.configure(command=solve_reverse_primer)
    
    
    
    tkIAPWS=StringVar(window)
    def OptionMenu_SelectionEvent_IAPWS(event):
        global iapwsversion
        if(tkIAPWS.get()==IAPWSVER[0]):
            iapwsversion=95
            print(iapwsversion)
        elif(tkIAPWS.get()==IAPWSVER[1]):
            iapwsversion=97
            print(iapwsversion)        
        pass 
    tkIAPWS.set(IAPWSVER[0])
    
    tkUNITS=StringVar(window)
    def OptionMenu_SelectionEvent_UNITS(event):
        global chooseunit
        if(tkUNITS.get()==outputunit[0]):
            chooseunit=0
            print("SI")
        elif(tkUNITS.get()==outputunit[1]):
            chooseunit=1
            print("US CU")        
        pass 
    tkUNITS.set(outputunit[0])
    tkThermo=StringVar(window)
    def OptionMenu_SelectionEvent_Thermo(event):
        global thermouserinp
        if(tkThermo.get()=="Saturated Steam (Pressure Based)"):
            optionP.configure(state='normal')
            optionT.configure(state='disabled')
            thermouserinp=0
        elif(tkThermo.get()=="Saturated Steam (Temperature Based)"):
            thermouserinp=1
            optionT.configure(state='normal')
            optionP.configure(state='disabled')
        elif(tkThermo.get()=="Single Phase Property(Compressed Water and Superheated Steam)"):
            thermouserinp=2
            optionP.configure(state='normal')
            optionT.configure(state='normal')
        print(thermouserinp)
        pass 
    tkThermo.set("Saturated Steam (Pressure Based)")
    tkPressureUnit=StringVar(window)
    def OptionMenu_SelectionEvent_PressureUnit(event):
        global P_unitselection
        global P_UNITDISP
        if(tkPressureUnit.get()=="MPa"):
            P_unitselection=0
            P_UNITDISP='MPa'
        elif(tkPressureUnit.get()=="kPa"):
            P_unitselection=1
            P_UNITDISP='kPa'
        elif(tkPressureUnit.get()=="PSI"):
            P_unitselection=2
            P_UNITDISP='PSI'
        elif(tkPressureUnit.get()=="Bar"):
            P_unitselection=3
            P_UNITDISP='Bar'
        elif(tkPressureUnit.get()=="Atm"):
            P_unitselection=4
            P_UNITDISP='Atm'
        elif(tkPressureUnit.get()=="mmHg"):
            P_unitselection=5
            P_UNITDISP='mmHg'
        print(P_unitselection)
        pass 
    tkPressureUnit.set(pressureunit[P_unitselection])
    tkTemperatureUnit=StringVar(window)
    def OptionMenu_SelectionEvent_TemperatureUnit(event):
        global T_unitselection
        global T_UNITDISP
        if(tkTemperatureUnit.get()=="Celsius"):
            T_unitselection=0
            T_UNITDISP='°C'
        elif(tkTemperatureUnit.get()=="Fahrenheit"):
            T_unitselection=1
            T_UNITDISP='°F'
        elif(tkTemperatureUnit.get()=="Kelvin"):
            T_unitselection=2
            T_UNITDISP='K'
        elif(tkTemperatureUnit.get()=="Rankine"):
            T_unitselection=3
            T_UNITDISP='R'
        print(T_unitselection)
        pass 
    tkTemperatureUnit.set(temperatureunit[T_unitselection])
    def thermo_help_me():
        lbdisp_thermo.configure(state='normal')
        lbdisp_thermo.delete('1.0', END)
        statement='-'*59+"HELP"+'-'*59+"\nThermodynamic Tables for water and steam. There are two methods for calculation- IAPWS'95 and IAPWS'97(LATEST VERSION). Both of them yield similar result(±2%). However, once the temperature or pressure nears to the critical region, the deviation becomes quite large. IAPWS'97 method also calulates a lot more varibles than IAPWS'95.Hence, I suggest that you use any method for calculation depending on your usage, however, for pressure or temperature near critical region please use IAPWS'97 method. One useful tip, in IAPWS'95 method, using Single Phase Property, you can determine the saturation temperature by just entering the pressure and keeping the temperature entry blank. IAPWS'95 is based on NIST Database(SEE INFORMATION TAB FOR MORE) and IAPWS'97 is calculated based on the equations by IAPWS(SEE INFORMATION TAB FOR MORE). This software also has a built-in unit conversion system. You can select the pressure and temperature units as well as the output in SI or US Customary Units\n"+'-'*59+"END"+'-'*60
        lbdisp_thermo.insert(INSERT,statement)
        lbdisp_thermo.configure(state='disabled')

    def Notations_HELP():
        new=Toplevel()
        new.title("NOTATIONS")
        new.geometry("350x300")
        new.resizable('false','false')
        new.lift()
        new.attributes('-topmost',True)
        # new.after_idle(new.attributes,'-topmost',False)
        lbdisp_thermo_2=ScrolledText(new,wrap=WORD,width=110, height=40,font=('Consolas',11))
        lbdisp_thermo_2.pack(side=LEFT,fill='none')      
        statement='f: Water\ng: Steam\nfg: Evaporation\nV: Specific Volume\nU: Internal Energy\nH: Specific Enthalpy\nS: Specific Entropy\nCp: Specific Heat at constant pressure\nCv: Specific Heat at constant volume\nZ: Compressibility factor\nW: Speed of sound\nk: Thermal Conductivity\nσ: Surface Tension\nPr: Prandtl Number'
        lbdisp_thermo_2.insert(INSERT,statement)
        lbdisp_thermo_2.configure(state='disabled')
        
    variableoptionMAIN = ttk.Frame(Steam_tables)
    variableoptionMAIN.grid(row=0,column=0, padx=5,pady=5,sticky=NW)
    popupMenuiapws_option = ttk.OptionMenu(variableoptionMAIN, tkIAPWS,IAPWSVER[0], *IAPWSVER, command = OptionMenu_SelectionEvent_IAPWS)
    popupMenuiapws_option.configure(takefocus=0)
    popupMenuiapws_option.pack(side=LEFT,fill='x',expand=TRUE,anchor=NW) 
    popupMenuthermo_option = ttk.OptionMenu(variableoptionMAIN, tkThermo,thermotablename[0], *thermotablename, command = OptionMenu_SelectionEvent_Thermo)
    popupMenuthermo_option.configure(takefocus=0,width=62)
    popupMenuthermo_option.pack(side=LEFT,fill='both',expand=TRUE,anchor=W) 
    notations_thermo=ttk.Button(variableoptionMAIN, text="Notations")
    notations_thermo.configure(takefocus=0,width=9,command=Notations_HELP)
    notations_thermo.pack(side=LEFT,anchor=NW) 
    help_thermo=ttk.Button(variableoptionMAIN, text="Help")#, font=("Arial", 13,"bold"), height=1, width=2)
    help_thermo.configure(takefocus=0,width=4,command=thermo_help_me)
    help_thermo.pack(side=LEFT,anchor=W,expand=TRUE)

       
    variableoption = ttk.Frame(Steam_tables)
    variableoption.grid(row=1,column=0, padx=5,pady=5,sticky=NW)
       
    optttkLabelPressure=ttk.Label(variableoption, text="Pressure: ", justify='center',font=("Arial", 13,"bold")).pack(side=LEFT)
    optionP=Entry(variableoption, width=10,font=("Consolas", 12))
    optionP.pack(side=LEFT,fill="both",pady=4)
    optionP.configure(state='normal')
    popupMenupressure_unit = ttk.OptionMenu(variableoption, tkPressureUnit,pressureunit[P_unitselection], *pressureunit, command = OptionMenu_SelectionEvent_PressureUnit)
    popupMenupressure_unit.configure(width=5,takefocus=0,)
    popupMenupressure_unit.pack(side=LEFT,fill='y',expand=TRUE,anchor=NW) 
    optttkLabelTemperature=ttk.Label(variableoption, text="Temperature: ", justify='center',font=("Arial", 13,"bold")).pack(side=LEFT)
    optionT=Entry(variableoption, width=10,font=("Consolas", 12))
    optionT.pack(side=LEFT,fill="both",pady=4)
    optionT.configure(state='disabled')
    popupMenuTemp_unit = ttk.OptionMenu(variableoption, tkTemperatureUnit,temperatureunit[T_unitselection], *temperatureunit, command = OptionMenu_SelectionEvent_TemperatureUnit)
    popupMenuTemp_unit.configure(width=10,takefocus=0,)
    popupMenuTemp_unit.pack(side=LEFT,fill='x',expand=TRUE,anchor=NW) 
    variableoption2 = ttk.Frame(Steam_tables)
    variableoption2.grid(row=2,column=0, padx=0,pady=0,sticky=NW)
    popupMenuCHOOSE_unit = ttk.OptionMenu(variableoption, tkUNITS,outputunit[0], *outputunit, command = OptionMenu_SelectionEvent_UNITS)
    popupMenuCHOOSE_unit.configure(width=16,takefocus=0,)
    popupMenuCHOOSE_unit.pack(side=LEFT,fill='y',expand=TRUE,anchor=NW) 
    solve_thermo=ttk.Button(variableoption, text="Estimate")#, font=("Arial", 13,"bold"), height=1, width=7)
    solve_thermo.configure(width=8,takefocus=0,)
    solve_thermo.pack(side=LEFT,anchor=N,fill='x',expand=TRUE)
    lbdisp_thermo=ScrolledText(variableoption2,wrap='word',width=122, height=13.5,padx=5,pady=8,font=('Consolas',10))
    lbdisp_thermo.pack(side=LEFT)      
    lbdisp_thermo.configure(state='disabled')
    # optttkLabel=ttk.Label(variableoption2, text="Notations",font=("Arial", 10,"bold")).pack(fill='x',side=TOP)
    # optttkLabel2=ttk.Label(variableoption2, text="f: Water\ng: Steam\nfg: Evaporation\nV: Specific Volume\nU: Internal Energy\nH: Specific Enthalpy\nS: Specific Entropy\nC: Specific Heat\nZ: Compressibility\n    factor\nW: Speed of sound\nk: Thermal\n    Conductivity\nσ: Surface Tension\nPr: Prandtl Number",font=("Arial", 8),anchor=E,justify=LEFT).pack(fill='y',side=TOP)
    
  

    def steam_table_value():
        lbdisp_thermo.configure(state='normal')
        global thermouserinp
        global tempvarlow
        global tempvarhigh
        global tempvarinterpolate
        global T_unitselection
        global P_unitselection
        tempvarlow=[]
        tempvarhigh=[]
        tempvarinterpolate=[]
        userinp=thermouserinp
        print("OPTION")
        print(thermouserinp)
        y_dat_SP=['T(°C)','P(MPa)','V(m3/kg)','U(kJ/kg)','H(kJ/kg)','S(kJ/kg-k)']
        y_dat=['T(°C)','P(MPa)','Vf(m3/kg)','Vg(m3/kg)','Uf(kJ/kg)','Ug(kJ/kg)','Hf(kJ/kg)','Hg(kJ/kg)']             
        y_dat2=['Hfg(kJ/kg)','Sf(kJ/kg-k)','Sg(kJ/kg-k)','Sfg(kJ/kg-k)','Cpf(kJ/kg-k)','Cpg(kJ/kg-k)']
        y_dat3=['Cvf(kJ/kg-k)','Cvg(kJ/kg-k)','Zf','Zg','Wf(m/s)','Wg(m/s)','kf(W/m-k)','kg(W/m-k)',]
        y_dat4=['σf(N/m)','σg(N/m)','Pr.f','Pr.g']
        if(chooseunit==0):
            y_dat=['T(°C)','P(MPa)','Vf(m3/kg)','Vg(m3/kg)','Uf(kJ/kg)','Ug(kJ/kg)','Hf(kJ/kg)','Hg(kJ/kg)']             
            y_dat2=['Hfg(kJ/kg)','Sf(kJ/kg-k)','Sg(kJ/kg-k)','Sfg(kJ/kg-k)','Cpf(kJ/kg-k)','Cpg(kJ/kg-k)']
            y_dat3=['Cvf(kJ/kg-k)','Cvg(kJ/kg-k)','Zf','Zg','Wf(m/s)','Wg(m/s)','kf(W/m-k)','kg(W/m-k)']
            y_dat4=['σf(N/m)','σg(N/m)','Pr.f','Pr.g']
            y_dat_SP=['T(C)','P(MPa)','V(m3/kg)','U(kJ/kg)','H(kJ/kg)','S(kJ/kg-k)']
        elif(chooseunit==1):
            y_dat=['T(°C)','P(MPa)','Vf(ft3/lbm)','Vg(ft3/lbm)','Uf(Btu/lbm)','Ug(Btu/lbm)','Hf(Btu/lbm)','Hg(Btu/lbm)']             
            y_dat2=['Hfg(Btu/lbm)','Sf(Btu/lbm-F)','Sg(Btu/lbm-F)','Sfg(Btu/lbm-F)','Cpf(Btu/lbm-F)','Cpg(Btu/lbm-F)']
            y_dat3=['Cvf(Btu/lbm-F)','Cvg(Btu/lbm-F)','Zf','Zg','Wf(ft/s)','Wg(ft/s)','kf(BTU/h-ft-F)','kf(BTU/h-ft-F)']
            y_dat4=['σf(lbf/in)','σg(lbf/in)','Pr.f','Pr.g']
            y_dat_SP=['T(C)','P(MPa)','V(ft3/lbm)','U(Btu/lbm)','H(Btu/lbm)','S(Btu/lbm-F)']
        y_datT=['T(°C)','T(°F)','T(K)','T(°R)']
        y_datP=['P(MPa)','P(kPa)','P(PSI)','P(Bar)','P(Atm)','P(mmHg)']       
        y_dat[0]=y_datT[T_unitselection]
        y_dat[1]=y_datP[P_unitselection]
        y_dat_SP[0]=y_datT[T_unitselection]
        y_dat_SP[1]=y_datP[P_unitselection]
        try:
            if(iapwsversion==95):
                if(userinp==0):
                    userinp2=2
                    try:
                        uservalue=float(optionP.get())
                        uservalue=p_conversion(uservalue, P_unitselection)
                        print(uservalue)
                    except:
                        uservalue=0.01
                    cmdlower_val="SELECT * FROM "+'"'+str("Saturated_property_P_based")+'"'+" WHERE "+"Psat_Mpa"+" <= "+str(uservalue)+" ORDER BY ABS"+"("+"Psat_Mpa"+"-" +str(uservalue)+") "+ "LIMIT 1"
                    for row in cur.execute(cmdlower_val):
                        for i in range(len(row)):
                            tempvarlow.append(str(row[i]))
                    
                    cmdhigher_val="SELECT * FROM "+'"'+str("Saturated_property_P_based")+'"'+" WHERE "+"Psat_Mpa"+" >= "+str(uservalue)+" ORDER BY ABS"+"("+"Psat_Mpa"+"-" +str(uservalue)+") "+ "LIMIT 1"
                    for row in cur.execute(cmdhigher_val):
                        for i in range(len(row)):
                            tempvarhigh.append(str(row[i]))
                    interpolate_var(uservalue, userinp2,tempvarlow,tempvarhigh)                 
                    tempvarinterpolate[1]=C_to_other(tempvarinterpolate[1],T_unitselection)
                    tempvarinterpolate[2]=Mpa_to_other(tempvarinterpolate[2],P_unitselection)
                    print(tempvarinterpolate)
                    if(chooseunit==0):
                        x_dat=[tempvarinterpolate[1:9]]
                        x=tabulate(x_dat, headers=y_dat)
                        lbdisp_thermo.delete('1.0',END)
                        lbdisp_thermo.insert(INSERT,str(x))
                        x_dat2=[tempvarinterpolate[9::]]
                        x2=tabulate(x_dat2, headers=y_dat2)
                        lbdisp_thermo.insert(INSERT,"\n\n\n")
                        lbdisp_thermo.insert(INSERT,str(x2))
                        print(x)
                    elif(chooseunit==1):
                        for i in range(len(tempvarinterpolate)):
                        	x=3
                        	if(i==x or i==x+1):
                        		tempvarinterpolate[i]=m3_kg_to_ft3_lbm(tempvarinterpolate[i])
                        	elif(i>=x+2 and i<=x+6):
                        		tempvarinterpolate[i]=kj_kg_to_btu_lbm(tempvarinterpolate[i])
                        	elif(i>=x+7 and i<=x+13):
                        		tempvarinterpolate[i]=kj_kg_k_to_btu_lbm_F(tempvarinterpolate[i])
                        	elif(i==x+16 or i==x+17):
                        		tempvarinterpolate[i]=m_s_to_ft_s(tempvarinterpolate[i])
                        	elif(i==x+18 or i==x+19):
                        		tempvarinterpolate[i]=W_m_k_to_BTU_h_ft_F(tempvarinterpolate[i])
                        	elif(i==x+20 or i==x+21):
                        		tempvarinterpolate[i]=N_M_to_lbf_in(tempvarinterpolate[i])
                        x_dat=[tempvarinterpolate[1:9]]
                        x=tabulate(x_dat, headers=y_dat)
                        lbdisp_thermo.delete('1.0',END)
                        lbdisp_thermo.insert(INSERT,str(x))
                        x_dat2=[tempvarinterpolate[9::]]
                        x2=tabulate(x_dat2, headers=y_dat2)
                        lbdisp_thermo.insert(INSERT,"\n\n\n")
                        lbdisp_thermo.insert(INSERT,str(x2))
                        print(x)
                elif(userinp==1):
                    userinp2=1
                    try:
                        uservalue=float(optionT.get())
                        uservalue=t_conversion(uservalue, T_unitselection)
                        print(uservalue)
                    except:
                        uservalue=0.01
                    cmdlower_val="SELECT * FROM "+'"'+str("Saturated_property_T_based")+'"'+" WHERE "+"Tsat_C"+" <= "+str(uservalue)+" ORDER BY ABS"+"("+"Tsat_C"+"-" +str(uservalue)+") "+ "LIMIT 1"
                    for row in cur.execute(cmdlower_val):
                        for i in range(len(row)):
                            tempvarlow.append(str(row[i]))
                    
                    cmdhigher_val="SELECT * FROM "+'"'+str("Saturated_property_T_based")+'"'+" WHERE "+"Tsat_C"+" >= "+str(uservalue)+" ORDER BY ABS"+"("+"Tsat_C"+"-" +str(uservalue)+") "+ "LIMIT 1"
                    for row in cur.execute(cmdhigher_val):
                        for i in range(len(row)):
                            tempvarhigh.append(str(row[i])) 
                    interpolate_var(uservalue, userinp2,tempvarlow,tempvarhigh)
                    tempvarinterpolate[1]=C_to_other(tempvarinterpolate[1],T_unitselection)
                    tempvarinterpolate[2]=Mpa_to_other(tempvarinterpolate[2],P_unitselection)
                    print(tempvarinterpolate)
                    if(chooseunit==0):
                        x_dat=[tempvarinterpolate[1:9]]
                        x=tabulate(x_dat, headers=y_dat)
                        lbdisp_thermo.delete('1.0',END)
                        lbdisp_thermo.insert(INSERT,str(x))
                        x_dat2=[tempvarinterpolate[9::]]
                        x2=tabulate(x_dat2, headers=y_dat2)
                        lbdisp_thermo.insert(INSERT,"\n\n\n")
                        lbdisp_thermo.insert(INSERT,str(x2))
                        print(x)
                    elif(chooseunit==1):
                        for i in range(len(tempvarinterpolate)):
                        	x=3
                        	if(i==x or i==x+1):
                        		tempvarinterpolate[i]=m3_kg_to_ft3_lbm(tempvarinterpolate[i])
                        	elif(i>=x+2 and i<=x+6):
                        		tempvarinterpolate[i]=kj_kg_to_btu_lbm(tempvarinterpolate[i])
                        	elif(i>=x+7 and i<=x+13):
                        		tempvarinterpolate[i]=kj_kg_k_to_btu_lbm_F(tempvarinterpolate[i])
                        	elif(i==x+16 or i==x+17):
                        		tempvarinterpolate[i]=m_s_to_ft_s(tempvarinterpolate[i])
                        	elif(i==x+18 or i==x+19):
                        		tempvarinterpolate[i]=W_m_k_to_BTU_h_ft_F(tempvarinterpolate[i])
                        	elif(i==x+20 or i==x+21):
                        		tempvarinterpolate[i]=N_M_to_lbf_in(tempvarinterpolate[i])
                        x_dat=[tempvarinterpolate[1:9]]
                        x=tabulate(x_dat, headers=y_dat)
                        lbdisp_thermo.delete('1.0',END)
                        lbdisp_thermo.insert(INSERT,str(x))
                        x_dat2=[tempvarinterpolate[9::]]
                        x2=tabulate(x_dat2, headers=y_dat2)
                        lbdisp_thermo.insert(INSERT,"\n\n\n")
                        lbdisp_thermo.insert(INSERT,str(x2))
                        print(x)
                elif(userinp==2):
                    userinp2=1
                    tempvarlow=[]
                    tempvarhigh=[]
                    pressuretempvar_low=[]
                    pressuretempvar_high=[]
                    try:
                        uservalue=float(optionT.get())
                        uservalue=t_conversion(uservalue, T_unitselection)
                    except:
                        uservalue="*"
                        
                    try:
                        pressure=float(optionP.get())
                        pressure=p_conversion(pressure, P_unitselection)
                        print(uservalue)
                        print(pressure)
                    except:
                        pressure=0.01
                    if(uservalue!="*"):
                        cmdlower_val='SELECT * FROM "Single_phase_property" WHERE (P_Mpa <={pv}) AND (T_C <={tv}) ORDER BY ABS(P_Mpa-{pv}),ABS(T_C-{tv}) LIMIT 1'.format(tv=uservalue,pv=pressure)
                        cmdhigher_val='SELECT * FROM "Single_phase_property" WHERE (P_Mpa <={pv}) AND (T_C >={tv}) ORDER BY ABS(P_Mpa-{pv}),ABS(T_C-{tv}) LIMIT 1'.format(tv=uservalue,pv=pressure)
                        for row in cur.execute(cmdlower_val):
                            for i in range(len(row)):
                                tempvarlow.append(str(row[i]))
                                
                        for row in cur.execute(cmdhigher_val):
                            for i in range(len(row)):
                                tempvarhigh.append(str(row[i])) 
                        interpolate_var(uservalue,1,tempvarlow,tempvarhigh)
                        pressuretempvar_low=tempvarinterpolate
                        tempvarlow=[]
                        tempvarhigh=[]
                        cmdlower_val='SELECT * FROM "Single_phase_property" WHERE (P_Mpa >={pv}) AND (T_C <={tv}) ORDER BY ABS(P_Mpa-{pv}),ABS(T_C-{tv}) LIMIT 1'.format(tv=uservalue,pv=pressure)
                        cmdhigher_val='SELECT * FROM "Single_phase_property" WHERE (P_Mpa >={pv}) AND (T_C >={tv}) ORDER BY ABS(P_Mpa-{pv}),ABS(T_C-{tv}) LIMIT 1'.format(tv=uservalue,pv=pressure)
                        for row in cur.execute(cmdlower_val):
                            for i in range(len(row)):
                                tempvarlow.append(str(row[i]))
                                
                        for row in cur.execute(cmdhigher_val):
                            for i in range(len(row)):
                                tempvarhigh.append(str(row[i])) 
                        interpolate_var(uservalue,1,tempvarlow,tempvarhigh)
                        pressuretempvar_high=tempvarinterpolate
                        interpolate_var(pressure,2,pressuretempvar_low,pressuretempvar_high)
                        tempvarinterpolate[1]=C_to_other(tempvarinterpolate[1],T_unitselection)
                        tempvarinterpolate[2]=Mpa_to_other(tempvarinterpolate[2],P_unitselection)
                        if(chooseunit==1):
                            for i in range(len(tempvarinterpolate)):
                            	x=3
                            	if(i==x):
                            		tempvarinterpolate[i]=m3_kg_to_ft3_lbm(tempvarinterpolate[i])
                            	elif(i>=x+1 and i<=x+2):
                            		tempvarinterpolate[i]=kj_kg_to_btu_lbm(tempvarinterpolate[i])
                            	elif(i>=x+3):
                            		tempvarinterpolate[i]=kj_kg_k_to_btu_lbm_F(tempvarinterpolate[i])
                        # elif(i==x+16 or i==x+17):
                    	# 	tempvarinterpolate[i]=m_s_to_ft_s(tempvarinterpolate[i])
                    	# elif(i==x+18 or i==x+19):
                    	# 	tempvarinterpolate[i]=W_m_k_to_BTU_h_ft_F(tempvarinterpolate[i])
                    	# elif(i==x+20 or i==x+21):
                    	# 	tempvarinterpolate[i]=N_M_to_lbf_in(tempvarinterpolate[i])
                        x_dat=[tempvarinterpolate[1::]]
                        x=tabulate(x_dat, headers=y_dat_SP)
                        lbdisp_thermo.delete('1.0',END)
                        lbdisp_thermo.insert(INSERT,str(x))
                    else:
                        T_low=0.0
                        T_high=0.0
                        tempvarstorelow=[]
                        tempvarstorehigh=[]
                        xlowwater=[]
                        xlowsteam=[]
                        xhighwater=[]
                        xhighsteam=[]
                        cmd_val_low='SELECT * FROM "Single_phase_property" WHERE (P_Mpa <={pv}) GROUP BY T_C HAVING (COUNT(T_C)==2) ORDER BY ABS(P_Mpa-{pv}) LIMIT 1'.format(pv=pressure)
                        for row in cur.execute(cmd_val_low):
                            T_low=float(row[1])
                        cmd_val_low='SELECT * FROM "Single_phase_property" WHERE T_C={tv} LIMIT 2'.format(tv=T_low)
                        for row in cur.execute(cmd_val_low):
                            for i in range(len(row)):
                                tempvarstorelow.append(row[i])
                        xlowwater=tempvarstorelow[0:7]
                        xlowsteam=tempvarstorelow[7::]
                        print(xlowwater)
                        print(xlowsteam)
                        cmd_val_high='SELECT * FROM "Single_phase_property" WHERE (P_Mpa >={pv}) GROUP BY T_C HAVING (COUNT(T_C)==2) ORDER BY ABS(P_Mpa-{pv}) LIMIT 1'.format(pv=pressure)
                        for row in cur.execute(cmd_val_high):
                            T_high=float(row[1])
                        cmd_val_high='SELECT * FROM "Single_phase_property" WHERE T_C={tv} LIMIT 2'.format(tv=T_high)
                        for row in cur.execute(cmd_val_high):
                            for i in range(len(row)):
                                tempvarstorehigh.append(row[i])
                        xhighwater=tempvarstorehigh[0:7]
                        xhighsteam=tempvarstorehigh[7::]
                        print("__________")
                        print(xhighwater)
                        print(xhighsteam)
                        interpolate_var(pressure,2,xlowwater,xhighwater)
                        if(chooseunit==1):
                            for i in range(len(tempvarinterpolate)):
                            	x=3
                            	if(i==x):
                            		tempvarinterpolate[i]=m3_kg_to_ft3_lbm(tempvarinterpolate[i])
                            	elif(i>=x+1 and i<=x+2):
                            		tempvarinterpolate[i]=kj_kg_to_btu_lbm(tempvarinterpolate[i])
                            	elif(i>=x+3):
                            		tempvarinterpolate[i]=kj_kg_k_to_btu_lbm_F(tempvarinterpolate[i])
                        # elif(i==x+16 or i==x+17):
                    	# 	tempvarinterpolate[i]=m_s_to_ft_s(tempvarinterpolate[i])
                    	# elif(i==x+18 or i==x+19):
                    	# 	tempvarinterpolate[i]=W_m_k_to_BTU_h_ft_F(tempvarinterpolate[i])
                    	# elif(i==x+20 or i==x+21):
                    	# 	tempvarinterpolate[i]=N_M_to_lbf_in(tempvarinterpolate[i])
                        tempvarinterpolate[1]=C_to_other(tempvarinterpolate[1],T_unitselection)
                        tempvarinterpolate[2]=Mpa_to_other(tempvarinterpolate[2],P_unitselection)
                        x_dat=[tempvarinterpolate[1::]]
                        x=tabulate(x_dat, headers=y_dat_SP)
                        lbdisp_thermo.delete('1.0',END)
                        lbdisp_thermo.insert(INSERT,str(x))
                        interpolate_var(pressure,2,xlowsteam,xhighsteam)
                        if(chooseunit==1):
                            for i in range(len(tempvarinterpolate)):
                            	x=3
                            	if(i==x):
                            		tempvarinterpolate[i]=m3_kg_to_ft3_lbm(tempvarinterpolate[i])
                            	elif(i>=x+1 and i<=x+2):
                            		tempvarinterpolate[i]=kj_kg_to_btu_lbm(tempvarinterpolate[i])
                            	elif(i>=x+3):
                            		tempvarinterpolate[i]=kj_kg_k_to_btu_lbm_F(tempvarinterpolate[i])
                        # elif(i==x+16 or i==x+17):
                    	# 	tempvarinterpolate[i]=m_s_to_ft_s(tempvarinterpolate[i])
                    	# elif(i==x+18 or i==x+19):
                    	# 	tempvarinterpolate[i]=W_m_k_to_BTU_h_ft_F(tempvarinterpolate[i])
                    	# elif(i==x+20 or i==x+21):
                    	# 	tempvarinterpolate[i]=N_M_to_lbf_in(tempvarinterpolate[i])
                        tempvarinterpolate[1]=C_to_other(tempvarinterpolate[1],T_unitselection)
                        tempvarinterpolate[2]=Mpa_to_other(tempvarinterpolate[2],P_unitselection)
                        x_dat=[tempvarinterpolate[1::]]
                        x=tabulate(x_dat, headers=y_dat_SP).split("\n")[2]
                        lbdisp_thermo.insert(INSERT,str("\n"))
                        lbdisp_thermo.insert(INSERT,str(x))
            elif(iapwsversion==97):
                if(userinp==0):
                    try:
                        uservalue=float(optionP.get())
                        uservalue=p_conversion(uservalue, P_unitselection)
                        print(uservalue)
                    except:
                        uservalue=1
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(P_sat_funct, uservalue)
                        return_value = future.result()
                        y=return_value
                    print(y)
                    tempvarinterpolate=y[0]
                    tempvarinterpolate[0]=C_to_other(tempvarinterpolate[0],T_unitselection)
                    tempvarinterpolate[1]=Mpa_to_other(tempvarinterpolate[1],P_unitselection)
                    if(chooseunit==1):
                        for i in range(len(tempvarinterpolate)):
                        	x=2
                        	if(i==x or i==x+1):
                        		tempvarinterpolate[i]=m3_kg_to_ft3_lbm(tempvarinterpolate[i])
                        	elif(i>=x+2 and i<=x+6):
                        		tempvarinterpolate[i]=kj_kg_to_btu_lbm(tempvarinterpolate[i])
                        	elif(i>=x+7 and i<=x+13):
                        		tempvarinterpolate[i]=kj_kg_k_to_btu_lbm_F(tempvarinterpolate[i])
                        	elif(i==x+16 or i==x+17):
                        		tempvarinterpolate[i]=m_s_to_ft_s(tempvarinterpolate[i])
                        	elif(i==x+18 or i==x+19):
                        		tempvarinterpolate[i]=W_m_k_to_BTU_h_ft_F(tempvarinterpolate[i])
                        	elif(i==x+20 or i==x+21):
                        		tempvarinterpolate[i]=N_M_to_lbf_in(tempvarinterpolate[i])
                    x_dat=[tempvarinterpolate[0:8]]
                    x=tabulate(x_dat, headers=y_dat)
                    print(x)
                    lbdisp_thermo.delete('1.0',END)
                    lbdisp_thermo.insert(INSERT,str(x))
                    x_dat2=[tempvarinterpolate[8:14]]
                    x2=tabulate(x_dat2, headers=y_dat2)
                    lbdisp_thermo.insert(INSERT,"\n\n\n")
                    lbdisp_thermo.insert(INSERT,str(x2))
                    print(x2)
                    x_dat3=[tempvarinterpolate[14:22]]
                    x3=tabulate(x_dat3, headers=y_dat3)
                    lbdisp_thermo.insert(INSERT,"\n\n\n")
                    lbdisp_thermo.insert(INSERT,str(x3))
                    x_dat4=[tempvarinterpolate[22::]]
                    x4=tabulate(x_dat4, headers=y_dat4)
                    lbdisp_thermo.insert(INSERT,"\n\n\n")
                    lbdisp_thermo.insert(INSERT,str(x4))
                    
                elif(userinp==1):
                    try:
                        uservalue=float(optionT.get())
                        uservalue=t_conversion(uservalue, T_unitselection)
                        print(uservalue)
                    except:
                        uservalue=0.1
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(T_sat_funct, uservalue)
                        return_value = future.result()
                        y=return_value
                    print(y)
                    tempvarinterpolate=y[0]
                    tempvarinterpolate[0]=C_to_other(tempvarinterpolate[0],T_unitselection)
                    tempvarinterpolate[1]=Mpa_to_other(tempvarinterpolate[1],P_unitselection)
                    if(chooseunit==1):
                        for i in range(len(tempvarinterpolate)):
                        	x=2
                        	if(i==x or i==x+1):
                        		tempvarinterpolate[i]=m3_kg_to_ft3_lbm(tempvarinterpolate[i])
                        	elif(i>=x+2 and i<=x+6):
                        		tempvarinterpolate[i]=kj_kg_to_btu_lbm(tempvarinterpolate[i])
                        	elif(i>=x+7 and i<=x+13):
                        		tempvarinterpolate[i]=kj_kg_k_to_btu_lbm_F(tempvarinterpolate[i])
                        	elif(i==x+16 or i==x+17):
                        		tempvarinterpolate[i]=m_s_to_ft_s(tempvarinterpolate[i])
                        	elif(i==x+18 or i==x+19):
                        		tempvarinterpolate[i]=W_m_k_to_BTU_h_ft_F(tempvarinterpolate[i])
                        	elif(i==x+20 or i==x+21):
                        		tempvarinterpolate[i]=N_M_to_lbf_in(tempvarinterpolate[i])
                    x_dat=[tempvarinterpolate[0:8]]
                    x=tabulate(x_dat, headers=y_dat)
                    print(x)
                    lbdisp_thermo.delete('1.0',END)
                    lbdisp_thermo.insert(INSERT,str(x))
                    x_dat2=[tempvarinterpolate[8:14]]
                    x2=tabulate(x_dat2, headers=y_dat2)
                    lbdisp_thermo.insert(INSERT,"\n\n\n")
                    lbdisp_thermo.insert(INSERT,str(x2))
                    print(x2)
                    x_dat3=[tempvarinterpolate[14:22]]
                    x3=tabulate(x_dat3, headers=y_dat3)
                    lbdisp_thermo.insert(INSERT,"\n\n\n")
                    lbdisp_thermo.insert(INSERT,str(x3))
                    x_dat4=[tempvarinterpolate[22::]]
                    x4=tabulate(x_dat4, headers=y_dat4)
                    lbdisp_thermo.insert(INSERT,"\n\n\n")
                    lbdisp_thermo.insert(INSERT,str(x4))
                elif(userinp==2):
                    try:
                        uservalue=float(optionT.get())
                        uservalue=t_conversion(uservalue, T_unitselection)
                    except:
                        uservalue=100
                        
                    try:
                        pressure=float(optionP.get())
                        pressure=p_conversion(pressure, P_unitselection)
                        print(uservalue)
                        print(pressure)
                    except:
                        pressure=10
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(P_T_REG, pressure,uservalue)
                        return_value = future.result()
                        y=return_value
                    print(y)
                    tempvarinterpolate=y[0]
                    tempvarinterpolate[0]=C_to_other(tempvarinterpolate[0],T_unitselection)
                    tempvarinterpolate[1]=Mpa_to_other(tempvarinterpolate[1],P_unitselection)
                    if(chooseunit==1):
                            for i in range(len(tempvarinterpolate)):
                            	x=2
                            	if(i==x):
                            		tempvarinterpolate[i]=m3_kg_to_ft3_lbm(tempvarinterpolate[i])
                            	elif(i>=x+1 and i<=x+2):
                            		tempvarinterpolate[i]=kj_kg_to_btu_lbm(tempvarinterpolate[i])
                            	elif(i>=x+3):
                            		tempvarinterpolate[i]=kj_kg_k_to_btu_lbm_F(tempvarinterpolate[i])
                        # elif(i==x+16 or i==x+17):
                    	# 	tempvarinterpolate[i]=m_s_to_ft_s(tempvarinterpolate[i])
                    	# elif(i==x+18 or i==x+19):
                    	# 	tempvarinterpolate[i]=W_m_k_to_BTU_h_ft_F(tempvarinterpolate[i])
                    	# elif(i==x+20 or i==x+21):
                    	# 	tempvarinterpolate[i]=N_M_to_lbf_in(tempvarinterpolate[i])
                    x_dat=[tempvarinterpolate[0:6]]
                    x=tabulate(x_dat, headers=y_dat_SP)
                    lbdisp_thermo.delete('1.0',END)
                    lbdisp_thermo.insert(INSERT,str(x))
        except:
            lbdisp_thermo.delete('1.0',END)
            x="PRESSURE OR TEMPERATURE IS OUT OF RANGE\nSATURATION PRESSURE <= 22.064 MPa or 3200.1126 PSI and SATURATION TEMPERATURE <= 373.946 C or 705.1028 F"
            lbdisp_thermo.insert(INSERT,str(x))
            print("ERROR")
        lbdisp_thermo.configure(state='disabled')
        
    solve_thermo.configure(command=steam_table_value)
    
    
    enteroption = ttk.Frame(IR_ESTIMATE)
    enteroption.grid(row=0,column=0, padx=5,pady=5,sticky=N)
    optttkLabel=ttk.Label(enteroption, text="IR wavenumber (per cm)", justify='center',font=("Arial", 13,"bold")).pack(side=TOP)
    option=Entry(enteroption, width=25,font=("Arial", 12))
    option.pack(anchor=NW,fill="x")
    solve_ir=ttk.Button(enteroption, text="Estimate Functional Group",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    solve_ir.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    updatedb=ttk.Button(enteroption, text="Update Database",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    updatedb.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    help1=ttk.Button(enteroption, text="Help",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    help1.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    typevib=ttk.Frame(IR_ESTIMATE)
    typevib.grid(row=0,column=2,padx=5,pady=5,sticky=N)
    lb1=ttk.Label(typevib, text="Choose Type of Vibration", justify='center',font=("Arial", 13,"bold")).pack(side=TOP)
    listvib = Listbox(typevib, activestyle='none',width=26, height=8, justify='center',font=("Arial", 12),selectmode=BROWSE,exportselection=False)
    listvib.pack(side=LEFT, fill="x")
    typeir_fg=ttk.Frame(IR_ESTIMATE)
    typeir_fg.grid(row=0,column=1,padx=5,pady=5,sticky=N)
    lb1=ttk.Label(typeir_fg, text="Choose Chemical Group",justify='center', font=("Arial", 13,"bold")).pack(side=TOP)
    option2=Entry(typeir_fg, width=26,font=("Arial", 12))
    option2.pack(side=TOP, anchor=NW,fill="x")
    search=ttk.Button(typeir_fg, text="Search",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    search.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    
    listfunc = Listbox(typeir_fg, activestyle='none',width=40, height=5,justify='center', font=("Arial", 12),selectmode=BROWSE,exportselection=False)
    listfunc.pack(side=LEFT, fill="x")
    scrollbar = Scrollbar(typeir_fg, orient="vertical")
    scrollbar.config(command=listfunc.yview)
    scrollbar.pack(side=RIGHT,anchor=N, fill="y")
    listfunc.config(yscrollcommand=scrollbar.set)
    lbdisp=ScrolledText(ESTIMATE,wrap=WORD,width=109, height=7,padx=2,pady=1,font=('Consolas',11))
    lbdisp.pack(side=LEFT,fill='none')      
    lbdisp.configure(state='disabled')
    while cm!=1:
        ir_func_group() 
        global ir_vib_type
        global ir_func_type
        listfunc.delete('0','end')
        for items in range(len(ir_vib)):
            listvib.insert(items, ir_vib[items])
        for items in range(len(ir_fg)):
            listfunc.insert(items, ir_fg[items])
        lbdisp.configure(state='normal')
        lbdisp.delete('1.0', END)
        lbdisp.insert(INSERT,statement)
        lbdisp.configure(state='disabled')
        listvib.select_set(0)
        listvib.event_generate("<<ListboxSelect>>")
        listfunc.select_set(0)
        listfunc.event_generate("<<ListboxSelect>>")
        cm=1 
    def ir_update():
        update_ir_db()
        lbdisp.configure(state='normal')
        listfunc.delete('0','end')
        for items in range(len(ir_fg)):
            listfunc.insert(items, ir_fg[items])
        statement="\n"+str("-")*108+"\n"+"DATABASE UPDATED SUCCESSFULLY\n"+"\n"+str("-")*108
        lbdisp.delete('1.0', END)
        lbdisp.insert(INSERT,statement)
        lbdisp.configure(state='disabled')
        print(statement)
    def ir_vib_type_choosen(evt):
        global ir_vib_type
        ir_vib_type=str((listvib.get(ANCHOR)))
        print(ir_vib_type)
    def ir_func_type_choosen(evt):
        global ir_func_type
        ir_func_type=str((listfunc.get(ANCHOR)))
        print(ir_func_type)
    def solvefunc():
        lbdisp.configure(state='normal')
        lbdisp.delete('1.0', END)
        x=option.get()
        if(x==''):
            x=0
        global statement
        global dat_check
        global ir_vib_type
        global ir_func_type
        global cmdlineq
        run_once=0
        dat_check=0
        print("SELECTED VIB:",ir_vib_type)
        print("SELECTED func:",ir_func_type)
        if(ir_func_type==''):
            ir_func_type='all'
        if(ir_vib_type=='all' and ir_func_type=='all'):
            cmdlineq='SELECT * FROM IR_DATA WHERE wavenumber_upper>='+str(x)+' AND wavenumber_lower<='+str(x)
        elif(ir_vib_type!='all' and ir_func_type=='all'):
            cmdlineq='SELECT * FROM IR_DATA WHERE type_of_vibration="'+str(ir_vib_type)+'" AND wavenumber_upper>='+str(x)+' AND wavenumber_lower<='+str(x)
        elif(ir_vib_type=='all' and ir_func_type!='all'):
            cmdlineq='SELECT * FROM IR_DATA WHERE group_name="'+str(ir_func_type)+'" AND wavenumber_upper>='+str(x)+' AND wavenumber_lower<='+str(x)
        elif(ir_vib_type!='all' and ir_func_type!='all'):
            cmdlineq='SELECT * FROM IR_DATA WHERE type_of_vibration="'+str(ir_vib_type)+'" AND group_name="'+str(ir_func_type)+'" AND wavenumber_upper>='+str(x)+' AND wavenumber_lower<='+str(x) 
        
        for row in cur.execute(cmdlineq):
            statement_bak="---------------------------------------------------\n"+"WAVENUMBER RANGE: "+str(row[0])+"-"+str(row[1])+"\n"+"FUNCTIONAL GROUP: "+str(row[4])+"\n"+"TYPE OF VIBRATION: "+str(row[5]).upper()+"\n"+"PROBABLE CHEMICAL GROUP: "+str(row[6]).upper()+"\n"+"OTHER PROPERTY: "+str(row[7]).upper()+"\n"
            x_dat=[[str(str(row[0])+'-'+str(row[1])),str(row[4]),str(row[5]),str(row[6]),str(row[7])]]
            y_dat=["WAVENUMBER(per cm)","FUNCTIONAL GROUP","VIBRATION TYPE","CHEMICAL GROUP","OTHER PROPERTY"]
            statement=tabulate(x_dat, headers=y_dat,tablefmt='simple')
            # print(statement_bak)
            if(run_once==0):
                # print(statement)
                lbdisp.insert(INSERT,statement)
                run_once=1
            elif(run_once==1):
                statement=statement.split("\n")[2]
                # print(statement)
                lbdisp.insert(INSERT,str("\n"))
                lbdisp.insert(INSERT,statement)
            dat_check+=1;
        if(dat_check<1):
            statement="NO DATA FOUND WITHIN RANGE"
            # print(statement)
            lbdisp.insert(INSERT,statement)
        statement="\n"+str("-")*108+"\n"+'TOTAL NUMBER OF MATCHES: '+str(dat_check).zfill(2)+"\n"+str("-")*108+"\n"
        lbdisp.insert(INSERT,statement)
        lbdisp.configure(state='disabled')
        
    solve_ir.configure(command=solvefunc)
    
    def ir_new_list_find(event):
        listfunc.delete('0','end')
        global ir_vib_type
        global ir_func_type
        global list_item
        global ir_fg
        list_item=option2.get()
        if(list_item==''):
            ir_func_group() 
            listfunc.delete('0', END)
            for items in range(len(ir_fg)):
                listfunc.insert(items, ir_fg[items])
            listfunc.select_set(0)
            listfunc.event_generate("<<ListboxSelect>>")
            lbdisp.configure(state='normal')
            lbdisp.delete('1.0', END)
            lbdisp.configure(state='disabled')
        else:
            indices = [i for i, s in enumerate(ir_fg) if list_item in s]
            new_list=list()
            for i in indices:
                new_list.append(ir_fg[i])
            for items in range(len(new_list)):
                listfunc.insert(items, new_list[items])
        print(ir_func_type)
        print(ir_vib_type)
    def ir_help_me():
        lbdisp.configure(state='normal')
        lbdisp.delete('1.0', END)
        statement='-'*52+"HELP"+'-'*52+"\nEnter the infrared spectrum wavenumber. Then select Estimate Functional Group button to show the corresponding matching functional groups. You can also limit the chemical group and type of vibration by choosing the options from the listbox. Once in a year or two, you can update the database for any new compounds\n"+'-'*52+"END"+'-'*53
        lbdisp.insert(INSERT,statement)
        lbdisp.configure(state='disabled')
    help1.configure(command=ir_help_me)
    updatedb.configure(command=ir_update)
    option2.bind('<Key-Return>',ir_new_list_find)
    listvib.bind('<<ListboxSelect>>',ir_vib_type_choosen)
    listfunc.bind('<<ListboxSelect>>',ir_func_type_choosen)
    search.bind('<Button-1>',ir_new_list_find)
    def ant_chem_list():
        global ant_chem
        global statement
        ant_chem_form=[]
        ant_chem_name=[]
        try:
            cmdlineq="SELECT * FROM"+" 'Antoine Constants'"
            row=cur.fetchone()
            for row in cur.execute(cmdlineq):
                   ant_chem_form.append(str(row[1]))
                   ant_chem_name.append(str(row[2]))
            ant_chem_temp=dict(zip(ant_chem_name, ant_chem_form))
            ant_chem = collections.OrderedDict(sorted(ant_chem_temp.items()))
        except:
            statement="NO DATABASE FOUND PLEASE UPDATE DATABASE!"
    cm_2=0
    ant_main0=ttk.Frame(Antoine_tables)
    ant_main0.grid(row=0,column=0, padx=5,pady=5,ipady=2,sticky=N)  
    lb_ant=ttk.Label(ant_main0, text="Search and Choose Chemical",justify='center', font=("Arial", 13,"bold")).pack(side=TOP)
    option_ant=Entry(ant_main0, width=35,font=("Consolas", 13))
    option_ant.pack(side=TOP,fill="both",pady=4)
    search_ant=ttk.Button(ant_main0, text="Search",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    search_ant.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    sval_ant=ttk.Button(ant_main0, text="Advanced Options",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    sval_ant.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    listfunc_ant = Listbox(ant_main0, width=34, activestyle='none',height=9,justify='center', font=("Arial", 12),selectmode=BROWSE,exportselection=False,takefocus=0)
    listfunc_ant.pack(side=LEFT, pady=10,fill="x")
    scrollbar_ant = Scrollbar(ant_main0, orient="vertical")
    scrollbar_ant.config(command=listfunc_ant.yview)
    scrollbar_ant.pack(pady=10,side=RIGHT,anchor=N, fill="y")
    listfunc_ant.config(yscrollcommand=scrollbar_ant.set)
    
    
    while cm_2!=1:
        ant_chem_list()
        listfunc_ant.delete('0','end')
        part1=''
        part2=''
        for items in range(len(ant_chem)):
            part1=str(list(ant_chem.keys())[items])
            part2=str(list(ant_chem.values())[items])
            listfunc_ant.insert(items, str(part1+' ['+part2+']'))
        cm_2=1

    ant_main1_PRIME=ttk.Frame(Antoine_tables)
    ant_main1_PRIME.grid(row=0,column=1, padx=5,pady=5,ipadx=10,ipady=10,sticky='nsew')
    ant_main1=ttk.Frame(ant_main1_PRIME)
    ant_main1.grid(row=0,column=0, padx=5,pady=5,sticky='nsew')
    ant_chemLabelPressure=ttk.Label(ant_main1, width=15,text="Vapor Pressure: ", justify='center',font=("Arial", 13,"bold")).pack(side=LEFT)
    optionP_ant=Entry(ant_main1, width=9,font=("Consolas", 13))
    optionP_ant.pack(side=LEFT,fill="both",pady=4)
    popupMenupressure_unit_ant = ttk.OptionMenu(ant_main1, tkPressureUnit,pressureunit[0], *pressureunit, command = OptionMenu_SelectionEvent_PressureUnit)
    popupMenupressure_unit_ant.configure(takefocus=0,)
    popupMenupressure_unit_ant.pack(side=LEFT,fill='both',expand=TRUE,anchor=W)
    solve_ant_P_base=ttk.Button(ant_main1, text="Estimate Temperature",takefocus=0)
    solve_ant_P_base.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    
    ant_main2=ttk.Frame(ant_main1_PRIME)
    ant_main2.grid(row=1,column=0, padx=5,pady=5,sticky='nsew')
    ant_chem_labelTemperature=ttk.Label(ant_main2, width=15,text="Temperature: ", justify='center',font=("Arial", 13,"bold")).pack(side=LEFT)
    optionT_ant=Entry(ant_main2, width=9,font=("Consolas", 12))
    optionT_ant.pack(side=LEFT,fill="both",pady=4)
    popupMenuTemp_unit_ant = ttk.OptionMenu(ant_main2, tkTemperatureUnit,temperatureunit[T_unitselection], *temperatureunit, command = OptionMenu_SelectionEvent_TemperatureUnit)
    popupMenuTemp_unit_ant.configure(takefocus=0,)
    popupMenuTemp_unit_ant.pack(side=LEFT,fill='x',expand=TRUE,anchor=NW) 
    solve_ant_T_base=ttk.Button(ant_main2, text="Estimate Vapor Pressure",takefocus=0)
    solve_ant_T_base.pack(side=TOP,anchor=N,fill='both',expand=TRUE)
    ant_main3=ttk.Frame(ant_main1_PRIME)
    ant_main3.grid(row=2,column=0, padx=5,sticky='nsew')
    labelchem=StringVar()
    tmin_chem=StringVar()
    tmax_chem=StringVar()
    A_val=StringVar()
    B_val=StringVar()
    C_val=StringVar()
    chem_title=ttk.Label(ant_main3,text="Chemical:", justify='center',font=("Arial Bold", 12)).pack(pady=5, side=LEFT)
    chem_label=ttk.Label(ant_main3,width=24,textvariable=labelchem, justify='center',font=("Arial", 12)).pack(side=LEFT)
    chem_tmin=ttk.Label(ant_main3,text="T(min):", justify='center',font=("Arial Bold", 12)).pack(side=LEFT)
    chem_tmin_val=ttk.Label(ant_main3, width=7,textvariable=tmin_chem, justify='center',font=("Arial", 12)).pack(side=LEFT)
    chem_tmax=ttk.Label(ant_main3, text="T(max):", justify='center',font=("Arial Bold", 12)).pack(side=LEFT)
    chem_tmax_val=ttk.Label(ant_main3, width=7,textvariable=tmax_chem, justify='center',font=("Arial", 12)).pack(side=LEFT)
    ant_main4=ttk.Frame(ant_main1_PRIME)
    ant_main4.grid(row=3,column=0, padx=2,sticky='nsew')
    ant_A=ttk.Label(ant_main4,text="A: ", justify='center',font=("Arial", 12)).pack(pady=5, side=LEFT)
    ant_A_label=ttk.Label(ant_main4,width=15,textvariable=A_val, justify='center',font=("Arial", 12)).pack(side=LEFT)
    ant_B=ttk.Label(ant_main4,text="B: ", justify='center',font=("Arial", 12)).pack(side=LEFT)
    ant_B_label=ttk.Label(ant_main4, width=15,textvariable=B_val, justify='center',font=("Arial", 12)).pack(side=LEFT)
    ant_C=ttk.Label(ant_main4, text="C: ", justify='center',font=("Arial", 12)).pack(side=LEFT)
    ant_C_label=ttk.Label(ant_main4, width=15,textvariable=C_val, justify='center',font=("Arial", 12)).pack(side=LEFT)
    ant_main5=ttk.Frame(ant_main1_PRIME)
    ant_main5.grid(row=4,column=0, padx=1,sticky='nsew')
    lbdisp_ant=ScrolledText(ant_main5,wrap=WORD, width=65,height=9,font=('Consolas',11))
    lbdisp_ant.pack(side=LEFT,fill='y',padx=6)      
    lbdisp_ant.configure(state='disabled')
    def ant_advanced_settings(evt):
        once=0
        while once!=1:
            lbdisp_ant.configure(state='normal')
            lbdisp_ant.delete('1.0','end')
            statement='Please enter new chemical data as required. Make sure that the formula is log10(P(mmHg))=A-B/(T(°C)+C). All variables are float formated other than names so using comma or other characters will prevent from saving. If T(min) or T(max) values are not available, please set some values like 0 instead. You will get temperature range exceeded error though'
            lbdisp_ant.insert(INSERT,statement)
            lbdisp_ant.configure(state='disabled')
            once=1
        new=Toplevel()
        new.title("Advanced Settings")
        new.geometry("490x300")
        new.resizable('false','false')
        new.lift()
        new.attributes('-topmost',True)
        new['bg']='#ffffff'
        index_val=0
        A_v=StringVar()
        B_v=StringVar()
        C_v=StringVar()
        c_name=StringVar()
        c_form=StringVar()
        T_min_v=StringVar()
        T_max_v=StringVar()
        style_config=ttk.Style()
        style_config.theme_use('adapta')
        style_config.theme_use('adapta')
        style_config.configure("Tab", focuscolor='00bcd4',padx=2,pady=2)
        style_config.configure("TButton", font=("Arial", 12),anchor=CENTER)
        style_config.configure("TMenubutton", font=("Arial", 12),anchor=CENTER)
        ant_adv_entry=ttk.Frame(new)
        ant_adv_entry.grid(row=0,column=0, padx=5,pady=5,sticky='nsew')
        chem_lb_ant=ttk.Label(ant_adv_entry, text="Enter Chemical Name",justify='center', font=("Arial", 13,"bold")).pack(side=TOP)
        chem_name_ant=Entry(ant_adv_entry, textvariable=c_name,width=35,font=("Consolas", 13)).pack(side=TOP,fill="both",pady=4)
        chem_form_lb_ant=ttk.Label(ant_adv_entry, text="Enter Chemical Formula",justify='center', font=("Arial", 13,"bold")).pack(side=TOP)
        chem_form_ant=Entry(ant_adv_entry, textvariable=c_form,width=35,font=("Consolas", 13)).pack(side=TOP,fill="both",pady=4)
        ant_adv_entry2=ttk.Frame(new)
        ant_adv_entry2.grid(row=1,column=0, padx=5,pady=5,sticky='nsew')
        chem_A_lb_ant=ttk.Label(ant_adv_entry2, text="A:",justify='center', font=("Arial", 13,"bold")).pack(side=LEFT)
        chem_A_ant=Entry(ant_adv_entry2, textvariable=A_v,width=15,font=("Consolas", 13)).pack(side=LEFT,fill="both",pady=4)
        chem_B_lb_ant=ttk.Label(ant_adv_entry2, text="B:",justify='center', font=("Arial", 13,"bold")).pack(side=LEFT)
        chem_B_ant=Entry(ant_adv_entry2, textvariable=B_v,width=15,font=("Consolas", 13)).pack(side=LEFT,fill="both",pady=4)
        chem_C_lb_ant=ttk.Label(ant_adv_entry2, text="C:",justify='center', font=("Arial", 13,"bold")).pack(side=LEFT)
        chem_C_ant=Entry(ant_adv_entry2, textvariable=C_v,width=15,font=("Consolas", 13)).pack(side=LEFT,fill="both",pady=4)
        ant_adv_entry3=ttk.Frame(new)
        ant_adv_entry3.grid(row=2,column=0, padx=5,pady=5,sticky='nsew')
        chem_Tmin_lb_ant=ttk.Label(ant_adv_entry3, text="T(min)(°C):",justify='center', font=("Arial", 13,"bold")).pack(side=LEFT)
        chem_Tmin_ant=Entry(ant_adv_entry3, textvariable=T_min_v,width=16,font=("Consolas", 13)).pack(side=LEFT,fill="both",pady=4)
        chem_Tmax_lb_ant=ttk.Label(ant_adv_entry3, text="T(max)(°C):",justify='center', font=("Arial", 13,"bold")).pack(side=LEFT)
        chem_Tmax_ant=Entry(ant_adv_entry3, textvariable=T_max_v,width=16,font=("Consolas", 13)).pack(side=LEFT,fill="both",pady=4)
        def button_adv():
            command1='SELECT "index" FROM "Antoine Constants" ORDER BY "index" DESC LIMIT 1'
            for row in cur.execute(command1):
                index_val=row[0]  
            try:
                print(int(index_val)+1,str(c_form.get()),str(c_name.get()),float(A_v.get()),float(B_v.get()),float(C_v.get()),float(T_min_v.get()),float(T_max_v.get()))
                command3='INSERT INTO ' +'"Antoine Constants"'+' ("index",formula,"compound name",A,B,C,Tmin,Tmax) VALUES (?,?,?,?,?,?,?,?)'
                cur.execute(command3, (int(int(index_val)+1),str(c_form.get()),str(c_name.get()),float(A_v.get()),float(B_v.get()),float(C_v.get()),float(T_min_v.get()),float(T_max_v.get())))
                conn.commit()
                lbdisp_ant.configure(state='normal')
                lbdisp_ant.insert(INSERT,'\n')
                statement='SAVED SUCCESSFULLY!'
                lbdisp_ant.insert(INSERT,statement,'good')
                lbdisp_ant.tag_configure('good',background='green',foreground='white')
                lbdisp_ant.configure(state='disabled')
            except:
                lbdisp_ant.configure(state='normal')
                lbdisp_ant.insert(INSERT,'\n')
                statement='ERROR OCCURED! PLEASE CHECK VALUES!'
                lbdisp_ant.insert(INSERT,statement,'error')
                lbdisp_ant.tag_configure('error',background='red',foreground='white')
                lbdisp_ant.configure(state='disabled')
            ant_chem_list()
            listfunc_ant.delete('0','end')
            part1=''
            part2=''
            for items in range(len(ant_chem)):
                part1=str(list(ant_chem.keys())[items])
                part2=str(list(ant_chem.values())[items])
                listfunc_ant.insert(items, str(part1+' ['+part2+']'))
        def delete_custom():
            command4='DELETE FROM "Antoine Constants" WHERE "index">700'
            cur.execute(command4)
            conn.commit()
            lbdisp_ant.configure(state='normal')
            lbdisp_ant.insert(INSERT,'\n')
            statement='ALL CUSTOM VALUES ARE DELETED PERMANENTLY'
            lbdisp_ant.insert(INSERT,statement,'error')
            lbdisp_ant.tag_configure('error',background='red',foreground='white')
            lbdisp_ant.configure(state='disabled')
            ant_chem_list()
            listfunc_ant.delete('0','end')
            part1=''
            part2=''
            for items in range(len(ant_chem)):
                part1=str(list(ant_chem.keys())[items])
                part2=str(list(ant_chem.values())[items])
                listfunc_ant.insert(items, str(part1+'['+part2+']'))
        ant_adv_entry4=ttk.Frame(new)
        ant_adv_entry4.grid(row=3,column=0, padx=5,pady=5,sticky='nsew')
        updatedb_ant=ttk.Button(ant_adv_entry4, text="ADD CUSTOM DATA",takefocus=0,command=button_adv)
        updatedb_ant.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
        deletedb_ant=ttk.Button(ant_adv_entry4, text="DELETE ALL CUSTOM DATA",takefocus=0,command=delete_custom)
        deletedb_ant.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    def ant_chem_choosen(evt):
        global chosen_ant_chem
        global antoine_constants
        global ant_tmin
        global ant_tmax
        global T_unitselection
        chosen_ant_chem=str((listfunc_ant.get(ANCHOR)))
        labelchem.set(str(chosen_ant_chem.split('[')[0]))
        ant_tmin=''
        ant_tmax=''
        cmdlineq='SELECT * FROM'+' "Antoine Constants"'+'WHERE '+'"compound name"'+'='+'"'+str(chosen_ant_chem.split('[')[0]).strip()+'"'+' COLLATE NOCASE'
        row=cur.fetchone()
        print(str(chosen_ant_chem))
        for row in cur.execute(cmdlineq):
            ant_tmin=(str(row[6]))
            ant_tmax=(str(row[7]))
            antoine_constants['A']=float(row[3])
            antoine_constants['B']=float(row[4])
            antoine_constants['C']=float(row[5])
        A_val.set(antoine_constants['A'])
        B_val.set(antoine_constants['B'])
        C_val.set(antoine_constants['C'])
        tmin_chem.set(str(round(C_to_other(ant_tmin, T_unitselection),2))+str(T_UNITDISP))
        tmax_chem.set(str(round(C_to_other(ant_tmax, T_unitselection),2))+str(T_UNITDISP))
    def ant_chem_list_find(event):
        global ant_chem
        global find_type_ant
        find_type_ant=0
        new_list=[]
        list_item=option_ant.get()
        list_item=list_item.replace(" ",'-')
        listfunc_ant.delete('0','end')
        indices=[]
        part1=''
        part2=''
        if(list_item==''):
            ant_chem_list()
            listfunc_ant.delete('0','end')
            for items in range(len(ant_chem)):
                part1=str(list(ant_chem.keys())[items])
                part2=str(list(ant_chem.values())[items])
                listfunc_ant.insert(items, str(part1+' ['+part2+']'))
        else:
            for i,chem_name in enumerate(list(ant_chem.keys())):
                if list_item.lower() in chem_name:
                    indices.append(i)
            if(len(indices)==0):
                find_type_ant=1
                for i,chem_form in enumerate(list(ant_chem.values())):
                    if list_item == chem_form:
                        indices.append(i)
            if(find_type_ant==0):
                for i in indices:
                    part1=str(list(ant_chem.keys())[i])
                    part2=str(list(ant_chem.values())[i])
                    new_list.append(str(part1+' ['+part2+']'))
            elif(find_type_ant==1):
                for i in indices:
                    part1=str(list(ant_chem.keys())[i])
                    part2=str(list(ant_chem.values())[i])
                    new_list.append(str(part1+' ['+part2+']'))
            for items in range(len(new_list)):
                listfunc_ant.insert(items, new_list[items])
            print(list_item)
            print(len(new_list))
            print(len(list(ant_chem.keys())))
    def estimate_vapor_pressure(evt):
        global T_unitselection
        global P_unitselection
        global ant_tmax
        global ant_tmin
        lbdisp_ant.configure(state='normal')
        lbdisp_ant.delete('1.0', END)
        chosen_ant_chem=str((listfunc_ant.get(ANCHOR)))
        statement=''
        try:
            A=antoine_constants['A']#GET
            B=antoine_constants['B']#GET
            C=antoine_constants['C']#GET
            T_val=optionT_ant.get()
            if(T_val==''):
                statement='Please enter temperature\n'
                lbdisp_ant.insert(INSERT,statement)
                pass
            else:
                T_val=float(T_val)
            T=t_conversion(T_val, T_unitselection)
            vP=10**(A-B/(T+C))
            vP=float(vP)/7500.6157584565623439424245176757#convert to MPa
            T_OUT=C_to_other(T, T_unitselection)    
            P_OUT=Mpa_to_other(vP, P_unitselection)            
            y_dat=['Chemical Name','T('+T_UNITDISP+')','P('+P_UNITDISP+')']
            x_dat=[[chosen_ant_chem.split('[')[0].strip(),T_OUT,P_OUT]]
            x=tabulate(x_dat, headers=y_dat)
            lbdisp_ant.insert(INSERT,x)
            if(T>float(ant_tmax) or T<float(ant_tmin)):
                lbdisp_ant.insert(INSERT,'\n')
                statement='Temperature range is exceeded'
                lbdisp_ant.insert(INSERT,statement,'error')
                lbdisp_ant.tag_configure('error',background='red',foreground='white')
        except:
            statement='Please choose the chemical'
            lbdisp_ant.insert(INSERT,statement)
        lbdisp_ant.configure(state='disabled')
    def estimate_temperature_from_vapor_pressure(evt):
        global T_unitselection
        global P_unitselection
        global ant_tmax
        global ant_tmin
        lbdisp_ant.configure(state='normal')
        lbdisp_ant.delete('1.0', END)
        chosen_ant_chem=str((listfunc_ant.get(ANCHOR)))
        statement=''
        try:
            A=antoine_constants['A']#GET
            B=antoine_constants['B']#GET
            C=antoine_constants['C']#GET
            P_val=optionP_ant.get()
            if(P_val==''):
                statement='Please enter vapor pressure\n'
                lbdisp_ant.insert(INSERT,statement)
                pass
            else:
                P_val=float(P_val)
            P=p_conversion(P_val, P_unitselection)
            PmmHg=float(P)*7500.6157584565623439424245176757#convert to mmHg
            T=B/(A-math.log10(PmmHg))-C
            T_OUT=C_to_other(T, T_unitselection)    
            P_OUT=Mpa_to_other(P, P_unitselection)            
            y_dat=['Chemical Name','P('+P_UNITDISP+')','T('+T_UNITDISP+')']
            x_dat=[[chosen_ant_chem.split('[')[0].strip(),P_OUT,T_OUT]]
            x=tabulate(x_dat, headers=y_dat)
            lbdisp_ant.insert(INSERT,x)
            if(T>float(ant_tmax) or T<float(ant_tmin)):
                lbdisp_ant.insert(INSERT,'\n')
                statement='Temperature range is exceeded'
                lbdisp_ant.insert(INSERT,statement,'error')
                lbdisp_ant.tag_configure('error',background='red',foreground='white')
        except:
            statement='Please choose the chemical'
            lbdisp_ant.insert(INSERT,statement)
        lbdisp_ant.configure(state='disabled')
    listfunc_ant.bind('<<ListboxSelect>>',ant_chem_choosen)
    search_ant.bind('<Button-1>',ant_chem_list_find)
    sval_ant.bind('<Button-1>',ant_advanced_settings)
    option_ant.bind('<Key-Return>',ant_chem_list_find)
    solve_ant_P_base.bind('<Button-1>',estimate_temperature_from_vapor_pressure)
    solve_ant_T_base.bind('<Button-1>',estimate_vapor_pressure)
    
    ######################################################################
    
    def crt_chem_list():
        global crt_chem
        global statement
        crt_chem_form=[]
        crt_chem_name=[]
        try:
            cmdlineq="SELECT * FROM"+" 'Critical Constants'"
            row=cur.fetchone()
            for row in cur.execute(cmdlineq):
                   crt_chem_form.append(str(row[1]))
                   crt_chem_name.append(str(row[2]))
            crt_chem_temp=dict(zip(crt_chem_name, crt_chem_form))
            crt_chem = collections.OrderedDict(sorted(crt_chem_temp.items()))
        except:
            statement="NO DATABASE FOUND PLEASE UPDATE DATABASE!"
            
    cm_3=0
    crt_main0=ttk.Frame(critical_tables)
    crt_main0.grid(row=0,column=0, padx=5,pady=5,ipady=2,sticky=N)  
    lb_crt=ttk.Label(crt_main0, text="Search and Choose Chemical",justify='center', font=("Arial", 13,"bold")).pack(side=TOP)
    option_crt=Entry(crt_main0, width=43,font=("Consolas", 13))
    option_crt.pack(side=TOP,fill="both",pady=4)
    
    search_crt=ttk.Button(crt_main0, text="Search",takefocus=0)#, font=("Arial", 13,"bold"), height=1, width=23)
    search_crt.pack(side=TOP,anchor=N,fill='x',expand=TRUE)
    # popupMenuCHOOSE_unit_crt = ttk.OptionMenu(crt_main0, tkUNITS,outputunit[0], *outputunit, command = OptionMenu_SelectionEvent_UNITS)
    # popupMenuCHOOSE_unit_crt.configure(width=43,takefocus=0,)
    # popupMenuCHOOSE_unit_crt.pack(side=TOP,fill='y',expand=TRUE,anchor=NW) 
    listfunc_crt = Listbox(crt_main0, width=45, activestyle='none',height=11,justify='left', font=("Arial", 12),selectmode=BROWSE,exportselection=False,takefocus=0)
    listfunc_crt.pack(side=LEFT, pady=10,fill="x")
    scrollbar_crt = Scrollbar(crt_main0, orient="vertical")
    scrollbar_crt.config(command=listfunc_crt.yview)
    scrollbar_crt.pack(pady=10,side=RIGHT,anchor=N, fill="both")
    listfunc_crt.config(yscrollcommand=scrollbar_crt.set)
    
    
    
    while cm_3!=1:
        crt_chem_list()
        listfunc_crt.delete('0','end')
        part1=''
        part2=''
        for items in range(len(crt_chem)):
            part1=str(list(crt_chem.keys())[items])
            part2=str(list(crt_chem.values())[items])
            listfunc_crt.insert(items, str(part1+' ['+part2+']'))
        cm_3=1


    crt_main1_PRIME=ttk.Frame(critical_tables)
    crt_main1_PRIME.grid(row=0,column=1, padx=5,pady=5,ipadx=10,ipady=10,sticky='nsew')
    crt_main1=ttk.Frame(crt_main1_PRIME)
    crt_main1.grid(row=0,column=0, padx=5,pady=2,sticky='nsew')
    crt_chemLabelPressure=ttk.Label(crt_main1, width=20,text="Pressure Unit: ", justify='center',font=("Arial", 13,"bold")).pack(side=LEFT)
    popupMenupressure_unit_crt = ttk.OptionMenu(crt_main1, tkPressureUnit,pressureunit[0], *pressureunit, command = OptionMenu_SelectionEvent_PressureUnit)
    popupMenupressure_unit_crt.configure(takefocus=0,)
    popupMenupressure_unit_crt.pack(side=LEFT,fill='both',expand=TRUE,anchor=W)
    crt_main2=ttk.Frame(crt_main1_PRIME)
    crt_main2.grid(row=1,column=0, padx=5,pady=2,sticky='nsew')
    ant_chem_labelTemperature=ttk.Label(crt_main2, width=20,text="Temperature Unit: ", justify='center',font=("Arial", 13,"bold")).pack(side=LEFT)
    popupMenuTemp_unit_ant = ttk.OptionMenu(crt_main2, tkTemperatureUnit,temperatureunit[T_unitselection], *temperatureunit, command = OptionMenu_SelectionEvent_TemperatureUnit)
    popupMenuTemp_unit_ant.configure(takefocus=0,)
    popupMenuTemp_unit_ant.pack(side=LEFT,fill='x',expand=TRUE,anchor=NW) 
    crt_main3=ttk.Frame(crt_main1_PRIME)
    crt_main3.grid(row=2,column=0, padx=2,sticky='nsew')
    solution_crt=ScrolledText(crt_main3, padx=5,width=46,height=12,font=("Consolas", 12))
    solution_crt.pack(pady=2,anchor=NW)
    
    
    
    def crt_chem_choosen(evt):
        global chosen_crt_chem
        global critical_constants
        global T_unitselection
        global P_unitselection
        global chooseunit
        y_dat0=['FORMULA','CAS-NO.','MW(g/mol)']
        y_dat1=['Tf','Tb','Tc','Pc']   
        y_dat2=['Vc(cc/mol)','Rho(g/mol)','Zc','Omega']
        y_datT=['(°C)','(°F)','(K)','(°R)']
        y_datP=['(MPa)','(kPa)','(PSI)','(Bar)','(Atm)','(mmHg)'] 
        x_1_4=[]
        x_5_8=[]
        x_9_12=[]
        chosen_crt_chem=str((listfunc_crt.get(ANCHOR)))
        cmdlineq='SELECT DISTINCT * FROM'+' "Critical Constants"'+'WHERE '+'"Name"'+'='+'"'+str(chosen_crt_chem.split('[')[0]).strip()+'"'+' COLLATE NOCASE ORDER BY "Index_i" DESC LIMIT 1'
        print(cmdlineq)
        row=cur.fetchone()
        print(str(chosen_crt_chem))
        for i in range(len(y_dat1)):
            if(i<3):
                y_dat1[i]=y_dat1[i]+y_datT[T_unitselection]
            else:
                y_dat1[i]=y_dat1[i]+y_datP[P_unitselection]
            print(y_dat1[i])
        for row in cur.execute(cmdlineq):
            x_1_4.append(row[1])#Formula
            x_1_4.append(row[3])#CAS-NO
            x_1_4.append(row[4])#MW
            x_5_8.append(str(C_to_other(t_conversion(row[5],2),T_unitselection)))#Tf
            x_5_8.append(str(C_to_other(t_conversion(row[6],2),T_unitselection)))#Tb
            x_5_8.append(str(C_to_other(t_conversion(row[7],2),T_unitselection)))#Tc
            x_5_8.append(str(Mpa_to_other(p_conversion(row[8],3),P_unitselection)))#Pc
            print(x_5_8[3])
            x_9_12.append(row[9])#Vc
            x_9_12.append(row[10])#Rho
            x_9_12.append(row[11])#Zc
            x_9_12.append(row[12])#Omega
        out1=tabulate([x_1_4], headers=y_dat0)
        out2=tabulate([x_5_8], headers=y_dat1)
        out3=tabulate([x_9_12], headers=y_dat2)
        solution_crt.delete('1.0',END)
        print(out1)
        print(out2)
        print(out3)
        solution_crt.insert(INSERT,out1)
        solution_crt.insert(INSERT,'\n')
        solution_crt.insert(INSERT,'\n')
        solution_crt.insert(INSERT,out2)
        solution_crt.insert(INSERT,'\n')
        solution_crt.insert(INSERT,'\n')
        solution_crt.insert(INSERT,out3)
    def crt_chem_list_find(event):
        global crt_chem
        global find_type_crt
        find_type_crt=0
        new_list=[]
        list_item=option_crt.get()
        list_item=list_item.replace(" ",'-')
        listfunc_crt.delete('0','end')
        indices=[]
        part1=''
        part2=''
        if(list_item==''):
            crt_chem_list()
            listfunc_crt.delete('0','end')
            for items in range(len(crt_chem)):
                part1=str(list(crt_chem.keys())[items])
                part2=str(list(crt_chem.values())[items])
                listfunc_crt.insert(items, str(part1+' ['+part2+']'))
        else:
            for i,chem_name in enumerate(list(crt_chem.keys())):
                if list_item.lower() in chem_name:
                    indices.append(i)
            if(len(indices)==0):
                find_type_crt=1
                for i,chem_form in enumerate(list(crt_chem.values())):
                    if list_item == chem_form:
                        indices.append(i)
            if(find_type_crt==0):
                for i in indices:
                    part1=str(list(crt_chem.keys())[i])
                    part2=str(list(crt_chem.values())[i])
                    new_list.append(str(part1+' ['+part2+']'))
            elif(find_type_crt==1):
                for i in indices:
                    part1=str(list(crt_chem.keys())[i])
                    part2=str(list(crt_chem.values())[i])
                    new_list.append(str(part1+' ['+part2+']'))
            for items in range(len(new_list)):
                listfunc_crt.insert(items, new_list[items])
            print(list_item)
            print(len(new_list))
            print(len(list(crt_chem.keys())))
    
    listfunc_crt.bind('<<ListboxSelect>>',crt_chem_choosen)
    search_crt.bind('<Button-1>',crt_chem_list_find)
    option_crt.bind('<Key-Return>',crt_chem_list_find)
    #solve_ant_P_base.bind('<Button-1>',estimate_temperature_from_vapor_pressure)
    splash_root.destroy()
    window.deiconify()
    window.lift()
    window.attributes('-topmost',True)
    window.after_idle(window.attributes,'-topmost',False)
    window.mainloop()  


interface_user()

