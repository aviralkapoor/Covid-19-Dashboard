from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


URL_1 = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'
URL_2 = 'https://www.mohfw.gov.in/'
page_1 = requests.get(URL_1)
page_2=requests.get(URL_2)

soup = BeautifulSoup(page_1.content, 'html.parser')
row=soup.find_all('tr')
bowl=BeautifulSoup(page_2.content,'html.parser')
states=bowl.find_all('tr')
data=[]
data_precise=[]
search_res=[]
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

def states_i(key):
    states_India=[]
    states_dummy=[]
    if key == 'India' or key == 'india':
        for s in range(1,33):
            std=states[s].find_all('td')
            for td in std:
                states_dummy.append(td.text.strip())
            states_India.append(states_dummy)
            states_dummy=[]
    return states_India

def number(data):
    encoded_data=[]
    for i in data:
        r=0
        for j in i:
            if j!=',' and i!='No data':
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


def line_chart():
    dummy_states=[]
    dummy_list=[]
    data=states_i('India')
    for i in data:
        dummy_states.append(i[1])
        dummy_list.append(i[2])
        dummy_list.append(i[4])
        dummy_list.append(i[3])
    dummy_list=number(dummy_list)
    dummy_list=active(dummy_list)
    dum={'0':dummy_states,'1':dummy_list}
    return dum


def pie_chart(data):
    p_ch=[]
    for j in data:
        for i in range(4,1,-1):
            p_ch.append(j[i])
    return number(p_ch)


active_cases=active(number(graph_d_label))

def index(req):
    search_res=[]
    for ele in data:
        if ele[1]=='India':
            search_res.append(ele)
            states_data=states_i('India')
            data_1=line_chart()
            for k,v in data_1.items():
                if k == '0':
                    d_s=v
                else:
                    d_a=v
                    
    p_c=pie_chart(search_res)
    return render(req,'Covid_Track/index.html',{'data':search_res,'p_c':p_c,'select':select,'tot_data':tot_data,'graph_label':select[:10],'active_cases':active_cases[:10],'states':states_data,'d_s':d_s,'d_a':d_a})

def search(req):
    key=req.POST["key"]
    search_res=[]
    for ele in data:
        if ele[1].lower()==key.lower():
            search_res.append(ele)
            data_1=line_chart()
            for k,v in data_1.items():
                if k == '0':
                    d_s=v
                else:
                    d_a=v

            break
    else:
        search_res.append(['No such Country found','No data','No data','No data'])
    states_data=states_i(key)
    p_c=pie_chart(search_res)
    return render(req,'Covid_Track/index.html',{'data':search_res,'p_c':p_c,'select':select,'tot_data':tot_data,'graph_label':select[:10],'active_cases':active_cases[:10],'states':states_data,'d_s':d_s,'d_a':d_a})
    
