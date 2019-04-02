# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 13:02:09 2019

@author: Abhishek
"""

import numpy
import requests
import bs4
import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer 
ps=PorterStemmer()
from sklearn.feature_extraction.text import CountVectorizer



req=requests.get('https://www.imdb.com/chart/top')
soup=bs4.BeautifulSoup(req.text, 'lxml')
movie_ids=[]
for a in soup.find_all('div',class_="wlb_ribbon"):
    movie_ids.append(a['data-tconst'])
potty=0
plot=[]
names=[]
ratings=[]
years=[]
grosss=[]
budget=[]
languages=[]
countrys=[]
runtimes=[]
substring1="Country:"
substring2="Language:"
substring3="(estimated)"
substring4="Worldwide"
substring5="Runtime:"


  for tatti in movie_ids:
      add='https://www.imdb.com/title/'
      ress='/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=5S3VRBK9SR5FK1JRNESC&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_'
      url = add + tatti + ress+"potty"
      r = requests.get(url)
      soup = BeautifulSoup(r.content, "lxml")
      x=soup.find('div', class_="inline canwrap")
      plot.append(x.span.get_text())
      potty=potty+1           
      
      s=soup.find("div", class_="title_wrapper")
        
      year=s.span.text
      year=clean_year(year)
        
      name=s.h1.text
        
      s=soup.find("div",class_="ratingValue")
      rating=s.strong.text
      
      s=soup.find("div",class_="article",id="titleDetails")
      ss=s.findAll("div",{"class":"txt-block"})
        
      for tt in range(len(ss)):
          ss[tt] = clean(ss[tt].text)
          
          
      for to in range(len(ss)):
          for word in ss[to].split():
              if substring2 == word:
                    lag=ss[to]
                    lag=clean(lag)
              elif substring1 == word:
                    con=ss[to]
                    con=clean(con)
              elif substring3 == word:
                    box=ss[to]
                    box=clean_gross(box)    
              elif substring4== word:
                    tbox=ss[to]
                    tbox=clean_gross(tbox)    
              elif substring5 == word:
                    rt=ss[to]
                    rt=clean_duration(rt)   
                    
      grosss.append(tbox)
      budget.append(box)
      runtimes.append(rt)
      languages.append(lag)
      countrys.append(con)
      names.append(name)
      years.append(year)
      ratings.append(rating)           
            

    
 
data_frame = pd.DataFrame({
    "Name": names,
    "Plot": corpus,
    "Year": years,
    "Duration": runtimes,
    "Rating": ratings,
    "Budget": budget,
    "Country": countrys,
    "Gross": grosss,
    "Language": languages
})

data_frame.to_csv("datamovie.csv", index=False)
print("All data successfully added") 




  
  


corpus=[]
for i in range (0,250):
    fplot=re.sub('[^a-zA-Z]', ' ', plot[i])
    fplot= fplot.lower()
    fplot=fplot.split()
            
    fplot=[(word) for word in fplot if not word in set(stopwords.words('english'))]
    fplot= ' '.join(fplot)
    corpus.append(fplot)










cv=CountVectorizer(max_features =10)
X=cv.fit_transform(corpus).toarray()

print(cv.get_feature_names())

X
