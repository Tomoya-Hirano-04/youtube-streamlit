import requests
import urllib
import folium
import gspread
import pandas as pd
from folium import plugins
import branca
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import os
import geopandas as gpd

# 認証情報の取得
scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_file('keys.json', scopes=scope)

# スプレッドシートにアクセス
gClient = gspread.authorize(credentials)
SPREADSHEET_KEY = '1ikU-wKo7gldu6j1XfgcVrZo3zaEu09kiusc40fGYwk8'
file = gClient.open_by_key(SPREADSHEET_KEY)

#小学校
# シートにアクセス
sheet1 = file.worksheet('シート1')
sheet2 = file.worksheet('シート2')

# シート1のデータフレームを作成
data_sheet1 = sheet1.get_all_values()
df_sheet1 = pd.DataFrame(data_sheet1[1:], columns=data_sheet1[0])
#df_sheet1["URL1"] = df_sheet1["URL"].astype(str)

# シート2のデータフレームを作成
data_sheet2 = sheet2.get_all_values()
df_sheet2 = pd.DataFrame(data_sheet2[1:], columns=data_sheet2[0])

# シート1のデータフレームにシート2の2列目のデータを追加
df_sheet1[df_sheet2.columns[1]] = df_sheet2.iloc[:, 1]

# shapefileを取得
input_path = "shougakkou"
files = os.listdir(input_path)
shapefile = [file for file in files if ".shp" in file][0]
print(f"downloaded shapefile: {shapefile}")

# 読み込み
shapefile_path = os.path.join(input_path, shapefile)
df = gpd.read_file(shapefile_path, encoding='cp932')
print(f"{shapefile_path} is loaded")

#学校の緯度経度取得
latitude_list = [] 
longtude_list = []

name_list = df_sheet1["学校名"].tolist()  # 名前のリスト
evaluation_list = df_sheet1["評価"].tolist()  # 評価のリスト
class_list = df_sheet1["公私立"].tolist()  # 分類のリスト
separation_list = df_sheet1["共学別学"].tolist()  # 分離のリスト
URL_list = df_sheet1["URL"].tolist()  # URLのリスト
address_list = df_sheet1["所在地"].tolist()  # 住所のリスト

url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="

for i in range(len(df_sheet1)):
    q = df_sheet1["所在地"][i]
    res = requests.get(url + urllib.parse.quote(q))

    latitude_list.append(res.json()[0]["geometry"]["coordinates"][1]) 
    longtude_list.append(res.json()[0]["geometry"]["coordinates"][0])

#マップにプロット
map = folium.Map(location=[latitude_list[0],longtude_list[0]],zoom_start=15)
folium.GeoJson(df,style_function=lambda x: {'fillColor': 'white', 'color': 'red'}, ).add_to(map)

for i in range(len(df_sheet1)):
    popup_content = f"<div style='writing-mode: horizontal-tb; white-space: nowrap;'>"
    popup_content += f"{name_list[i]}<br>"
    popup_content += f"口コミ評価: {evaluation_list[i]}<br>"
    popup_content += f"国公私立: {class_list[i]}<br>"
    popup_content += f"共学別学: {separation_list[i]}<br>"
    popup_content += f'<a href={URL_list[i]} target="_blank">詳細</a>' #'<a href={URL_list[i]}>詳細</a>'
    popup_content += "</div>"
    
    iframe = branca.element.IFrame(html=popup_content, width=200, height=140)
    popup = folium.Popup(iframe, max_width=300)

    folium.Marker(location=[latitude_list[i], longtude_list[i]], popup=popup).add_to(map)

map