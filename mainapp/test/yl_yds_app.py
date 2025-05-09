import streamlit as st
import pandas as pd
import requests


def excel_to_markdown(file):
    df = pd.read_excel(file)
    markdown_table = df.to_csv(sep="|", na_rep="nan")
    header = "| " + markdown_table.split("\n", 1)[0] + " |"
    separator = "|-" + "-|-".join(["-" * len(cell) for cell in header.split("|")[1:-1]]) + "-|"
    rows = ["| " + row + " |" for row in markdown_table.strip().split("\n")[1:]]
    full_table = "\n".join([header, separator] + rows)
    return full_table


def call_large_model(prompt, api_key, model="deepseek-r1-distill-qwen-32b-250120", temperature=0.1):
    messages = [
        {"role": "user", "content": prompt},
        {"role": "system", "content": "你是一名经验丰富的水调行业专家."},
    ]

    headers = {"Authorization": f"Bearer {api_key}"}

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature  # 使用传入的温度参数
    }

    response = requests.post(
        f"https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        headers=headers,
        json=data
    )
    print(response.json())
    content = response.json()["choices"][0]["message"]["content"]
    return content


def main():
    prompt = """
        数据逻辑：
            若当前为1月份，实际用水的统计月份为1月份，统计季度为第一季度；当前时间是2~12月份，实际用水的统计月份为当前月份的前一个月份，统计季度为截止统计月份的所在季度。
            如当前月为2月份：该企业截止2025年1月份，实际用水量为**万m³，其计划下达量为***万m³、取水许可量为*万m³，第一季度的用水量在正常范围内，不需要进行水权交易。
            表述方式：（按证进行判断，若某企业存在多个证，依次将各个证的情况表述出来）
            正常：该企业***项日截止于2024年6月份，实际用水量为***万m³，其预算下达量为**万m³、取水许可量为***万m³，一至二季度的用水量均在正常范围，因此该企业只要保持正常的用水效率，暂时不需要进行水权交易。
            推荐买入：该企业***项日截止于2024年6月份，实际用水量为**万m³，其预算下达量为***万m³、取水许可量为*万m³，一至二季度的用水量超许可量60%，前两个季度的实际用水量占许可量比例为65%，历史平均占比为45%，因此判断设企业本年度水量不足，建议进行水权交易，及时买入水量。
            推荐卖出：该企业***项日截止于2024年6月份，实际用水量为***万m³，其预算下达量为***万m³、取水许可量为***万m³，由于一至二季度的用水量未达到预算下达量25%，因此判断该企业本年度存在节余水量，建议进行水权交易，对节余水量进行交易。

        推荐卖出：
            （1）第一季度累计实际用水量小于年计划用水下达量的12.5%，推荐卖出；
            （2）第二季度累计实际用水量小于年计划用水下达量的25%，推荐卖出；
            （3）第三季度累计实际用水量小于年计划用水下达量的37.5%，推荐卖出；
            （4）第四季度年累计实际用水量小于年计划用水下达量的50%，推荐卖出。
        推荐买入：
            （1）第一季度的实际用水量超许可用水量30%且第一季度的用水量占比高于历史近三年的第一季度占比10%以上；
            （2）前两季度的实际用水量超许可用水量60%且前两季度的用水量占比高于历史近三年的前两季度占比10%以上；
            （3）前三季度的实际用水量超许可用水量90%且前三季度的用水量占比高于历史近三年的前三季度占比10%以上；
            （4）年度的实际用水量超许可用水量。

        你需要按照上述数据逻辑确定企业最新用水月份，确定所属的季度，和对应买、卖水的规则，最后判断下面企业是否存在结余水量，是否需要进行转让或受让？

    """
    st.title("水权交易预测")

    # 增加 API Key 输入框
    default_api_key = 'ff47bc89-2fa3-4cd2-ae4f-49f11cb38cf0'
    api_key = st.text_input("请输入豆包 API Key", type="password", value=default_api_key)

    # 定义可选的模型列表
    model_options = [
        "deepseek-r1-distill-qwen-32b-250120",
        "doubao-1-5-lite-32k-250115",
        "doubao-1-5-pro-256k-250115",
        "doubao-1-5-pro-32k-250115",
    ]
    # 默认选中的模型
    default_model_index = model_options.index("doubao-1-5-lite-32k-250115")
    # 增加模型选择下拉框
    model_name = st.selectbox("请选择豆包模型名称", model_options, index=default_model_index)

    # 增加温度调节滑动条
    temperature = st.slider("请调节温度参数", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

    # 用户上传 Excel 文件
    uploaded_file = st.file_uploader("上传 Excel 文件", type=["xlsx", "xls"])

    if uploaded_file is not None and api_key:
        # 解析 Excel 文件为 Markdown 格式
        markdown_table = excel_to_markdown(uploaded_file)
        # 拼接提示词
        prompt += markdown_table

        # 调用大模型，传入温度参数
        model_result = call_large_model(prompt, api_key, model=model_name, temperature=temperature)
        st.write(f"大模型返回结果：{model_result}")


if __name__ == "__main__":
    main()
    