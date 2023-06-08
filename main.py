# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Election import Election
import os
import json
import string
from flask import Flask, render_template, request, jsonify
import threading
app = Flask(__name__)

sehirler_dict = {
    1: "Adana", 2: "Adiyaman", 3: "Afyonkarahisar", 4: "Ağri", 5: "Amasya",
    6: "Ankara", 7: "Antalya", 8: "Artvin", 9: "Aydin", 10: "Balikesir",
    11: "Bilecik", 12: "Bingöl", 13: "Bitlis", 14: "Bolu", 15: "Burdur",
    16: "Bursa", 17: "Çanakkale", 18: "Çankiri", 19: "Çorum", 20: "Denizli",
    21: "Diyarbakir", 22: "Edirne", 23: "Elaziğ", 24: "Erzincan", 25: "Erzurum",
    26: "Eskişehir", 27: "Gaziantep", 28: "Giresun", 29: "Gümüşhane", 30: "Hakkâri",
    31: "Hatay", 32: "isparta", 33: "Mersin", 34: "istanbul", 35: "izmir",
    36: "Kars", 37: "Kastamonu", 38: "Kayseri", 39: "Kirklareli", 40: "Kirşehir",
    41: "Kocaeli", 42: "Konya", 43: "Kütahya", 44: "Malatya", 45: "Manisa",
    46: "Kahramanmaraş", 47: "Mardin", 48: "Muğla", 49: "Muş", 50: "Nevşehir",
    51: "Niğde", 52: "Ordu", 53: "Rize", 54: "Sakarya", 55: "Samsun",
    56: "Siirt", 57: "Sinop", 58: "Sivas", 59: "Tekirdağ", 60: "Tokat",
    61: "Trabzon", 62: "Tunceli", 63: "Şanliurfa", 64: "Uşak", 65: "Van",
    66: "Yozgat", 67: "Zonguldak", 68: "Aksaray", 69: "Bayburt", 70: "Karaman",
    71: "Kirikkale", 72: "Batman", 73: "Şirnak", 74: "Bartin", 75: "Ardahan",
    76: "iğdir", 77: "Yalova", 78: "Karabük", 79: "Kilis", 80: "Osmaniye",
    81: "Düzce"
}
def run_election():
    # Election işlemini burada gerçekleştirin
    election = Election()
    election.run()
@app.route('/')
def index():
    # thread = threading.Thread(target=run_election)
    # thread.start()

    return render_template('index.html',sehirler_dict=sehirler_dict)


@app.route('/secilen_il/<int:il_index>', methods=['GET', 'POST'])
def secilen_il(il_index=None):
    ilce_result = []
    if il_index is not None:
        # Seçilen ilin indexini kullanarak istediğiniz işlemleri yapabilirsiniz
        ilceler_dict = {}
        city = sehirler_dict.get(il_index)


        print("şsehir ", city)
        # il_index değeri belirtilmemişse veya geçerli bir il_index değeri alınamamışsa yapılacak işlemler

        json_files_dir = 'json_files'  # JSON dosyalarının bulunduğu dizin
        searhcFile=city.lower().strip()+".json"
        clean=clean_string(searhcFile)
        print(searhcFile)
        sonuc=[]
        with open(os.path.join(json_files_dir, "SecimSonucIl.json"), 'r', encoding='UTF-8') as file:
            data = json.load(file)

            for city in data:


                if city.get("İl Id")==str(il_index):
                    totalVote=int(str(city.get("Valid Total Number of Votes").replace(".", "")).strip())
                    tayyip=(int(str(city.get(" RECEP TAYYİP ERDOĞAN ")).replace(".", "").strip())/totalVote)*100
                    muharrem=(int(str(city.get(" MUHARREM İNCE ")).replace(".", "").strip())/totalVote)*100
                    meral=(int(str(city.get(" MERAL AKŞENER ")).replace(".", "").strip())/totalVote)*100
                    selahattin=(int(str(city.get(" SELAHATTİN DEMİRTAŞ ")).replace(".", "").strip())/totalVote)*100
                    temel=(int(str(city.get(" TEMEL KARAMOLLAOĞLU ")).replace(".", "").strip())/totalVote)*100
                    dogu=(int(str(city.get(" DOĞU PERİNÇEK ")).replace(".", "").strip())/totalVote)*100

                    sonuc.append(tayyip)
                    sonuc.append(muharrem)
                    sonuc.append(meral)
                    sonuc.append(selahattin)
                    sonuc.append(temel)
                    sonuc.append(dogu)

        getIlce(json_files_dir,clean,ilceler_dict)

        return render_template('city.html', sehirler_dict=sehirler_dict, ilceler_dict=ilceler_dict,
                                secilen_index=il_index,il_sonuc=sonuc,ilce_result=ilce_result)

    return render_template('city.html', sehirler_dict=sehirler_dict)


