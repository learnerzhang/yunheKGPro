import json
import requests
def test():
    url = "http://192.168.2.182:8000/dataapp/datamodelsearchoradd"#"http://192.168.2.182:8000/kgapp/kgtabtaglist"#
    response = requests.get(url,headers={'Content-Type': 'application/json'})
    print(response.text)

if __name__ == '__main__':
    #batch_QA()
    test()
print("aaaaaaa")