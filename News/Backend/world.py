from technology import *

def storedata(soup):
    for data in soup.findAll("div", {"class": "news-card z-depth-1"}):
        if data.find(itemprop="headline").getText() not in dict["headlines"]:
            dict["headlines"].append(data.find(itemprop="headline").getText())
            dict["date"].append(data.find("span", {"clas": "date"}).getText())
            dict["time"].append(data.find("span", {"class": "time"}).getText())
            dict["author"].append(data.find("span", {"class": "author"}).getText())
            if data.find("a", {"class": "source"}):
                dict["read_more"].append(data.find("a", {"class": "source"}).get("href"))
            else:
                dict["read_more"].append(None)
            img = data.find("div", {"class": "news-card-image"})
            if img:
                img_src = img.get("style")
                img_url = urljoin(url, img_src.split("(")[-1].split(")")[0])
                dict["image_url"].append(img_url)
            else:
                dict["image_url"].append(None)

url = "https://inshorts.com/en/read/world"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "referer": "https://inshorts.com/en/read/world",
    "origin": "https://inshorts.com",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, "lxml")
dict = {"headlines": [], "date": [], "time":[] , "author": [], "read_more": [], "image_url": []}
storedata(soup)

#Start Ajaxing
start_id=soup.findAll("script",{"type":"text/javascript"})[-1].getText().split()[3].strip(";").strip('"')
for i in range(10):
    # print(i,len(dict["headlines"]),start_id)
    ajax_url="https://inshorts.com/en/ajax/more_news"
    # payload={"news_offset":start_id,"category":""}
    payload = {
    "category": "world",
    "news_offset": start_id,
    "vert": "world"}
    # print(payload)
    try:
        r=requests.post(ajax_url,payload,headers=headers)
        start_id=r.content.decode("utf-8")[16:26]
        soup=BeautifulSoup(r.text.replace('\\',""),"lxml")
        storedata(soup)
    except:
        pass
    if i%10==0:
        df = pd.DataFrame(dict)
        df = df.dropna()
        df.to_csv(path,encoding="utf-8", index=False)
        dict = {"headlines": [], "date": [], "time":[] , "author": [], "read_more": [], "image_url": []}
    else:
        df = pd.DataFrame(dict)
        df = df.dropna()
        df.to_csv(path,encoding="utf-8", index=False)

d=pd.read_csv(path,encoding="utf-8")
os.remove(path)
d.drop_duplicates(subset=["headlines"],inplace=True)
d.reset_index(drop=True)

d["ctext"]=[None for i in range(len(d["headlines"]))]

count=0
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }

for i,head in enumerate(d["headlines"]):
    # print(i)
    if d["read_more"][i]:
        if len(d["read_more"][i].split("/"))>2:
            link=d["read_more"][i].split("/")[2]
            try:
                r=requests.get(d["read_more"][i],headers=headers)
            except:
                time.sleep(10)
            if i%300==0:
                time.sleep(10)
            if link=="www.hindustantimes.com":
                soup=BeautifulSoup(r.content,"lxml")
                try:
                    txt=soup.find("div",{"class":"detail"}).getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="www.thenewsminute.com":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("div",{"class":"field-item"})
                txt=""
                try:
                    for s in soup.find("div",{"class":"field-item"}).findAll("p"):
                        txt=txt+s.getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="www.reuters.com":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("div",{"class":"paywall-article"})
                txt=""
                try:
                    for s in soup.find("div",{"class":"paywall-article"}).findAll("p"):
                        txt=txt+s.getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="www.aninews.in":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("div",{"itemprop":"articleBody"})
                txt=""
                class_pattern = re.compile(r"jsx-\d+")
                try:
                    for s in soup.find("div",{"itemprop":"articleBody"}).findAll("p"):
                        txt=txt+s.getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="theprint.in":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("div",{"class":"td-post-content"})
                txt=""
                class_pattern = re.compile(r"jsx-\d+")
                try:
                    for s in soup.find("div",{"class":"td-post-content"}).findAll("p"):
                        txt=txt+s.getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="www.news18.com":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("div",{"class":"article_outer"})
                txt=""
                class_pattern = re.compile(r"jsx-\d+")
                try:
                    for s in soup.find("div",{"class":"article_contentWrap"}).findAll("p"):
                        txt=txt+s.getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="www.independent.co.uk":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("div",{"id":"main"})
                txt=""
                class_pattern = re.compile(r"jsx-\d+")
                try:
                    for s in soup.find("div",{"id":"main"}).findAll("p"):
                        txt=txt+s.getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="www.timesnownews.com":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("div",{"class":"article-paragraph"})
                txt=""
                try:
                    for s in soup.find("div",{"class":"article-paragraph"}):
                        txt=txt+s.text.strip()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
print("world",count)


d['image_url'] = d['image_url'].str.replace("https://inshorts.com/en/read/'", '', regex=True)
d['image_url'] = d['image_url'].str.replace("'", '', regex=True)

d = d.dropna()
d = d.reset_index(drop=True)
d.to_csv('Static/output_worl.csv',encoding="utf-8")