def getIlce(json_files_dir,searhcFile,ilceler_dict,ilce_result=None):

    for filename in os.listdir(json_files_dir):

        dosya = filename.lower().strip().split(".")
        print(f"dosya: {dosya[0]}  sercchfile:{searhcFile}")


        file=clean_string(dosya[0])
        if  searhcFile==file+".json":
            print("girdasdasdi", filename)
            with open(os.path.join(json_files_dir, filename), 'r', encoding='UTF-8') as file:
                data = json.load(file)

                for index,name in enumerate(data):

                    if name.get("Name of District") != '':
                        district_name = name.get("Name of District")
                        print(district_name)
                        totalVote = int(str(name.get("Valid Total Number of Votes").replace(".", "")).strip())
                        tayyip = (int(str(name.get(" RECEP TAYYİP ERDOĞAN ")).replace(".",
                                                                                      "").strip()) / totalVote) * 100
                        muharrem = (int(str(name.get(" MUHARREM İNCE ")).replace(".", "").strip()) / totalVote) * 100
                        meral = (int(str(name.get(" MERAL AKŞENER ")).replace(".", "").strip()) / totalVote) * 100
                        selahattin = (int(str(name.get(" SELAHATTİN DEMİRTAŞ ")).replace(".",
                                                                                         "").strip()) / totalVote) * 100
                        temel = (int(str(name.get(" TEMEL KARAMOLLAOĞLU ")).replace(".", "").strip()) / totalVote) * 100
                        dogu = (int(str(name.get(" DOĞU PERİNÇEK ")).replace(".", "").strip()) / totalVote) * 100


                        ilceler_dict[index] = district_name
                        if ilce_result is not None:

                            ilce_result[district_name]=[tayyip,muharrem,meral,selahattin,temel,dogu]
            ilceOfCity=ilceler_dict

            return ilceOfCity

ilce_result ={}
def clean_string(input_string):
    printable = set(string.printable)
    cleaned_string = ''.join(filter(lambda x: x in printable, input_string))
    return cleaned_string
@app.route('/secilen_ilce/<int:ilce_index>', methods=['GET', 'POST'])
def ilce(ilce_index:None):


    if ilce_index is not None:
        # Seçilen ilin indexini kullanarak istediğiniz işlemleri yapabilirsiniz
        ilceler_dict = {}
        sehir_id = request.args.get('sehir_id')
        city = sehirler_dict.get(int(sehir_id))


        # il_index değeri belirtilmemişse veya geçerli bir il_index değeri alınamamışsa yapılacak işlemler

        json_files_dir = 'json_files'  # JSON dosyalarının bulunduğu dizin
        searhcFile = city.lower() + ".json"

        sonuc = []


        ilceOfCity=getIlce(json_files_dir, searhcFile, ilceler_dict, ilce_result)
        print(ilceOfCity)
        ilce = ilceOfCity.get(ilce_index)
        print(" güncelle", ilce)
        result=ilce_result.get(ilce)


        return render_template('ilce.html', sehirler_dict=sehirler_dict, ilceler_dict=ilceler_dict,
                                secilen_index=sehir_id, il_sonuc=sonuc,
                               ilce_sonuc=result)

    return render_template('city.html', sehirler_dict=sehirler_dict)
ilceOfCity={}
@app.route('/get_ilce_data', methods=['GET'])
def get_ilce_data():
    ilceler_dict = {}
    sehir_id = request.args.get('sehir_id')
    city = sehirler_dict.get(sehir_id)
    json_files_dir = 'json_files'  # JSON dosyalarının bulunduğu dizin
    searhcFile = city.lower() + ".json"

    sonuc = []
    ilce_id = request.args.get('ilceId')
    print("ilce.e id: ",ilce_id)# AJAX isteğinden ilceId parametresini alın
    ilceOfCity = getIlce(json_files_dir, searhcFile, ilceler_dict, ilce_result)
    ilce_name=ilceOfCity.get(ilce_id)

    sonuc=ilce_result[ilce_name]
    print(f" ilçe sonucu: {ilce_name}")
    # ilce_id'ye göre ilçe verilerini alın veya hesaplayın
    # Örneğin, veritabanından ilçe verilerini sorgulayın veya hesaplamalar yapın

    # ilceData'yı oluşturun

    print("sonuc: ",sonuc)
    # JSON yanıtı döndürün
    response = {
        'ilceData': sonuc,
        'ilce':ilce_name
    }
    return jsonify(response)

if __name__=="__main__":
    app.run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
