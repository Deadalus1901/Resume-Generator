from tika import parser
import re
import string
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
parsed=parser.from_file("Sample.pdf")
data=parsed['content']
data=data.lower()
a=data.find('years')
if data[a-3]==" ":
    exp=data[a-2]
else:
    exp=data[a-3]+data[a-2]
data=re.sub(r'\d+','',data)
data=data.translate(str.maketrans('','',string.punctuation))
data=data.replace('\xc2\xb7','')
data=data.replace('•','')
data= re.sub('[^a-zA-Z0-9 \n\.]', ' ', data)
exp=int(exp.replace('+',''))
terms = {'Quality':['interview','black belt','capability analysis','control charts','doe','dmaic','fishbone',
                              'gage r&r', 'green belt','ishikawa','iso','kaizen','kpi','lean','metrics',
                              'pdsa','performance improvement','process improvement','quality',
                              'quality circles','quality tools','root cause','six sigma',
                              'stability analysis','statistical analysis','tqm'],      
        'Operations management':['automation','bottleneck','constraints','cycle time','efficiency','fmea',
                                 'machinery','maintenance','manufacture','line balancing','oee','operations',
                                 'operations research','optimization','overall equipment effectiveness',
                                 'pfmea','process','process mapping','production','resources','safety',
                                 'stoppage','value stream mapping','utilization'],
        'Supply chain':['abc analysis','apics','customer','customs','delivery','distribution','eoq','epq',
                        'fleet','forecast','inventory','logistic','materials','outsourcing','procurement',
                        'reorder point','rout','safety stock','scheduling','shipping','stock','suppliers',
                        'third party logistics','transport','transportation','traffic','supply chain',
                        'vendor','warehouse','wip','work in progress'],
        'Project management':['administration','agile','budget','cost','direction','feasibility analysis',
                              'finance','kanban','leader','leadership','management','milestones','planning',
                              'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
        'Data analytics':['analytics','api','aws','big data','busines intelligence','clustering','code',
                          'coding','data','database','data mining','data science','deep learning','hadoop',
                          'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                          'predictive','programming','python','r','sql','tableau','text mining',
                          'visualuzation'],
        'Healthcare':['adverse events','care','clinic','cphq','ergonomics','healthcare',
                      'health care','health','hospital','human factors','medical','near misses',
                      'patient','reporting system']}
quality = 0
operations = 0
supplychain = 0
project = 0
dat=0
healthcare = 0
data=str(data)
# Obtain the scores for each area
for area in terms.keys():
        
    if area == 'Quality':
        for word in terms[area]:
            if word in data:
                quality +=1
    elif area == 'Operations management':
        for word in terms[area]:
            if word in data:
                operations +=1
    elif area == 'Supply chain':
        for word in terms[area]:
            if word in data:
                supplychain +=1
    elif area == 'Project management':
        for word in terms[area]:
            if word in data:
                project +=1
    elif area == 'Data analytics':
        for word in terms[area]:
            if word in data:
                dat +=1
    else:
        for word in terms[area]:
            if word in data:
                healthcare +=1
score={
   "Categories": ['Quality', 'Operations management', 'Supply Chain', 'Project Management', 'Data Analytics','Healthcare'],"Score": [quality, operations,supplychain,project,dat,healthcare]
}

df = pd.DataFrame(score)
df.set_index('Categories').plot.pie(y='Score', legend=False, autopct=lambda p: format(p, '.2f') if p > 40 else None)
plt.ylabel("")
plt.savefig('pie.png')
ev=('')
if exp>=10 and dat>=7:
    if operations>-7:
        ev+='Business Devolopment Manager'
    if project>=7:
        ev+='Senior Team Leader'
    if healthcare>=7:
        ev+='Biomedical Research Scientist'
if exp<10 and exp>5 and dat>=7:
    if operations>=5 and operations<7:
        ev+='Financial Risk Analst'
    if project>=5 and project<7:
        ev+='Senior Technical Lead'
    if healthcare>=3:
        ev+='Biotechnologist'
if exp>5 and dat>=3:
    if operations>=3:
        ev+='Business Advisor'
    if project>=3:
        ev+='Project Administrator'
       
    else:
        ev+='Financial Trader'
if exp>=2 and exp<5 and dat>=3:
    if operations>=1:
        ev+='Retail Manager'
    if project>=1:
        ev+='Campaign Assistant'
    else:
        ev+='Junior Coder'
if exp<1 and dat<1 and project<1:
    ev+='We are sorry to inform you that we can not recommend a job based on your resume at the moment.We would recommend you to check out our featured courses'
pdf = FPDF()
pdf.add_page()
pdf.set_fill_color(236,134,117)
pdf.set_font("Arial", size=28)
pdf.cell(200, 10, txt="Welcome to JobDirect", ln=1, align="C")
pdf.set_font("Arial",size=16)
pdf.cell(200, 10, txt="", ln=1, align="L")
pdf.cell(200, 10, txt="Here is our analysis for the submitted resume", ln=1, align="L")
pdf.image('pie.png',x=30,y=40,link='',type='')
pdf.set_y(150)
pdf.set_font("Arial",size=20)
pdf.cell(200, 10, txt="Our analysis recommends you:", ln=1, align="C")
pdf.cell(200, 10, txt=ev, ln=1, align="C")
pdf.output("python.pdf")    