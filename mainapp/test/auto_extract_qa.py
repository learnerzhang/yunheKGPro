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
