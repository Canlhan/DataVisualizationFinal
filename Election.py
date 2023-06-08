import shutil
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

class Election:
    def __init__(self):
        self.driver = self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": os.path.join(os.getcwd(), "json_files")
        })
        return webdriver.Chrome(options=chrome_options)

    def wait_and_click(self, by, selector):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, selector)))
        element.click()

    def wait_for_element(self, by, selector):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, selector)))

    def download_json_file(self):
        self.wait_and_click(By.XPATH, "//*[@id='kadinErkekOraniBar']/div[2]/div/button[2]")
        time.sleep(10)

    def extract_province_name(self):
        name_div = self.driver.find_element(By.XPATH, "//*[@id='kadinErkekOraniBar']/div[1]")
        name_city = name_div.find_element(By.XPATH, "//*[@id='kadinErkekOraniBar']/div[1]/h4")
        province_name = name_city.text
        return province_name

    def download_province_json(self, province_index):
        self.driver.get("https://acikveri.ysk.gov.tr/secim-sonuc-istatistik/secim-sonuc")
        time.sleep(3)
        map_element = self.driver.find_element(By.ID, "map")
        svg = map_element.find_element(By.CLASS_NAME, "country-svg")
        time.sleep(2)
        province_elements = svg.find_elements(By.TAG_NAME, "path")
        time.sleep(2)
        ActionChains(self.driver).move_to_element(province_elements[province_index]).click().perform()
        time.sleep(2)
        province_name = self.extract_province_name()
        file_name = f"{province_name}.json".lower()
        self.download_json_file()
        time.sleep(5)
        source_file = os.getcwd()+"\\json_files\\SecimSonucIlce.json"
        target_file = os.path.join(os.getcwd(), "json_files", file_name)
        if os.path.exists(source_file):
            try:
                with open(source_file, 'r', encoding='utf-8') as src, open(target_file, 'w', encoding='utf-8') as dst:
                    shutil.copyfileobj(src, dst)
                os.remove(source_file)
                print("Dosya içeriği başarıyla aktarıldı ve kaynak dosya silindi.")
            except OSError as e:
                print(f"Hata: Kaynak dosya silinirken bir hata oluştu: {e}")
        else:
            print("Kaynak dosya bulunamadı.")

    def run(self):
        self.driver.get("https://acikveri.ysk.gov.tr/anasayfa")
        close_button = self.wait_for_element(By.ID, "myModalClose")
        close_button.click()
        time.sleep(3)
        select_election_button = self.driver.find_element(By.XPATH, "//*[@id='navbarDropdown']")
        select_election_button.click()
        time.sleep(3)
        presidential_election_button = self.driver.find_element(By.XPATH, "//*[@id='heading6']/h5/a")
        presidential_election_button.click()
        time.sleep(3)
        election_2018_button = self.driver.find_elements(By.XPATH, "//*[@id='collapse6']/div/div")
        election_2018_button[2].click()
        time.sleep(5)
        results_button = self.wait_for_element(By.XPATH, "//*[@id='accordionSidebar']/li[8]/a")
        results_button.click()
        time.sleep(3)
        self.download_json_file()

        svg = self.driver.find_element(By.CLASS_NAME, "country-svg")
        province_elements = svg.find_elements(By.TAG_NAME, "path")
        print(len(province_elements))

        os.makedirs("json_files", exist_ok=True)
        for index, province in enumerate(province_elements):
            print(index)
            try:
                self.download_province_json(index)
            except Exception as e:
                print(f"Hata: {e}")
                continue

        self.driver.quit()


