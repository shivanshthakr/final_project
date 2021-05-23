#for testing only no use in app
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
googlenews=GoogleNews()
googlenews.search('Covid')
result=googlenews.result()
df=pd.DataFrame(result)

list=[]
for ind in df.index:
    dict={}
    article = Article(df['link'][ind])
    article.download()
    article.parse()
    article.nlp()
    dict['Date']=df['date'][ind]
    dict['Media']=df['media'][ind]
    dict['Title']=article.title
    dict['Article']=article.text
    dict['Summary']=article.summary
    list.append(dict)
print(len(list))
print(list[0]['Title'])

