# needed libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np

STAT=pd.DataFrame(columns=['Team_H','Team_A','HomeWin',
                            'MP_H','FG_H','FGA_H','FG%_H','3P_H','3PA_H','3P%_H','FT_H','FTA_H','FT%_H','ORB_H','DRB_H','TRB_H','AST_H','STL_H','BLK_H','TOV_H','PF_H','PTS_H',
                           'MP_A','FG_A','FGA_A','FG%_A','3P_A','3PA_A','3P%_A','FT_A','FTA_A','FT%_A','ORB_A','DRB_A','TRB_A','AST_A','STL_A','BLK_A','TOV_A','PF_A','PTS_A'])

basic_url="https://www.basketball-reference.com"
date_url="https://www.basketball-reference.com/boxscores/?month=5&day=16&year=2021"

while (STAT.shape[0]<=1230):
  urls=[]
  response = requests.get(date_url)
  soup=BeautifulSoup(response.text,"html.parser")

  for suburl in soup.find_all("td",{"class":"right gamelink"}):
    urls.append(basic_url+suburl.find("a").get('href'))

  for j in range(len(urls)):
    response_temp=requests.get(urls[j])
    print(urls[j])
    soup_temp=BeautifulSoup(response_temp.text, 'html.parser')

    soup_strong=soup_temp.find_all("strong")
    for k in range(len(soup_strong)):
      if(len(soup_strong[k].get_text())==3):
        home_team=soup_strong[k].get_text()
        away_team=soup_strong[k+1].get_text()
        break;
    
    score_list=soup_temp.find_all("div",{"class":"score"})
    score=[]
    for eachscore in score_list:
      score.append(eachscore.get_text())
    if score[0]>score[1]:
      homewin="1"
    else:
      homewin="0"

    class1=soup_temp.select('div#div_box-'+home_team+'-h1-basic table#box-'+home_team+'-h1-basic tfoot td')
    class2=soup_temp.select('div#div_box-'+away_team+'-h1-basic table#box-'+away_team+'-h1-basic tfoot td')
    df=[]
    df.append(home_team)
    df.append(away_team)
    df.append(homewin)

    for i in range(len(class1)-1):
      df.append(class1[i].get_text())
    for i in range(len(class2)-1):
      df.append(class2[i].get_text())

    STAT.loc[STAT.shape[0]]=df
    num=np.random.rand(1)[0]*5
    time.sleep(num)
    print(STAT.shape[0])
  prev_url=soup.find("div",{"class":"prevnext"}).find("a").get('href')
  date_url=basic_url+prev_url

STAT.head(10)
STAT.tail(10)
