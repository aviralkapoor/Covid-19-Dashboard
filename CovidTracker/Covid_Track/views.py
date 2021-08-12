from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time
#import threading

URL_1 = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'
URL_2 = 'https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_India'
URL_3 = 'https://en.wikipedia.org/wiki/Deployment_of_COVID-19_vaccines'

states=[]
data=[]
tot_data=[]
select=[]
graph_d_label=[]
t=''
inc=''
new=[]
tot_vacc=[]

def execute(row):
    data=[]
    data_precise=[]
    select=[]
    tot_data=[]
    graph_d_label=[]
    for i in range(1,245):
        if i!=1:
            ths=row[i].find_all('th')
            temp=ths[0].find('img')
            data_precise.append(temp['src'])
            temp=ths[1].find('a')
            select.append(temp.text.strip())
            data_precise.append(temp.text.strip())
            tds=row[i].find_all('td')
            for j in range(0,3):
                data_precise.append(tds[j].text.strip())
                graph_d_label.append(tds[j].text.strip())
            data.append(data_precise)
            data_precise=[]
        else:
            ths=row[i].find_all('th')[1:]
            for th in ths:
                tot_data.append(th.text.strip())
    #print(graph_d_label)
    return data,tot_data,select,graph_d_label

def up_time():
    sec=time.time()
    local_time=time.ctime(sec)
    return local_time

def process(vaccine):
    temp=[]
    res=[]
    tot_vacc=[]
    for i in range(0,214):
        j=vaccine[i].find_all('td')
        j=j[1:]
        temp.append(j[0].find('a').text.strip())
        j=j[1:]
        for td in j:
            temp.append(td.text.strip())
        if(i!=0):
            res.append(temp)
        else:
            tot_vacc.extend(temp)
        temp=[]
    return res,tot_vacc

def merge(a,b):
    for i in a:
        for j in b:
            if(i[1].lower()==j[0].lower()):
                i.append(j[1])
                i.append(j[2])
                break
        else:
            i.append('No Data')
            i.append('No Data')
    return a

def fetch():
    global new
    page_1 = requests.get(URL_1)
    page_2=requests.get(URL_2)
    page_3=requests.get(URL_3)
    #Page 1
    soup = BeautifulSoup(page_1.content,'html.parser')
    row=soup.find('table',id="thetable")
    row=row.find('tbody')
    row=row.find_all('tr')
    #print(row)
    #Page 2
    bowl=BeautifulSoup(page_2.content,'html.parser')
    bowl=bowl.find('div',id='covid19-container')
    states=bowl.find('table')
    states=states.find('tbody')
    states=states.find_all('tr')[3:]
    #print(states)
    #Page 3
    spoon=BeautifulSoup(page_3.content,'html.parser')
    spoon=spoon.find('div',id='covid19-container')
    vaccine=spoon.find('table')
    vaccine=vaccine.find('tbody')
    vaccine=vaccine.find_all('tr')[1:]
    #print(vaccine)
    data,tot_data,select,graph_d_label=execute(row)
    vacc_data,tot_vacc=process(vaccine)
    data=merge(data,vacc_data)
    time=up_time()
    return states,data,tot_data,tot_vacc,select,graph_d_label,time,inc
    

def number(data):
    encoded_data=[]
    for i in data:
        r=0
        for j in i:
            if j!=',' and i!='No data' and j!='[' and j!=']' and j!='a' and j!='b' and j!='c' and j!='+':
                r=(r*10)+int(j)
        encoded_data.append(r)
    return encoded_data

def active(data):
    active_cases=[]
    for i in range(0,len(data),3):
        r=data[i]-data[i+1]-data[i+2]
        active_cases.append(r)
    return active_cases

def states_i(states,key):
    global inc
    states_India=[]
    states_dummy=[]
    states_dummy_1=[]
    inc=''
    if key == 'India' or key == 'india':
        for s in range(0,36):
            sth=states[s].find_all('th')
            for th in sth:
                states_dummy.append(th.text.strip())
            std=states[s].find_all('td')
            for td in std:
                states_dummy_1.append(td.text.strip())
            states_dummy_1=number(states_dummy_1)
            states_dummy.extend(states_dummy_1)
            states_India.append(states_dummy)
            states_dummy=[]
            states_dummy_1=[]
        #r=new.find_all('tr')[-5]
        #inc=r.find_all('td')[35].text.strip()
        #print(states_India)
    return states_India


def line_chart(states):
    dummy_states=[]
    dummy_list=[]
    data=states_i(states,'India')
    for i in data:
        dummy_states.append(i[0])
        dummy_list.append(i[4])
    dum={'0':dummy_states,'1':dummy_list}
    return dum


def pie_chart(data):
    p_ch=[]
    for j in data:
        for i in range(4,1,-1):
            p_ch.append(j[i])
    return number(p_ch)


def update():
    global states
    global data
    global tot_data
    global select
    global graph_d_label
    global t
    global inc
    global tot_vacc
    states,data,tot_data,tot_vacc,select,graph_d_label,t,inc=fetch()
    #t1=threading.Timer(43200.0,update)
    #t1.start()


update()

def index(req):
    search_res=[]
    for ele in data:
        if ele[1]=='India':
            search_res.append(ele)
            states_data=states_i(states,'India')
            data_1=line_chart(states)
            for k,v in data_1.items():
                if k == '0':
                    d_s=v
                else:
                    d_a=v
    p_c=pie_chart(search_res)
    active_cases=active(number(graph_d_label))
    return render(req,'Covid_Track/index.html',{'data':search_res,'p_c':p_c,'select':select,'tot_data':tot_data,'tot_vacc':tot_vacc,'graph_label':select[:20],'active_cases':active_cases[:20],'states':states_data,'d_s':d_s,'d_a':d_a,'time':t,'inc':inc})

def search(req):
    key=req.POST["key"]
    search_res=[]
    for ele in data:
        if ele[1].lower()==key.lower():
            search_res.append(ele)
            data_1=line_chart(states)
            for k,v in data_1.items():
                if k == '0':
                    d_s=v
                else:
                    d_a=v

            break
    else:
        search_res.append(['No such Country found','No data','No data','No data'])
    states_data=states_i(states,key)
    active_cases=active(number(graph_d_label))
    p_c=pie_chart(search_res)
    return render(req,'Covid_Track/index.html',{'data':search_res,'p_c':p_c,'select':select,'tot_data':tot_data,'tot_vacc':tot_vacc,'graph_label':select[:20],'active_cases':active_cases[:20],'states':states_data,'d_s':d_s,'d_a':d_a,'time':t,'inc':inc})
    
