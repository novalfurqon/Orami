from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

#opsi headless tanpa menampilkan browser saat running
opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

shopee_link = "https://www.orami.co.id/shopping/promo/belanja-di-bawah-20-ribu"
driver.set_window_size(1300,800)
driver.get(shopee_link)

#10x scroll page untuk get all data
rentang = 500
for i in range(1,21):
    akhir = rentang * i
    perintah = "window.scrollTo(0,"+str(akhir)+")"
    driver.execute_script(perintah)
    print("loading ke-"+str(i))
    time.sleep(1)

time.sleep(5)

driver.save_screenshot("home.png")
content = driver.page_source
driver.quit()

data = BeautifulSoup(content, 'html.parser')
#print(data.encode("utf-8"))

i = 1
base_url = "https://orami.co.id"

list_nama,list_gambar,list_harga,list_link=[],[],[],[]

for area in data.find_all('div',class_="px-8 pb-16"):
    print('proses data ke-'+str(i))
    nama = area.find('p',class_="product-title text-dark pt-12 non-loading").get_text()
    gambar = area.find('img')['src']
    harga = area.find('span',class_="original-price strikethrough text-charcoal align-center med-weight non-loading")
    if harga != None:
        harga = harga.get_text()
    link = base_url + area.find('a')['href']
   
    list_nama.append(nama)
    list_gambar.append(gambar)
    list_harga.append(harga)
    list_link.append(link)

    i+=1
    print("----------")

df = pd.DataFrame({'Nama':list_nama,'Gambar':list_gambar,'Harga':list_harga,'Link':list_link})
#save to .csv
df.to_csv("orami.csv",index=False)

