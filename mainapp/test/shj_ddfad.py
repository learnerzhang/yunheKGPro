import collections
import ollama
import pandas as pd
import requests
import json
from collections import defaultdict

idx_list = ['水位', '入库', '出库', '蓄量', "流量"]
sknames = { '三门峡', '小浪底',  '陆浑', '故县', '河口村', '西霞院'}
swznames = { '花园口', '小花间'}
othnames = { '24h水位' }

def process_complex_header(file_path):
    """
    处理复杂表头的 Excel 表格，将多行表头合并为单行表头，并按照指定格式处理
    
    参数:
        file_path (str): Excel 文件路径
        
    返回:
        DataFrame: 处理后的 DataFrame
    """
    try:
        # 读取 Excel 文件，不指定表头
        df = pd.read_excel(file_path, header=None)
        # 获取表头信息
        header_data = []
        cur = 0
        for i in range(len(df)):
            row = df.iloc[i, :]
            cur += 1
            if not row.isnull().any():
                """
                如果当前行没有空值，跳出循环
                """
                break
            if i == 0:
                preValue = None
                for col in row:
                    if pd.isna(col):
                        header_data.append(preValue)
                    else:
                        preValue = col
                        header_data.append(col)
            else:
                for ii, col in enumerate(row):
                    if pd.isna(col):
                        continue
                    else:
                        header_data[ii] = f"{header_data[ii]}_{col}"
                pass

        # 检查表头行数是否合理
        if len(header_data) == 0:
            raise ValueError("未找到有效的表头行")
        
        
        # df.columns = header_data
        data_df = df.iloc[cur:]
        data_df.columns = header_data
        # data_df['时间'] = pd.to_datetime(data_df['时间']).apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        data_df.iloc[:, 0] = pd.to_datetime(data_df.iloc[:, 0]).apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        return data_df
        
    except Exception as e:
        print(f"Error processing complex header: {str(e)}")
        return pd.DataFrame()  # 返回空的 DataFrame 而不是错误信息字符串

def excel_to_json(file_path):
    """
    将 Excel 文件内容转换为 JSON 格式
    
    参数:
        file_path (str): Excel 文件路径
        
    返回:
        str: JSON 格式的字符串
    """
    try:
        # 处理复杂表头
        df = process_complex_header(file_path)
        
        # 如果 DataFrame 为空，返回空 JSON
        if df.empty:
            return json.dumps([])
        # 将 DataFrame 转换为 JSON
        json_data = df.to_json(orient='records', force_ascii=False, indent=4)
        return json_data
        
    except Exception as e:
        return f"Error converting Excel to JSON: {str(e)}"

def analyze_table_with_ollama(table_data):
    """
    使用 ollama 8b 识别表格数据
    
    参数:
        table_data (str): 表格数据（Markdown 格式）
        
    返回:
        str: ollama 的识别结果
    """

    prompt = f"""请解析以下表格数据：\n {table_data} \n\n, 
            已知第一行是表头，包括时间、区间引水、区间预报、花园口流量、水库名称及子表头水位、流量、入库、出库。
            表格有多行，表中每一行代表一个时间点，每列对应不同时间点下不同的水库的水位, 流量, 入库, 出库以及区间引水，区间预报、花园口流量、
            
            接下来需要你我提取其中的数据, 要求按照下面的格式输出:\n\n
            "XX水库": [["XX时间","XX水位", "XX流量", "XX入库", "XX出库"], ....],
            ...
            "XX区间引水": [["XX时间","XX区间引水"], ....],
            "XX区间预报": [["XX时间","XX区间预报"], ....],
            "花园口": [["XX时间": "XX流量"], ....]
        """
    try:
        response = ollama.generate(
            # model='deepseek-r1:8b',  # 需提前通过 ollama pull 下载】
            model='deepseek-r1:14b',  # 需提前通过 ollama pull 下载
            prompt=prompt,
            options={
                'temperature': 0.3,
                'max_tokens': 500
            }
        )
        return response['response']
    except Exception as e:
        return f"Error analyzing table with ollama: {str(e)}"


def excel_to_dict(ddfa_file_path):
    try:
        json_data = excel_to_json(ddfa_file_path)
        # print(file, "JSON 数据：\n", json_data)
        print("JSON 数据：\n", ddfa_file_path)
        skMapData = collections.defaultdict(dict)
        swMapData = collections.defaultdict(list)
        date_list = []
        for record in json.loads(json_data):
            record_keys = list(record.keys())
            new_record_keys = [ "".join(k.split("_")[:2]) for k in record_keys]
            for skname in sknames:
                for idx in idx_list:
                    for key in record_keys:
                        if skname in key and idx in key:
                            # print(skname, idx)
                            if idx not in skMapData[skname]:
                                skMapData[skname][idx] = [record[key]]
                            skMapData[skname][idx].append(record[key])
            for swname in swznames:
                for key in record_keys:
                    if swname in key:
                        swMapData[swname].append(record[key])
            
            if '时间' in record_keys:
                date_list.append(record['时间'])
            elif '月.日' in record_keys:
                date_list.append(record['月.日'])
        
        return skMapData, swMapData, date_list
    except Exception as e:
        return None
    

if __name__ == "__main__":

    # 文件列表
    # files = [
    #     "调度方案单13.xlsx",
    #     "调度方案单12.xlsx",
    #     "调度方案单11.xlsx",
    #     "调度方案单07.xlsx",
    #     "调度方案单04.xlsx",
    #     "调度方案单02.xlsx"
    # ]

    # for file in files:
    #     file_path = f"data/shj_ddfad/{file}"
    #     # df = pd.read_excel(file_path, sheet_name='Sheet1')
    #     # print(df.head(10))
    #     json_data = excel_to_json(file_path)
    #     print(file, "JSON 数据：\n", json_data)

    
    r = excel_to_dict("data/ddfa/3/调度方案单13.xlsx")
    print(r)