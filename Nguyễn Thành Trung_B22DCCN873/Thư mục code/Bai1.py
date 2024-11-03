import requests,random
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
for _ in user_agent_list:
  user_agent = random.choice(user_agent_list)
  headers = {'User-Agent': user_agent}
session = requests.Session()
r = requests.get("https://fbref.com/en/",headers)
print("Bắt đầu crawl dữ liệu")
soup = bs(r.content, 'html.parser')
resultTable = soup.select('table')[0]
links = resultTable.find_all('a')
links = [l.get('href') for l in links]
links = [l for l in links if '/squads/' in l]
team_urls = [f"https://fbref.com/{l}" for l in links]
all_dataFrame=[]
for i in team_urls:
    team_url = i
    # lấy tên của đội bóng
    teamName= team_url.split("/")[-1].replace("-Stats","").replace("-"," ")
    print(f"Đang crawl dữ liệu team {teamName}")
    r=requests.get(team_url)
    soup = bs(r.content, 'html.parser')
    #link đội bóng  mùa 2023-2024
    previousSeasonUrl ="https://fbref.com/"+soup.find('div',attrs={'id':'meta'}).find('a').get('href')
    r=requests.get(previousSeasonUrl)
    soup = bs(r.content,'html.parser')
    table_teams=soup.find_all('table')
    all_table=[]
    #xử lý các bảng
    for table in table_teams:
        cols=[]
        cols.append(['Info','Team'])
        tableId=table.get("id")
      
        if tableId == "matchlogs_for" or ("stats_keeper_adv" in tableId) or ("results" in tableId):
            continue
        #xử lý col
        theads = table.find("thead").find_all("tr")[1].find_all('th')
        for col in theads:
          if col.get('data-over-header') is None:
            if col.text=="Player" or col.text=="Nation" or col.text=="Pos" or col.text=="Age" :
              cols.append(['Info',col.text])
            elif col.text=="MP":
              cols.append(['Playing Time',col.text])
            else:
              cols.append(['',col.text])
          else:
            cols.append([col.get('data-over-header'),col.text])
        #xử lý phần body
        dataTbody=[]
        tbody = table.find("tbody").find_all("tr")
        for row in tbody:
          if row.get("class")=="over_header thead" or row.get("class")=="thead":
            continue
          data=[]
          data.append(teamName)
          namePlayer = row.find('th').text
          data.append(namePlayer)
          tds = row.find_all('td')
          for td in tds:
            data.append(td.text)
          dataTbody.append(data)
        #tạo cột 
        cols = pd.MultiIndex.from_tuples(cols)
        #tạo dataFrame
        dataFrame=pd.DataFrame(dataTbody,columns=cols)
        #xóa bỏ các cột không cần thiết của tất cả các bảng
        columns_to_drop = [('','Matches'),('Playing Time','90s')]
        dataFrame.drop(columns=[col for col in columns_to_drop if col in dataFrame.columns], inplace=True)
        all_table.append(dataFrame)
    df = all_table[0]
    all_table[9].drop(columns=[('Performance','CrdY'),('Performance','CrdR'),('Performance','2CrdY'),('Performance','Int'),('Performance','TklW'),('Performance','PKwon'),('Performance','PKcon')], inplace=True)
    #xóa bỏ các cột không cần thiết của bảng đầu
    df.drop(columns=[('Performance','Gls'),('Performance','PKatt'),('Performance','G+A'),('Expected','npxG+xAG')], inplace=True)
    for i in all_table[1:]:
      #hợp các bảng lại với nhau
      df=pd.merge(df,i,how="outer")
    #lọc ra các cầu thủ có hơn 90 phút thi đấu  
    df[('Playing Time', 'Min')] = pd.to_numeric(df[('Playing Time', 'Min')].str.replace(',', ''), errors='coerce')
    df=df[df[('Playing Time',"Min")]>90]  
    #sắp xếp các cầu thủ theo điều kiện
    #dừng 5s trước khi crawl tiếp
    all_dataFrame.append(df)
    print(f"Đã crawl xong team {teamName},chờ 10s để crawl team tiếp theo")
    time.sleep(10)
all_result=pd.concat(all_dataFrame,ignore_index=True)
all_result = all_result.sort_values(by=[('Info','Player'), ('Info','Age')], ascending=[True, False])
#cột nào mà rỗng thì sẽ thay thế bằng giá trị N/A
all_result.fillna('N/A', inplace=True)
all_result.to_csv('result.csv',index=False)
print("Đã crawl data xong !")
