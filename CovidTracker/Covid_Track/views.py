from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


URL_1 = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'
URL_2 = 'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India'


def execute(row):
    data=[]
    data_precise=[]
    select=[]
    tot_data=[]
    graph_d_label=[]
    for i in range(1,231):
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
            ths=row[i].find_all('th')
            for th in ths:
                tot_data.append(th.text.strip())
    return data,tot_data,select,graph_d_label


def fetch():
    page_1 = requests.get(URL_1)
    page_2=requests.get(URL_2)
    soup = BeautifulSoup(page_1.content, 'html.parser')
    row=soup.find_all('tr')
    bowl=BeautifulSoup(page_2.content,'html.parser')
    states=bowl.find('table',["sortable", "mw-collapsible", "jquery-tablesorter", "mw-made-collapsible"])
    states=states.find('tbody')
    states=states.find_all('tr')[2:]
    data,tot_data,select,graph_d_label=execute(row)
    return states,data,tot_data,select,graph_d_label
    

def number(data):
    encoded_data=[]
    for i in data:
        r=0
        for j in i:
            if j!=',' and i!='No data' and j!='[' and j!=']' and j!='a' and j!='b':
                r=(r*10)+int(j)
        if i=='No data':
            r=0
        encoded_data.append(r)
    return encoded_data

def active(data):
    active_cases=[]
    for i in range(0,len(data),3):
        r=data[i]-data[i+2]
        active_cases.append(r)
    return active_cases

def states_i(states,key):
    states_India=[]
    states_dummy=[]
    states_dummy_1=[]
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
    return states_India


def line_chart(states):
    dummy_states=[]
    dummy_list=[]
    data=states_i(states,'India')
    for i in data:
        dummy_states.append(i[1])
        dummy_list.append(i[5])
    dum={'0':dummy_states,'1':dummy_list}
    return dum


def pie_chart(data):
    p_ch=[]
    for j in data:
        for i in range(4,1,-1):
            p_ch.append(j[i])
    return number(p_ch)



def index(req):
    search_res=[]
    states,data,tot_data,select,graph_d_label=fetch()
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
    return render(req,'Covid_Track/index.html',{'data':search_res,'p_c':p_c,'select':select,'tot_data':tot_data,'graph_label':select[:20],'active_cases':active_cases[:20],'states':states_data,'d_s':d_s,'d_a':d_a})

def search(req):
    key=req.POST["key"]
    search_res=[]
    states,data,tot_data,select,graph_d_label=fetch()
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
    return render(req,'Covid_Track/index.html',{'data':search_res,'p_c':p_c,'select':select,'tot_data':tot_data,'graph_label':select[:20],'active_cases':active_cases[:20],'states':states_data,'d_s':d_s,'d_a':d_a})
    
