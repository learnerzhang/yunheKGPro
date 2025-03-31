from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, JSONLoader
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import codecs
import json

def extract_qa_pairs(chunks, ollama_model):
    qa_pairs = []
    for chunk in chunks:
        prompt = f"从下面的文本中抽取问答对: {chunk},  输出以`Q: `开头，`A: `结尾的文本。"
        response = ollama_model.generate([prompt])
        # print("-"*10)
        # print(response.generations[0][0].text)
        cct_str = response.generations[0][0].text
        for line in cct_str.splitlines():
            if line.startswith('Q:'):
                question = line[len('Q:'):].strip()
            elif line.startswith('A:'):
                answer = line[len('A:'):].strip()
                if len(question) > 10 and len(answer) > 10:
                    qa_pairs.append({"question": question, "answer": answer})
    return qa_pairs

def browse_folder_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            yield os.path.join(root, file)

def batch_upload_docs(folder_path):
    import requests
    def get_mime_type(filename):
        mime_types = {
            'txt': 'text/plain',
            'jpg': 'image/jpeg',
            'png': 'image/png',
            'xls': 'application/vnd.ms-excel'
        }
        ext = filename.split('.')[-1].lower()
        return mime_types.get(ext, 'application/octet-stream')

    for filepath in browse_folder_files('D://三门峡使用到的资料v2'):
        if filepath.endswith('.png') or filepath.endswith('.jpg') or filepath.endswith('.jpeg') or filepath.endswith('.gif') or filepath.endswith('.bmp') or filepath.endswith('.zip'):
            continue
        #  c4156447ce35e15447b3da91ac4f65aa

        url = "http://10.104.209.112:8000/apiapp/knowledge/upload"

        # 构造 FormData：文件 + 其他字段
        data = {"knowledge_id": "c4156447ce35e15447b3da91ac4f65aa", "tags": "RAG,知识库,智能问答"}

        filename = filepath.split(os.path.sep)[-1]
        mime_type = get_mime_type(filename)
        print("upload param:", filepath, mime_type, filename)
        # 上传文件时指定 MIME 类型
        with open(filepath, 'rb') as f:
            files = {'file': (filename, f, mime_type)}
            response = requests.post(url, data=data, files=files)
            print(response.text)
    
def upload_ragkg(qa_pairs):
    pass
    print("function ingest")

    docdir = 'D://云河资料//三门峡知识文档'
    # 初始化大模型 Ollama
    ollama = OllamaLLM(model="deepseek-r1:14b", temperature=0, max_tokens=512)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=200)

    final_qa_pairs = []
    for file in os.listdir(docdir):
        filepath = os.path.join(docdir, file)
        # filepath="D://workspace//yunheKGProWH//data//tst.pdf"# Save the uploaded file to a temporary file
        file_extension = os.path.splitext(filepath)[1]
        if file_extension.lower() == ".pdf":
            docs = PyPDFLoader(file_path=filepath).load()
        elif file_extension.lower() == ".txt":
            docs = TextLoader(file_path=filepath).load()
        elif file_extension.lower() == ".docx":
            docs = Docx2txtLoader(file_path=filepath).load()
        elif file_extension.lower() == '.json':
            docs = JSONLoader(file_path=filepath, jq_schema='.', text_content=False).load()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        print("function ingest end")
        
        chunks = text_splitter.split_documents(docs)
        # 提取问答对
        qa_pairs = extract_qa_pairs(chunks, ollama)
        for qa_pair in qa_pairs:
            qa_pair['source'] = str(file)
            final_qa_pairs.append(qa_pair)

    with  codecs.open('qa_pairs.json', 'w', 'utf-8') as f:
        json.dump(final_qa_pairs, f, ensure_ascii=False, indent=4)


if  __name__ == '__main__':
    batch_upload_docs('D://三门峡使用到的资料v2')
