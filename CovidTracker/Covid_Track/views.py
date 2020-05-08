from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


URL = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
data=[]
data_precise=[]
search_res=[]
select=[]
tot_data=[]
graph_d_label=[]
row=soup.find_all('tr')
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
    p_c=pie_chart(search_res)
    print(p_c)
    return render(req,'Covid_Track/index.html',{'data':search_res,'p_c':p_c,'select':select,'tot_data':tot_data,'graph_label':select[:10],'active_cases':active_cases[:10]})

def search(req):
    key=req.POST["key"]
    search_res=[]
    for ele in data:
        if ele[1].lower()==key.lower():
            search_res.append(ele)
            break
    else:
        search_res.append(['No such Country found','No data','No data','No data'])
    p_c=pie_chart(search_res)
    return render(req,'Covid_Track/index.html',{'data':search_res,'p_c':p_c,'select':select,'tot_data':tot_data,'graph_label':select[:10],'active_cases':active_cases[:10]})
    
