import requests


def extract_qa():
    url = "http://10.4.145.209:8000/qa/Extract_QA_pairs/"

    # payload = {"type_word": "pdf"}
    # files={"text_file": open("media/docs/6156322755248062700.pdf", mode='rb')}
    # payload = {"type_word": "doc"}
    # files={"text_file": open("C:/Users/alpha/Desktop/123.doc", mode='rb')}
    payload = {"type_word": "pdf", "filepath": "C:/Users/alpha/Desktop/123.doc", "tag_list": ""}
    files={"text_file": open('C:/Users/alpha/Downloads/123.pdf', 'rb')}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=60000)
    print(response.text)
    # print(response.json())


def geonline():
    url = "http://10.4.145.209:7861/chat-docs/dagang-chat"
    payload = {"question": "你好", "history": []}
    headers = {}
    response = requests.request("POST", url, headers=headers, json=payload,  timeout=60000)
    print(response.text)
    # print(response.json())


def QAonline():
    url = "http://10.4.145.209:8000/qa/Text_QA/"
    payload = {"query": "你好", "choice": 'GLM', "tag_list": ""}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload,  timeout=60000)
    print(response.text)
    # url = "{}?{}".format(url, "&".join(["{}={}".format(k, v) for k, v in payload.items()]))
    # response = requests.request("GET", url, headers=headers, data=payload, timeout=60000)
    # print(response.text)
    # print(response.json())


def extract_ab():
    """
    生成摘要
    """
    url = "http://10.4.145.209:8000/qa/Texts_Summary/"

    payload = {"text": "你好"}
    files = [
        ('files_texts', ('123.pdf', open('C:/Users/alpha/Downloads/123.pdf', 'rb'), 'application/pdf')),
        ('files_texts', ('[Graph Embedding] DeepWalk- Online Learning of Social Representations (SBU 2014).pdf', open('C:/Users/alpha/Downloads/[Graph Embedding] DeepWalk- Online Learning of Social Representations (SBU 2014).pdf', 'rb'), 'application/pdf'))
    ]

    files = [
        ('files_texts', open('C:/Users/alpha/Downloads/123.pdf', 'rb')),
        ('files_texts', open('C:/Users/alpha/Downloads/123.pdf', 'rb'))
    ]
    headers = {}
    files = []
    response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=60000)
    print(response.text)
    # print(response.json())



def extract_text():
    """
    生成摘要
    """
    url = "http://10.4.145.209:8000/qa/Texts_reading/"

    payload = {"text": "你好"}
    files = [
        ('files_texts', ('123.pdf', open('C:/Users/alpha/Downloads/123.pdf', 'rb'), 'application/pdf')),
        ('files_texts', ('[Graph Embedding] DeepWalk- Online Learning of Social Representations (SBU 2014).pdf', open('C:/Users/alpha/Downloads/[Graph Embedding] DeepWalk- Online Learning of Social Representations (SBU 2014).pdf', 'rb'), 'application/pdf'))
    ]

    files = [
        ('files_texts', open('C:/Users/alpha/Downloads/123.pdf', 'rb')),
        ('files_texts', open('C:/Users/alpha/Downloads/123.pdf', 'rb'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=60000)
    print(response.text)
    # print(response.json())


if __name__ == '__main__':
    # QAonline()
    # geonline()
    # extract_qa()
    extract_text()
    pass
