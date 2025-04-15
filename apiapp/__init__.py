import requests


def prod_extend(payload: dict, headers={}, postmethod=0, url="http://10.4.145.209:7861/chat-docs/text_extends"):
    """
        大模型文本扩写
    """
    print("extend_method:", postmethod)
    print("extend_extend:", payload)
    print("extend_ulr:", url)
    if postmethod == 0:
        try:
            response = requests.request("POST", url, headers=headers, json=payload, timeout=60000)
            return response.json()
        except:
            pass
    return {}


def prod_outline(payload: dict, headers={}, postmethod=0, url="http://10.4.145.209:7861/chat-docs/dagang-chat"):
    """
        大模型生产大纲
    """
    print("prod_method:", postmethod)
    print("prod_outline:", payload)
    print("outline_ulr:", url)
    if postmethod == 0:
        try:
            response = requests.request("POST", url, headers=headers, json=payload, timeout=60000)
            return response.json()
        except:
            pass
    return {}


def prod_qa(payload: dict, headers={}, postmethod=0, url="http://10.4.145.209:8000/qa/Text_QA/"):
    """
        大模型生产大纲
    """
    print("textqa_method:", postmethod)
    print("textqa_outline:", payload)
    print("textqa_ulr:", url)
    if postmethod == 0:
        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout=60000)
            tmpJson = response.json()
            print("QA-> ", tmpJson)
            return tmpJson
        except:
            pass
    else:
        try:
            url = "{}?{}".format(url, "&".join(["{}={}".format(k, v) for k, v in payload.items()]))
            print("prod_qa get ->", url)
            response = requests.request("GET", url, headers=headers, timeout=60000)
            return response.json()
        except:
            pass
    return {}


def prod_text2sql(payload: dict, headers={}, postmethod=0, url="http://10.4.145.209:8000/qa/Text_to_sql/"):
    """  Text2sql  """
    print("text2sql_method:", postmethod)
    print("text2sql_outline:", payload)
    print("text2sql_url:", url)
    if postmethod == 0:
        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout=60000)
            tmpJson = response.json()
            print("Text2sql-> ", tmpJson)
            return tmpJson
        except:
            pass
    else:
        try:
            url = "{}?{}".format(url, "&".join(["{}={}".format(k, v) for k, v in payload.items()]))
            print("prod_qa get ->", url)
            response = requests.request("GET", url, headers=headers, timeout=60000)
            return response.json()
        except:
            pass
    return {}


def prod_abstract(payload: dict, headers={}, files=[], postmethod=0, url="http://10.4.145.209:8000/qa/Texts_Summary/"):
    """
        大模型生产摘要
    """
    # payload = {"text": "你好"}
    # files = [
    #     ('files_texts', open('C:/Users/alpha/Downloads/123.pdf', 'rb')),
    #     ('files_texts', open('C:/Users/alpha/Downloads/123.pdf', 'rb'))
    # ]
    print("abstract_method:", postmethod)
    print("abstract_outline:", payload)
    print("abstract_ulr:", url)
    if postmethod == 0:
        try:
            response = requests.request("POST", url, headers=headers, files=files, data=payload, timeout=600000)
            return response.json()
        except:
            pass
    return {}


if __name__ == '__main__':
    payload = {'mid': '0', 'text': '你好'}
    rt = prod_abstract(payload)
    print(rt)
