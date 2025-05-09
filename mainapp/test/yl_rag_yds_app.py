import streamlit as st
import requests


def get_statistical_month_and_quarter(current_month):
    if current_month == 1:
        statistical_month = 1
        statistical_quarter = 1
    else:
        statistical_month = current_month - 1
        if 1 <= statistical_month <= 3:
            statistical_quarter = 1
        elif 4 <= statistical_month <= 6:
            statistical_quarter = 2
        elif 7 <= statistical_month <= 9:
            statistical_quarter = 3
        else:
            statistical_quarter = 4
    return statistical_month, statistical_quarter


def call_api(prompt):
    api_key = 'fc840267-2c20-43fb-b68c-50a9007597fe'
    messages = [
        {"role": "user", "content": prompt},
        {"role": "system", "content": "你是一名经验丰富的水调行业专家."}
    ]
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "deepseek-r1-distill-qwen-32b-250120",
        "messages": messages,
        "temperature": 0.1
    }
    try:
        response = requests.post(
            f"https://ark.cn-beijing.volces.com/api/v3/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API 请求出错: {e}")
        return None


def main():
    st.title("水权交易预测")

    # 用户输入
    current_month = st.number_input("当前月份 (1 - 12)", min_value=1, max_value=12, step=1)
    actual_water = st.number_input("实际用水量 (万m³)", min_value=0.0, step=0.1)
    planned_water = st.number_input("年计划用水下达量 (万m³)", min_value=0.0, step=0.1)
    permitted_water = st.number_input("取水许可量 (万m³)", min_value=0.0, step=0.1)

    historical_ratio_q1 = st.number_input("历史近三年第一季度用水量占比", min_value=0.0, max_value=1.0, step=0.01)
    historical_ratio_q2 = st.number_input("历史近三年前两季度用水量占比", min_value=0.0, max_value=1.0, step=0.01)
    historical_ratio_q3 = st.number_input("历史近三年前三季度用水量占比", min_value=0.0, max_value=1.0, step=0.01)

    historical_ratios = [historical_ratio_q1, historical_ratio_q2, historical_ratio_q3]

    # 获取统计月份和季度
    statistical_month, statistical_quarter = get_statistical_month_and_quarter(current_month)

    # 构建提示词
    prompt = f"当前时间为 2025 年 {current_month} 月，统计月份为 {statistical_month} 月，统计季度为第 {statistical_quarter} 季度。"\
        "实际用水量为 {actual_water} 万m³，年计划用水下达量为 {planned_water} 万m³，取水许可量为 {permitted_water} 万m³。"\
        "历史近三年第一季度用水量占比为 {historical_ratio_q1}，前两季度用水量占比为 {historical_ratio_q2}，前三季度用水量占比为 {historical_ratio_q3}。"\
        "请根据以下规则判断水权交易建议：推荐卖出：（1）第一季度累计实际用水量小于年计划用水下达量的 12.5%，推荐卖出；（2）第二季度累计实际用水量小于年计划用水下达量的 25%，推荐卖出；（3）第三季度累计实际用水量小于年计划用水下达量的 37.5%，推荐卖出；（4）第四季度年累计实际用水量小于年计划用水下达量的 50%，推荐卖出。"\
        "推荐买入：（1）第一季度的实际用水量超许可用水量 30%且第一季度的用水量占比高于历史近三年的第一季度占比 10%以上；（2）前两季度的实际用水量超许可用水量 60%且前两季度的用水量占比高于历史近三年的前两季度占比 10%以上；（3）前三季度的实际用水量超许可用水量 90%且前三季度的用水量占比高于历史近三年的前三季度占比 10%以上；（4）年度的实际用水量超许可用水量。"

    # 调用 API
    result = call_api(prompt)
    print("result：", result)
    if result:
        content = result['choices'][0]['message']['content'].strip()
        st.write(content)
        # 输出结果

if __name__ == "__main__":
    main()
    