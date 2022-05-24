import  requests
from bs4 import BeautifulSoup
import json
def sports():
    content=requests.get("https://www.geo.tv/category/sports").content
    soup=BeautifulSoup(content,'lxml')
    lists=soup.find_all('div',class_='list')
    for list in lists:
        title=list.h2.text
        time=list.span.text
        pics=list.img.get('src')
        dict = {
            "title": title,
            "time": time,
            "pics": pics,
        }
        json_object = json.dumps(dict)
        with open("data.json", "w", encoding='iso-8859-1') as wfile:
            wfile.write(json_object)

        with open('data.json', 'r') as f:
            data = json.load(f)
        print(data)
        # print(title)
        # print(time)
        # print(pics)
def latest():
    url='https://www.geo.tv/latest-news'
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'lxml')
    lists = soup.find('div', class_='panel')
    title=lists.h4.text
    news=lists.ul
    print(title.strip())
    for new in news:
        n=new.text
        print(n.strip())

if __name__ == '__main__':
   sports()
   latest()