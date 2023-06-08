import time
import requests
from bs4 import BeautifulSoup

# Ana sayfaya git ve modalı kapat
url = "https://acikveri.ysk.gov.tr/anasayfa"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

close_button = soup.find("button", {"id": "myModalClose"})
close_button

time.sleep(2)

# Seçim seçiniz butonuna tıkla
select_button = soup.find("button", text="Seçim seçiniz")
select_button.click()

time.sleep(2)

# Cumhurbaşkanlığı seçimi butonuna tıkla
presidential_button = soup.find("button", text="Cumhurbaşkanlığı seçimi")
presidential_button.click()

time.sleep(2)

# 27. dönem Milletvekili genel seçimi butonuna tıkla
general_election_button = soup.find("button", text="27.dönem Milletvekili genel seçimi(24 haziran 2018)")
general_election_button.click()

time.sleep(2)

# Election Results butonuna tıkla
election_results_button = soup.find("button", text="Election Results")
election_results_button.click()

time.sleep(2)

# İlleri gezerek JSON dosyalarını indirme
province_elements = soup.find_all("path")
for province in province_elements:
    province_id = province["data-il-id"]
    province_url = f"https://acikveri.ysk.gov.tr/secim-sonuc-istatistik/il/{province_id}"
    province_response = requests.get(province_url)
    province_soup = BeautifulSoup(province_response.content, "html.parser")

    json_button = province_soup.find("button", text="Download JSON")
    json_url = json_button["data-url"]
    json_response = requests.get(json_url)
    json_data = json_response.json()

    # JSON verilerini kullanarak istediğiniz işlemleri gerçekleştirin
    # ...

    time.sleep(2)  # İstediğiniz bekleme süresini ayarlayabilirsiniz