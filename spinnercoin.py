import requests
import time
header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Connection" : "keep-alive",
        "Content-Length": "372",
        "Content-Type":"application/json",
        "Host":"back.timboo.pro",
        "Origin":"https://spinner.timboo.pro",
        "Referer":"https://spinner.timboo.pro/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-site",
        "User-Agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"       
    }
with open('query.txt', 'r') as file:
    querys = [line.strip() for line in file]

def get_info(query):
    url = 'https://back.timboo.pro/api/init-data'
    
    body = {
        "initData": query
    }

    response = requests.post(url,headers=header,json=body)
    if response.status_code == 200:
        return response.json()
    print("Token salah..")
    return

def auto_upgrade(query,id,tujuanlevel):
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Connection" : "keep-alive",
        "Content-Length": "372",
        "Content-Type":"application/json",
        "Host":"back.timboo.pro",
        "Origin":"https://spinner.timboo.pro",
        "Referer":"https://spinner.timboo.pro/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-site",
        "User-Agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"       
    }
    url = "https://back.timboo.pro/api/upgrade-spinner"
    body = {
        "initData": query,  
        "spinnerId": id
    }
    response = get_info(query)
    init_data = response["initData"]
    level = init_data["spinners"][0]["level"]
    hp = init_data["spinners"][0]["hp"]
    howmanyklik = int(hp / level) 
    if tujuanlevel == level:
        print(f"sudah level {tujuanlevel} tidak upgrade lagi")
        return
    response = requests.post(url=url,headers=header,json=body)
    print(response.json()["message"])
    if response.json()["message"] == "The spinner is upgraded.":
        response = get_info(query)
        init_data = response["initData"]
        level = init_data["spinners"][0]["level"]
        hp = init_data["spinners"][0]["hp"]
        howmanyklik = int(hp / level) 
        click_spin(query=query,howmanyklik=howmanyklik)
        print("Mencoba upgrade lagi")
        auto_upgrade(query=query,id=id,tujuanlevel=tujuanlevel)




def click_spin(query,howmanyklik):
    url = 'https://back.timboo.pro/api/upd-data'
    klik = howmanyklik
    if klik > 25 :
        while klik > 25 :
            body = {
                "initData": query,
                "data": {
                "clicks": 25,
                "isClose": None
                }
            }      
            klik-=25
            respones = requests.post(url=url,headers=header,json=body)
            print(f"sisa {klik} klik")
            time.sleep(1)
            response_spin(respones.json()["message"])
        if klik != 0:           
            respones = requests.post(url=url,headers=header,json=body)
            response_spin(respones.json()["message"])
    body = {
                "initData": query,
                "data": {
                "clicks": howmanyklik,
                "isClose": None
                }
            }
    respones = requests.post(url=url,headers=header,json=body)
    response_spin(respones.json()["message"])      
    return get_info(query)


def repair(query):
    url = 'https://back.timboo.pro/api/repair-spinner'
    body = {
        "initData" : query
    }
    response = requests.post(url=url,headers=header,json=body)
    return response.json()

def response_spin(a):
    if a == "Data acquisition error1":
        print("gagal spin")
    if a == "Data received successfully.":
        print("berhasil spin")


def main():
    autoupgrade = input("Mau auto upgrade level ? jika mau ketik 'y'  ")
    if (autoupgrade == "y") :
        maxautoupgrade = int(input("Mau upgrade sampe level berapa ?  "))
    
    while True :
        for query in querys:
            response = get_info(query)
            if response == None:
                continue
            init_data = response["initData"]
            level = init_data["spinners"][0]["level"]
            hp = init_data["spinners"][0]["hp"]
            id = init_data["user"]["mainSpinnerId"]
            print(f"====Nama : {init_data["user"]["name"]}===")
            print(f"Level : {level}")
            print(f"Hp : {hp}")
            print(f"Balance : {init_data["user"]["balance"]}")
            howmanyklik = int(hp / level) 
            if hp == 0:
                if init_data["spinners"][0]["endRepairTime"] == None:
                    responserepair = repair(query=query)
                    print(responserepair["message"])
                    print("berhasil memperbaiki")
                print("skip spin sedang di perbaiki")
            if hp != 0:   
                response = click_spin(query=query,howmanyklik=howmanyklik)
            hp = response["initData"]["spinners"][0]["hp"]
            if hp == 0:
                if init_data["spinners"][0]["endRepairTime"] == None:
                    responserepair = repair(query=query)
                    print("berhasil memperbaiki")       
            if autoupgrade == "y" :
                if level < maxautoupgrade:
                    print("mencoba upgrade")
                    auto_upgrade(query=query,id=id,tujuanlevel=maxautoupgrade)
        break
main()

