from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# 创建 FastAPI 实例
app = FastAPI(title="Demo API", version="0.1.0")

# 示例数据
fake_items_db = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
]

# 定义数据模型
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(ItemCreate):
    id: int

class QueryItem(BaseModel):
    need_think: bool = False
    query: str

# 基础 GET 路由
@app.get("/")
async def root():
    return {"message": "Hello FastAPI!"}


@app.post("/query")
async def query(item: QueryItem):
    import requests

    queryTargetPools = {}
    queryTargetPools['榆林市水务集团有限责任公司'] = """
    年度	许可证编号	取水权人	许可水量（万m³）	水源类型	今年计划下达量（万m³）	去年用水量（万m³）	2025年取水量（万m3）	2025年1月	2025年2月	2025年3月	2024取水量（万m3）	2024年1月	2024年2月	2024年3月	2024年4月	2024年5月	2024年6月	2024年7月	2024年8月	2024年9月	2024年10月	2024年11月	2024年12月	2023取水量（万m3）	2023年1月	2023年2月	2023年3月	2023年4月	2023年5月	2023年6月	2023年7月	2023年8月	2023年9月	2023年10月	2023年11月	2023年12月	2022取水量（万m3）	2022年1月	2022年2月	2022年3月	2022年4月	2022年5月	2022年6月	2022年7月	2022年8月	2022年9月	2022年10月	2022年11月	2022年12月
    2024	C610802S2021-0041	榆林市水务集团有限责任公司	560	地表水	324	10.3	240	30	50	60	182.7472	2.3472	7.03	11.71	16.4	21.09	25.77	28.11	23.43	18.74	14.06	9.37	4.69	12.0295	0.15	0.46	0.76	1.08	1.39	1.7095	1.85	1.54	1.23	0.93	0.62	0.31	190.767	2.45	7.34	12.23	17.113	22.01	26.9	29.35	24.46	19.57	14.674	9.78	4.89

    """
    queryTargetPools['榆林高新区水务有限责任公司'] = """
    年度	许可证编号	取水权人	许可水量（万m³）	水源类型	今年计划下达量（万m³）	去年用水量（万m³）	2025年取水量（万m3）	2025年1月	2025年2月	2025年3月	2024取水量（万m3）	2024年1月	2024年2月	2024年3月	2024年4月	2024年5月	2024年6月	2024年7月	2024年8月	2024年9月	2024年10月	2024年11月	2024年12月	2023取水量（万m3）	2023年1月	2023年2月	2023年3月	2023年4月	2023年5月	2023年6月	2023年7月	2023年8月	2023年9月	2023年10月	2023年11月	2023年12月	2022取水量（万m3）	2022年1月	2022年2月	2022年3月	2022年4月	2022年5月	2022年6月	2022年7月	2022年8月	2022年9月	2022年10月	2022年11月	2022年12月
    2024	C610802S2023-0019	榆林高新区水务有限责任公司	2590	地表水、中水	2100	1639	358	100	124	134	1711.5551	21.93	65.83	109.72	153.6051	197.49	241.37	263.32	219.43	175.54	131.66	87.77	43.89	1639.3124	21.02	63.05	105.08	147.12	189.15	231.1924	252.2	210.17	168.13	126.1	84.07	42.03	1396.1373	17.9	53.7	89.5	125.29	161.09	196.89	214.79	178.99	143.1841	107.4032	71.6	35.8

    """
    queryTargetPools['榆林市水务集团王圪堵水库有限责任公司'] = """
    年度	许可证编号	取水权人	许可水量（万m³）	水源类型	今年计划下达量（万m³）	去年用水量（万m³）	2025年取水量（万m3）	2025年1月	2025年2月	2025年3月	2024取水量（万m3）	2024年1月	2024年2月	2024年3月	2024年4月	2024年5月	2024年6月	2024年7月	2024年8月	2024年9月	2024年10月	2024年11月	2024年12月	2023取水量（万m3）	2023年1月	2023年2月	2023年3月	2023年4月	2023年5月	2023年6月	2023年7月	2023年8月	2023年9月	2023年10月	2023年11月	2023年12月	2022取水量（万m3）	2022年1月	2022年2月	2022年3月	2022年4月	2022年5月	2022年6月	2022年7月	2022年8月	2022年9月	2022年10月	2022年11月	2022年12月
    2024	C610803S2021-0038	榆林市水务集团王圪堵水库有限责任公司	15600	地表水	4850	3919	135	81	32	22	3894.0064	49.91	149.77	249.62	349.46	449.31	549.15	599.08	499.23	399.39	299.5464	199.69	99.85	3119.055	39.99	119.96	199.932	279.92	359.89	439.87	479.853	399.88	319.9	239.93	159.95	79.98	3052.0166	39.13	117.39	195.63	273.9	352.1624	430.41	469.54	391.2842	313.03	234.77	156.51	78.26

    """
    queryTargetPools['陕西交通控股集团有限公司榆吴分公司'] = """
    年度	许可证编号	取水权人	许可水量（万m³）	水源类型	今年计划下达量（万m³）	去年用水量（万m³）	2025年取水量（万m3）	2025年1月	2025年2月	2025年3月	2024取水量（万m3）	2024年1月	2024年2月	2024年3月	2024年4月	2024年5月	2024年6月	2024年7月	2024年8月	2024年9月	2024年10月	2024年11月	2024年12月	2023取水量（万m3）	2023年1月	2023年2月	2023年3月	2023年4月	2023年5月	2023年6月	2023年7月	2023年8月	2023年9月	2023年10月	2023年11月	2023年12月	2022取水量（万m3）	2022年1月	2022年2月	2022年3月	2022年4月	2022年5月	2022年6月	2022年7月	2022年8月	2022年9月	2022年10月	2022年11月	2022年12月
    2024	C610802G2021-0042	陕西交通控股集团有限公司榆吴分公司	4	地下水	3.95	3.73	3.3	0.8	1.2	1.3	3.7774	0.05	0.14	0.24	0.34	0.44	0.53	0.58	0.48	0.39	0.29	0.19	0.1074	3.7325	0.05	0.1405	0.24	0.32	0.43	0.53	0.57	0.48	0.38	0.29	0.19	0.112	3.9572	0.0531	0.15	0.25	0.36	0.45	0.56	0.61	0.51	0.41	0.3	0.2041	0.1

    """
    queryTargetPools['陕西交通控股集团有限公司榆靖分公司'] = """
    年度	许可证编号	取水权人	许可水量（万m³）	水源类型	今年计划下达量（万m³）	去年用水量（万m³）	2025年取水量（万m3）	2025年1月	2025年2月	2025年3月	2024取水量（万m3）	2024年1月	2024年2月	2024年3月	2024年4月	2024年5月	2024年6月	2024年7月	2024年8月	2024年9月	2024年10月	2024年11月	2024年12月	2023取水量（万m3）	2023年1月	2023年2月	2023年3月	2023年4月	2023年5月	2023年6月	2023年7月	2023年8月	2023年9月	2023年10月	2023年11月	2023年12月	2022取水量（万m3）	2022年1月	2022年2月	2022年3月	2022年4月	2022年5月	2022年6月	2022年7月	2022年8月	2022年9月	2022年10月	2022年11月	2022年12月
    2024	C610824G2021-0043	陕西交通控股集团有限公司榆靖分公司	5.58	地下水	4.8	3.34	3.3	0.8	1.2	1.3	3.3034	0.04	0.13	0.21	0.3	0.38	0.47	0.51	0.42	0.34	0.2534	0.17	0.08	3.3359	0.04	0.13	0.2123	0.3	0.38	0.47	0.51	0.43	0.34	0.26	0.17	0.0936	3.313	0.04	0.13	0.21	0.31	0.38	0.47	0.51	0.42	0.343	0.25	0.17	0.08

    """
    queryTargetPools['子洲县元嘉糠醛生产销售有限公司'] = """
    年度	许可证编号	取水权人	许可水量（万m³）	水源类型	今年计划下达量（万m³）	去年用水量（万m³）	2025年取水量（万m3）	2025年1月	2025年2月	2025年3月	2024取水量（万m3）	2024年1月	2024年2月	2024年3月	2024年4月	2024年5月	2024年6月	2024年7月	2024年8月	2024年9月	2024年10月	2024年11月	2024年12月	2023取水量（万m3）	2023年1月	2023年2月	2023年3月	2023年4月	2023年5月	2023年6月	2023年7月	2023年8月	2023年9月	2023年10月	2023年11月	2023年12月	2022取水量（万m3）	2022年1月	2022年2月	2022年3月	2022年4月	2022年5月	2022年6月	2022年7月	2022年8月	2022年9月	2022年10月	2022年11月	2022年12月
    2025	D610831G2021-0003	子洲县元嘉糠醛生产销售有限公司	1.08	地下水	1	0.9	0.8	0.2	0.3	0.3	0.8	0.02	0.03	0.03	0.03	0.03	0.2	0.03	0.03	0.03	0.2	0.03	0.14	0.88	0.04	0.06	0.06	0.03	0.03	0.2	0.03	0.03	0.03	0.2	0.03	0.14	0.88	0.04	0.06	0.06	0.03	0.03	0.2	0.03	0.03	0.03	0.2	0.03	0.14

    """

    if not item.query in queryTargetPools:
        return {"error": "获取企业信息错误"}

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
            （1）第一季度的实际用水量超许可用水量30% 且第一季度的用水量占比高于历史近三年的第一季度占比10%以上；
            （2）前两季度的实际用水量超许可用水量60% 且前两季度的用水量占比高于历史近三年的前两季度占比10%以上；
            （3）前三季度的实际用水量超许可用水量90% 且前三季度的用水量占比高于历史近三年的前三季度占比10%以上；
            （4）年度的实际用水量超许可用水量。

        """ + queryTargetPools[item.query]  + """ \n
        需要按照上述数据逻辑确定企业最新用水月份(表中最新的数据是2025年3月份，需要判断当前季度是否需要水权交易)，已知当前是2025年4月份，首选确定当前所属的季度，和对应买、卖水的规则，最后判断下面企业是否存在结余水量，是否需要进行转让或受让？

    """

    api_key = 'fc840267-2c20-43fb-b68c-50a9007597fe'
    messages = [
        {"role": "user", "content": prompt },
        {"role": "system","content": "你是一名经验丰富的水调行业专家."},
    ]

    headers = {"Authorization": f"Bearer {api_key}"}

    model = "doubao-1-5-lite-32k-250115"
    if item.need_think:
        model = "deepseek-r1-distill-qwen-32b-250120"

    data = {
        # "model": "deepseek-r1-distill-qwen-32b-250120",
        # "model": "doubao-1-5-lite-32k-250115",
        "model": model,
        "messages": messages,
        "temperature": 0.1  # 降低随机性以提升稳定性
    }
    response = requests.post(f"https://ark.cn-beijing.volces.com/api/v3/chat/completions", headers=headers, json=data)
    return response.json()


# 带路径参数的 GET 路由
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    for item in fake_items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

# 带查询参数的 GET 路由
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# POST 路由（带请求体验证）
@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    new_id = len(fake_items_db) + 1
    new_item = {"id": new_id, **item.dict()}
    fake_items_db.append(new_item)
    return new_item