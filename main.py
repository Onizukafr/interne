import pandas as pd
import streamlit as st
import os

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     st.write(bytes_data)

     # To convert to a string based IO:
     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
     st.write(stringio)

     # To read file as string:
     string_data = stringio.read()
     st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
     dataframe = pd.read_xlsx(uploaded_file)
     st.write(dataframe)

list_keywords = pd.read_excel(uploaded_file) 
list_keywords = list_keywords.values.tolist()

list_urls = []
for x in list_keywords:
    list_urls.append(x[6])
 
list_urls = list(dict.fromkeys(list_urls))

list_keyword_url = []
for x in list_keywords:
    list_keyword_url.append([x[6],x[0],x[1]])
    
import requests
from bs4 import BeautifulSoup
import pandas as pd
 
absolute_rute = str(input("URL (avec https): "))
internal_linking_opportunities = []
for iteration in list_urls:
 
    page = requests.get(iteration)
    print(iteration)
    soup = BeautifulSoup(page.text, 'html.parser')
    paragraphs = soup.find_all('p')
    paragraphs = [x.text for x in paragraphs]
    
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
 
    
    for x in list_keyword_url:
        for y in paragraphs:
            if " " + x[1].lower() + " " in " " + y.lower().replace(",","").replace(".","").replace(";","").replace("?","").replace("!","") + " " and iteration != x[0]:
                links_presence = False
                for z in links:
                    try:
                        if x[0].replace(absolute_rute,"") == z.replace(absolute_rute,""):
                            links_presence = True
                    except AttributeError:
                        pass
                        
                
                if links_presence == False:
                    internal_linking_opportunities.append([x[1],y,iteration,x[0], "False", x[2]])
                else:
                    internal_linking_opportunities.append([x[1],y,iteration,x[0], "True", x[2]])
 
 
pd.DataFrame(internal_linking_opportunities, columns = ["Mot clé", "Phrase contenant le mot clé", "Source URL", "URL Cible", "Maillage interne existant dans la page source ?", "Position du mot clé"]).to_excel('Maillage-interne.xlsx', header=True, index=False)
