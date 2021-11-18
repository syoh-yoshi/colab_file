%matplotlib inline
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import MeCab
import collections
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS

# gain html source

def gain_html_source():
  articles = []

  for i in range(100):
    html = urllib.request.urlopen("https://voice-action.net/view-voice.html?page={:d}".format(i+1))
    soup = BeautifulSoup(html)
    soup_voice = soup.find_all("a", class_="media01_ballon")

    for tag in soup_voice:
      text = tag.span.text

      articles.append(text)

  articles_list = list(set(articles))
  df_voice = pd.DataFrame(articles_list)

  return(df_voice)

#Morphological analysis by MeCab 


def morphological_analysis(df_voice):

  need_list = []
  # new_need_data = []

  for i in range(len(df_voice)):
    text = df_voice.at[i, 0]
    node = mecab.parseToNode(text)

    while node:
      if node.feature.split(",")[0]=="名詞":
        if node.feature.split(",")[1]=="一般":  
          need_list.append(node.surface)
        elif node.feature.split(",")[1]=="サ変接続":
          need_list.append(node.surface)
        elif node.feature.split(",")[1]=="副詞可能":
          need_list.append(node.surface)
        elif node.feature.split(",")[1]=="数":
          need_list.append(node.surface)
        elif node.feature.split(",")[1]=="形容動詞語幹":
          need_list.append(node.surface)
        elif node.feature.split(",")[1]=="固有名詞":
          need_list.append(node.surface)
        else:
          pass

      elif node.feature.split(",")[0]=="形容詞":
        if node.feature.split(",")[1]=="自立":
          need_list.append(node.surface)
          #print(node.surface)
        else:
          pass

      elif node.feature.split(",")[0]=="感動詞":
        if node.feature.split(",")[1]=="自立":
          need_list.append(node.surface)
          print(node.surface)
        else:
          pass
  
      else:
        pass
      node = node.next

  return(need_list)

def create_wordcloud(text, mask=None):

    # 環境に合わせてフォントのパスを指定する。
    #fpath = "/System/Library/Fonts/HelveticaNeue-UltraLight.otf"
    fpath = "フォントが保存されているパズを指定。"

    # ストップワードの設定
    for word in ['消去したいワードをこのリスト内にいれる']:
      STOPWORDS.add(word)

    
    wordcloud = WordCloud(background_color="white" ,font_path=fpath, mask=mask
                          ,width=900, 
                          #min_font_size=30, \
                          height=500, max_words=200).generate(text)
    
    plt.figure(figsize=(15,12))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

html_source = gain_html_source()
need_words = morphological_analysis(html_source)
linetext = ""
for token in need_words:
#for token in new_need_data:
  linetext += token
  linetext += " "
create_wordcloud("".join(linetext), mask=None)
