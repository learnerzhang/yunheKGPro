import json
from yaapp import yautils
from yaapp import divHtml, gx_sk, hkc_sk, img2base64, lhbs_sk, paraHtml, smx_sjt_sk, xld_sk, generate_ddjy, process_outflow,bold_left_align,pd2HtmlCSS,excel_to_html_with_merged_cells
from yaapp.api_yuan import (huanghe_diaodu_plan_ctx, huanghe_diaodu_plan_dfjson, huanghe_hedaoshuiqing_generate_dfjson, huanghe_shuikushuiqing_generate_dfjson, huanghe_yuqing_generate,huanghe_hedaoshuiqing_generate,huanghe_shuikushuiqing_generate,huanghe_gongqing_generate,huanghe_jiangyu13_forecast,huanghe_fenqu_jiangyu_forecast,huanghe_jiangyu47_forecast,huanghe_flood_forecast,huanghe_diaodu_plan,huanghe_shuiku_diaodu_result,huanghe_tanqu_yanmo,huanghe_keneng_danger,huanghe_xiangying_level,xld_yushui_context,
                            engineer_safety_shuikuyj,engineer_safety_shuiwenyj,engineer_safety_gongchengjcyj,shuniuFangAn,xldJZStatus,xldholeStatus,JZHoleRecommend,YingjiResponse,OrganizeBaoZhang_leader,OrganizeBaoZhang_zhihuibu,company_duty,team_baozhang,fangxun_table,xld_diaodu_table,huanghe_fenqu_jiangyu_forecast_dfjson,huanghe_flood_forecast_json,engineer_safety_shuikuyj_json,engineer_safety_shuiwenyj_json,engineer_safety_gongchengjcyj_json,xldJZStatus_json,JZHoleRecommend_json,xldholeStatus_json,
                            OrganizeBaoZhang_leader_json,OrganizeBaoZhang_zhihuibu_json,company_duty_json,team_baozhang_json,fangxun_table_json,xld_diaodu_table_json,huanghe_fenqu_jiangyu_forecast_dfjson,generate_description_for_label,map_input_to_label, huanghe_gongqing_generate_html,huanghe_diaodu_plan_yuanze_ctx,huanghe_diaodu_plan_yuanze_html,huanghe_diaodu_plan_jianyi_ctx,huanghe_diaodu_plan_jianyi_html,shj_yushui_context,shj_shuikuxushui_generate_dfjson,shj_shuikuxushui_generate,
                            shj_hedaoshuiqing_generate_dfjson,shj_hedaoshuiqing_generate,shj_laishuiyugu_context,shj_laishuiyugu_generate_dfjson,shj_laishuiyugu_generate,shj_hedaobijian_context,yiluohe_yuqing_generate,yiluohe_fenqu_jiangyu_forecast,yiluohe_future_7_forecast)
from yaapp.models import TemplateNode, WordParagraph
from datetime import datetime
import os
import base64
import re
from yaapp.rule import *
import logging
logger = logging.getLogger('kgproj')
import pandas as pd
class PlanFactory:
    def __init__(self, node: TemplateNode, context={}):
        self.context = context
        self.node = node
        # 搜集生成预案所需要的参数！！！
        self.param_path = self.context.get("param_path", "")
        try:
            with open(self.param_path, 'r', encoding='utf-8') as f:
                self.params = json.load(f)
        except Exception as e:
            self.params = {}
    def get_ysq(self):
        if self.context['type'] == 0:
            # 黄河中下游的河道水情
            #TODO
            # logger.debug("self.params:",   self.params)
            # logger.debug("type(self.params):",type(self.params))
            tmp = huanghe_yuqing_generate(self.params)
            ## 对每段描述内容进行细分
            wp = WordParagraph.objects.create(title="雨情实况", content=tmp, ctype=1)
            # self.node.wordParagraphs.clear()
            for n in self.node.wordParagraphs.all():
                n.delete()
            self.node.wordParagraphs.add(wp)
            return tmp
            # return ""
        elif self.context['type'] == 1 or self.context['type'] == 2:
            # 小浪底河道水情
            #TODO
            #tmp = huanghe_yuqing_generate(self.params)
            tmp = xld_yushui_context(self.params)
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="雨情实况", content=tmp, ctype=1)
            self.node.wordParagraphs.add(wp)
            return xld_yushui_context(self.params)
        elif self.context['type'] == 3:
            # 三花间河道水情
            #TODO
            #tmp = huanghe_yuqing_generate(self.params)
            yuqing= shj_yushui_context(self.params)
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="实时雨水情", content=yuqing, ctype=1)
            self.node.wordParagraphs.add(wp)
            current_date = datetime.now().strftime("%Y年%m月%d日")
            current_hour = datetime.now().strftime("%H时")
            skxs = f"水库蓄水：{current_date}，黄河主要水库蓄水情况见下表。"
            wp = WordParagraph.objects.create(title="实时雨水情", content=skxs, ctype=1)
            self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="河道水情", content=f"河干流重要水库蓄水情况表", ctype=1)
            # self.node.wordParagraphs.add(wp)
            tmpjson = shj_shuikuxushui_generate_dfjson(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="河道水情", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            tmp = shj_shuikuxushui_generate(self.params)
            hdsq = f"河道水情：黄河主要控制站{current_hour}蓄水情况见下表。"
            wp = WordParagraph.objects.create(title="实时雨水情", content=hdsq, ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = shj_hedaoshuiqing_generate_dfjson(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="河道水情", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            tmp_hdsq = shj_hedaoshuiqing_generate(self.params)
            return yuqing+"\n"+skxs+ "\n"+ divHtml(f"黄河干流重要水库{current_hour}蓄水情况表\n") + tmp + "\n" +hdsq+ "\n" + divHtml(f"黄河主要控制站{current_hour}蓄水情况表\n") + tmp_hdsq

    def get_hdsq(self):
        """
        获取河道水情
        """
        if self.context['type'] == 0:
            # 黄河中下游的河道水情
            # 表格部分
            for n in self.node.wordParagraphs.all():
                n.delete()
            # 新增描述部分
            current_date = datetime.now().strftime("%Y-%m-%d")
            wp = WordParagraph.objects.create(title="河道水情", content=f"黄河主要站点流量表（{current_date}）", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = huanghe_hedaoshuiqing_generate_dfjson(self.params)    # 新增表格部分 
            wp = WordParagraph.objects.create(title="河道水情", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            tmp = huanghe_hedaoshuiqing_generate(self.params)
            return divHtml(f"黄河主要站点流量表\n") + tmp
        elif self.context['type'] == 1:
            # 小浪底河道水情
            #TODO
            logger.debug("# 小浪底河道水情#TODO")
            return ""

    def get_sksq(self):
        """
        获取水库水情
        """
        if self.context['type'] == 0:
            # 黄河中下游
            #TODO
            for n in self.node.wordParagraphs.all():
                n.delete()
            # 新增描述部分
            current_date = datetime.now().strftime("%Y-%m-%d")
            wp = WordParagraph.objects.create(title="水库水情", content=f"黄河主要水库蓄水情况表（{current_date}）", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = huanghe_shuikushuiqing_generate_dfjson(self.params)    # 新增表格部分 
            wp = WordParagraph.objects.create(title="水库水情", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            return divHtml(f"黄河主要水库蓄水情况表\n") + huanghe_shuikushuiqing_generate(self.params)
        elif self.context['type'] == 1:
            # 小浪底
            #TODO
            return ""
    def get_gqxq(self):
        if self.context['type'] == 0:
            # 黄河中下游
            #TODO
            for n in self.node.wordParagraphs.all():
                n.delete()
            # 新增描述部分  
            # wp = WordParagraph.objects.create(title="工情险情", content="这是关于工情险情的描述内容", ctype=1)
            # self.node.wordParagraphs.add(wp)
            tmpjson = huanghe_gongqing_generate(self.params)
            #wp = WordParagraph.objects.create(title="水库水情", content=tmp, ctype=1)
            wp = WordParagraph.objects.create(title="工情险情", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            tmp = huanghe_gongqing_generate_html(self.params)#返回网页表格数据
            return tmp #tmpjson

        elif self.context['type'] == 1:
            # 小浪底
            #TODO
            return ""

    def get_jyyb(self):

        """
        获取降雨预报
        """
        logger.debug("get_jyyb", self.context)
        def jyyb_imgs(context):
            jyyb_imgs = context.get("jyyb_imgs", [])
            logger.debug(f" jyyb_imgs:{jyyb_imgs}")
            tmpHtml = ""
            tmp_content = []
            for imgJson in jyyb_imgs:
                logger.debug(f"jyyb img:{imgJson}")
                tmpdesc = imgJson['desc']
                tmpfname = imgJson['url']
                tmppath = os.path.join("data", "yuan_data",str(self.context['type']),"yubao", self.context['yadate'], tmpfname)
                #tmppath ="/data/jyybimgs/2023-07-23 /1.png"
                logger.debug(f"tmppath:{tmppath}")
                if not os.path.exists(tmppath):
                    logger.debug(f"文件不存在: {tmppath}")
                    continue
                logger.debug(f"降雨路径:{tmppath}")
                encoded_string = img2base64(tmppath)
                tmp_content.append({"content":encoded_string, "desc": tmpdesc})
                wp = WordParagraph.objects.create(title="降雨预报", content=encoded_string, ctype=2)
                self.node.wordParagraphs.add(wp)
                wp = WordParagraph.objects.create(title="降雨预报", content=tmpdesc, ctype=1)
                self.node.wordParagraphs.add(wp)
                tmpHtml += divHtml("<img src='data:image/png;base64," + encoded_string + "' width='50%'>") + "\n" + paraHtml(tmpdesc) + "\n"
            return tmpHtml,tmp_content

        if self.context['type'] == 0:
            # 黄河中下游
            for n in self.node.wordParagraphs.all():
                n.delete()
            jiangyu13 = huanghe_jiangyu13_forecast(self.params)
            # wp = WordParagraph.objects.create(title="降雨预报", content="1） 降雨预报   \n", ctype=0)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="降雨预报", content=jiangyu13, ctype=1)
            # self.node.wordParagraphs.add(wp)
            jyyb_img_html,tmp_content = jyyb_imgs(self.params)
            # wp = WordParagraph.objects.create(title="降雨预报", content="2） 未来3天降水预报图   \n", ctype=0)
            # self.node.wordParagraphs.add(wp)
            jiangyu_table = huanghe_fenqu_jiangyu_forecast(self.params)
            # 写入word
            wp = WordParagraph.objects.create(title="降雨预报", content="分区面平均雨量预报 \n", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpwpctx = huanghe_fenqu_jiangyu_forecast_dfjson(self.params)
            wp = WordParagraph.objects.create(title="降雨预报", content=json.dumps(tmpwpctx), ctype=3)
            self.node.wordParagraphs.add(wp)
            jiangyu47 = huanghe_jiangyu47_forecast(self.params)
            # wp = WordParagraph.objects.create(title="降雨预报", content="4）未来4—7天降水预报  \n", ctype=0)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="降雨预报", content=jiangyu47, ctype=1)
            # self.node.wordParagraphs.add(wp)
            #TODO
            # yubao = (f"1） 降雨预报   \n"
            #          f"\t{jiangyu13}\n"
            yubao = (#f"降雨预报\n"
                     f"\t{jyyb_img_html}\n"+
                     #f"分区面平均雨量预报   \n" + 
                     divHtml(f"黄河流域分区面平均雨量预报（单位：mm）  \n") + 
                     f"\t{jiangyu_table}\n")
                     # f"4）未来4—7天降水预报  \n"
                     # f"\t{jiangyu47}\n")
            #logger.debug(f"预报：{yubao}")
            return yubao
        elif self.context['type'] == 1:
            # 小浪底
            #TODO
            return ""
        elif self.context['type'] == 2:
            # 小浪底
            #TODO
            return ""
        elif self.context['type'] == 3:
            # 黄河汛情及水库调度方案单
            #TODO
            return ""
        elif self.context['type'] == 4:
            # 伊洛河
            jyyb_img_html,tmp_content = jyyb_imgs(self.params)
            jiangyu_table = yiluohe_fenqu_jiangyu_forecast(self.params)
            logger.debug(f"黄河流域分区面平均雨量预报（单位：mm）：{jiangyu_table}")
            tmpfname = self.params["jlyb"]
            tmppath = os.path.join("data", "yuan_data", str(self.context['type']), "yubao", self.context['yadate'],tmpfname)
            # tmppath ="/data/jyybimgs/2023-07-23 /1.png"
            logger.debug(f"tmppath: {tmppath}")
            if not os.path.exists(tmppath):
                logger.debug(f"文件不存在: {tmppath}")
            logger.debug(f"降雨路径:{tmppath}")
            encoded_string = img2base64(tmppath)
            jlyb = divHtml("<img src='data:image/png;base64," + encoded_string + "' width='50%'>")
            llyb = yiluohe_future_7_forecast(self.params)
            for n in self.node.wordParagraphs.all():
                n.delete()
            # 新增描述部分
            wp = WordParagraph.objects.create(title=f"未来7天降雨预报", content="降雨预报", ctype=1)
            self.node.wordParagraphs.add(wp)
            for item in tmp_content:
                wp = WordParagraph.objects.create(title=f"降雨预报图", content=item["content"], ctype=2)
                self.node.wordParagraphs.add(wp)
                wp = WordParagraph.objects.create(title=f"降雨预报描述", content=item["desc"], ctype=1)
                self.node.wordParagraphs.add(wp)

            wp = WordParagraph.objects.create(title="预报", content= "黄河流域分区面平均雨量预报（单位：mm）", ctype=1)
            self.node.wordParagraphs.add(wp)
            df = pd.DataFrame(self.params["ylhjyyb"])
            ylhjyyb_json = df.to_json(orient='records')
            wp = WordParagraph.objects.create(title="降雨预报表", content=json.dumps(ylhjyyb_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="q强降雨预警描述", content=self.params['qjsyj'], ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="预报", content="未来7天径流预报", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="径流预报图", content=encoded_string, ctype=2)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="预报", content="未来7天径日均流量预报", ctype=1)
            self.node.wordParagraphs.add(wp)
            df = pd.DataFrame(self.params["hhfloodforecast"])
            hhfloodforecast_json = df.to_json(orient='records')
            wp = WordParagraph.objects.create(title="未来7天径日均流量预报表", content=json.dumps(hhfloodforecast_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            return (bold_left_align("降雨预报")+"\n"+bold_left_align("未来7天降雨预报")+jyyb_img_html+ divHtml(f"黄河流域分区面平均雨量预报（单位：mm）  \n") + f"\t{jiangyu_table}\n"+"短时强降水预警\n"+self.params["qjsyj"]
                    +bold_left_align("洪水预报") +bold_left_align("未来7天径流预报") + jlyb+bold_left_align("未来7天日均流量预报")+llyb)

    def get_hsyb(self):
        """
        获取洪水预报
        """
        if self.context['type'] == 0:
            # 黄河中下游
            for n in self.node.wordParagraphs.all():
                n.delete()
            # 新增描述部分
            wp = WordParagraph.objects.create(title="洪水预报", content= "黄河上游未来七天径流预报", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = huanghe_flood_forecast_json(self.params)
            wp = WordParagraph.objects.create(title="洪水预报", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            #TODO
            #logger.debug("XXXXXXXXXXXXXX")
            return huanghe_flood_forecast(self.params)
        elif self.context['type'] == 1:
            # 小浪底
            #TODO
            return ""
    
    def get_ddfa(self):
        """
        获取调度方案
        """
        if self.context['type'] == 0:
            # 黄河中下游
            #TODO
            import pandas as pd
            import time
            yadate = self.context['plan']['yadate']
            ddfa_excel = os.path.join("data","yuan_data","0","ddfad",f"{yadate}.xlsx")
            #ddfa_excel="data/yuan_data/0/ddfad/2023-07-23.xlsx" 
            if not os.path.exists(ddfa_excel):
                logger.debug("ddfan_excel:",ddfa_excel)
                raise Exception("调度方案单不存在")
            skMapData, swMapData, date_list = yautils.excel_to_dict(ddfa_excel)
            smx_ckll, xld_ckll, lh_ckll, gx_ckll, hkc_ckll = yautils.skddjy(ddfa_excel)
            smx_ddjy = process_outflow(smx_ckll, date_list)
            xld_ddjy = process_outflow(xld_ckll, date_list)
            lh_ddjy = process_outflow(lh_ckll, date_list)
            gx_ddjy = process_outflow(gx_ckll, date_list)
            hkc_ddjy = process_outflow(hkc_ckll, date_list)
            # smx_ddjy = process_outflow(skMapData["三门峡"]["出库"], date_list)
            # xld_ddjy = process_outflow(skMapData["小浪底"]["出库"], date_list)
            # lh_ddjy = process_outflow(skMapData["陆浑"]["出库"], date_list)
            # gx_ddjy = process_outflow(skMapData["故县"]["出库"], date_list)
            # hkc_ddjy = process_outflow(skMapData["河口村"]["出库"], date_list)
            ddjy = "三门峡水库：" + smx_ddjy + "\n小浪底水库：" + xld_ddjy + "\n陆浑水库：" + lh_ddjy + "\n故县水库：" + gx_ddjy + "\n河口村水库：" + hkc_ddjy
            #ddjy = generate_ddjy(ddfa_excel)
            for n in self.node.wordParagraphs.all():
                n.delete()
            # 新增描述部分
            wp = WordParagraph.objects.create(title="调度方案", content="调度原则", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = huanghe_diaodu_plan_yuanze_ctx(self.params)
            wp = WordParagraph.objects.create(title="调度方案单", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度方案", content="调度建议", ctype=1)
            self.node.wordParagraphs.add(wp)
            #tmpjson = huanghe_diaodu_plan_jianyi_ctx(self.params)
            tmpjson = huanghe_diaodu_plan_jianyi_ctx(ddjy)
            wp = WordParagraph.objects.create(title="调度方案单", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            # tmp = huanghe_diaodu_plan_ctx(self.params)
            # wp = WordParagraph.objects.create(title="调度方案", content=tmp, ctype=1)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="调度方案单", content="黄河中下游调度方案单", ctype=1)
            # self.node.wordParagraphs.add(wp)
            # 新增调度方案附近即可
            # tmpjson = huanghe_diaodu_plan_dfjson(self.params)    # 新增表格部分 
            # wp = WordParagraph.objects.create(title="调度方案单", content=json.dumps(tmpjson), ctype=3)
            # self.node.wordParagraphs.add(wp)
            # 页面结果
            return huanghe_diaodu_plan(self.params)
        elif self.context['type'] == 1:
            # 小浪底
            #TODO
            return ""
        elif self.context['type'] == 2:
            # 小浪底
            #TODO
            return ""
        elif self.context['type'] == 3:
            # 黄河汛情及水库调度方案单
            import pandas as pd
            import time
            yadate = self.context['plan']['yadate']
            #ddfa_excel = os.path.join("media", "ddfa", str(self.context['plan']['ctype']), f"{yadate}.xlsx")
            ddfa_excel = os.path.join("data","yuan_data","3","ddfad",f"{yadate}.xlsx")
            #logger.debug(ddfa_excel)
            if not os.path.exists(ddfa_excel):
                raise Exception("调度方案单不存在")
            #ddjy = generate_ddjy(ddfa_excel)
            skMapData, swMapData, date_list = yautils.excel_to_dict(ddfa_excel)
            results = yautils.skddjy_new(ddfa_excel)
            # 初始化调度建议字符串
            ddjy_list = []
            # 遍历返回的结果字典
            for key, value in results.items():
                # 处理每个水库的出流量
                ckll = process_outflow(value, date_list)
                ddjy_list.append(f"{key}水库：{ckll}")
            # 将所有水库的调度建议合并为一个字符串
            ddjy = "\n".join(ddjy_list)
            skddresult = ""
            # funMap = {
            #     "小浪底": xld_sk,
            #     "三门峡": smx_sk,
            #     "陆浑": lh_sk,
            #     "故县": gx_sk,
            #     "河口村": hkc_sk,
            #     "花园口": hyk_sk
            # }
            sk2image = {}
            for skname in skMapData:
                record = skMapData[skname]
                keys = list(record.keys())

                if "水位" not in keys:
                    continue
                swdata = list(record["水位"])
                max_sw = max(swdata)
                max_idx = swdata.index(max_sw)
                max_date = date_list[max_idx]
                tmpimgpath = f"data/yuan_data/3/ddfadouts/{self.context['plan']['yadate']}/imgs/{skname}.png"
                #tmpimgpath = f"data/ddfaouts/{self.context['plan']['ctype']}/{self.context['plan']['yadate']}/imgs/{skname}.png"
                if not os.path.exists(tmpimgpath):
                    logger.debug(f"调度过程曲线不存在：{tmpimgpath}")
                    continue
                tmp_ddgc_img = img2base64(tmpimgpath)
                sk2image[skname] = tmp_ddgc_img
                tmp_ddgc_img_desc = f"{skname}调度过程({date_list[0]}~{date_list[-1]})"
                # TODO: 需要根据调度方案单的类型来确定调度方案单的函数
                tmp_ddjg_result = f"预计{skname}将于{max_date}达到最高水位{max_sw}m，{xld_sk(sw=max_sw)}；\n"
                skddresult += paraHtml(tmp_ddjg_result) + divHtml("<img src='data:image/png;base64," + tmp_ddgc_img + "'  width='50%' >") + "\n" + divHtml(tmp_ddgc_img_desc) + "\n"

            hd_result = ""
            sw2image = {}
            for swname in swMapData:
                # logger.debug("swMapdata:",swMapData)
                record = swMapData[swname]
                # logger.debug("records:",record)
                # keys = list(record.keys())
                # if "流量" not in keys:
                #     continue
                lldata = record  # list(record["流量"])
                max_ll = max(lldata)
                max_idx = lldata.index(max_ll)
                max_date = date_list[max_idx]

                #tmpimgpath = f"data/ddfaouts/{self.context['plan']['ctype']}/{self.context['plan']['yadate']}/imgs/{swname}.png"
                tmpimgpath = f"data/yuan_data/3/ddfadouts/{self.context['plan']['yadate']}/imgs/{swname}.png"
                if not os.path.exists(tmpimgpath):
                    logger.debug(f"调度过程曲线不存在：{tmpimgpath}")
                    continue
                sw2image[swname] = tmpimgpath
                tmp_ddgc_img = img2base64(tmpimgpath)
                sw2image[swname] = tmp_ddgc_img
                tmp_ddgc_img_desc = f"{swname}调度过程({date_list[0]}~{date_list[-1]})"
                tmp_result = f"预计{max_date}，{swname}出现{max_ll}立方米每秒的洪峰流量\n"
                hd_result = paraHtml(tmp_result) + divHtml("<img src='data:image/png;base64," + tmp_ddgc_img + "'  width='60%' >") + "\n" + paraHtml(tmp_ddgc_img_desc) + "\n"
            for n in self.node.wordParagraphs.all():
                n.delete()
            tmpjson = huanghe_diaodu_plan_jianyi_ctx(ddjy)
            wp = WordParagraph.objects.create(title="调度方案单", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度结果", content="水库调度过程线", ctype=1)
            self.node.wordParagraphs.add(wp)

            for skname, ddcimg in sk2image.items():
                wp = WordParagraph.objects.create(title=f"{skname}过程曲线", content=ddcimg, ctype=2)
                self.node.wordParagraphs.add(wp)

            wp = WordParagraph.objects.create(title="调度结果", content="水文站调度过程线", ctype=1)
            self.node.wordParagraphs.add(wp)
            for swname, imgpath in sw2image.items():
                wp = WordParagraph.objects.create(title=f"{swname}过程曲线", content=imgpath, ctype=2)
                self.node.wordParagraphs.add(wp)
            #TODO
            return huanghe_diaodu_plan_jianyi_html(ddjy)+ "1) 水库调度过程线 \n"+ f"{skddresult}\n"+ "2) 水文站调度过程线\n" + f"{hd_result}\n"
        elif self.context['type'] == 4:
            import pandas as pd
            import time
            yadate = self.context['plan']['yadate']
            ddfa_excel = os.path.join("data", "yuan_data", "4", "ddfad", f"{yadate}.xlsx")
            # logger.debug(ddfa_excel)
            ddfad = ""
            if not os.path.exists(ddfa_excel):
                raise Exception("调度方案单不存在")
            else:
                # df = pd.read_excel(ddfa_excel)
                # ddfad = pd2HtmlCSS() + df.to_html(index=False, justify="center")
                html_table = excel_to_html_with_merged_cells(ddfa_excel)
                ddfad = pd2HtmlCSS()+html_table
            skMapData, swMapData, date_list = yautils.excel_to_dict(ddfa_excel)
            results = yautils.skddjy_new(ddfa_excel)
            # 初始化调度建议字符串
            ddjy_list = []
            # 遍历返回的结果字典
            for key, value in results.items():
                ckll = process_outflow(value, date_list)
                #ddjy_list.append(f"{key}水库：{ckll}")
                ddjy_list.append([key, ckll])
            df = pd.DataFrame(ddjy_list, columns=["水库", "调度方式"])
            ddjy = pd2HtmlCSS() + df.to_html(index=False)
            for n in self.node.wordParagraphs.all():
                n.delete()
            ddfs_json=df.to_json(orient="records")
            wp = WordParagraph.objects.create(title="调度方案", content="调度运用方式", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度方案", content=json.dumps(ddfs_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度方案", content="调度运用方案单", ctype=1)
            self.node.wordParagraphs.add(wp)
            ddfad_json=pd.read_excel(ddfa_excel).to_json(orient="records")
            wp = WordParagraph.objects.create(title="调度方案", content=json.dumps(ddfad_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            # 将所有水库的调度建议合并为一个字符串
            #ddjy = "\n".join(ddjy_list)
            return (bold_left_align("调度运用方式")+ddjy+"\n"+bold_left_align("调度方案单")+ divHtml(f"伊洛河调度方案单\n")+ddfad)
    def get_ddjg(self):
        """
        获取调度方案
        """
        if self.context['type'] == 0:
            # 黄河中下游  对水库的调度进行细化
            # skddresult = huanghe_shuiku_diaodu_result(self.params)
            import pandas as pd
            import time
            yadate = self.context['plan']['yadate']
            #ddfa_excel = os.path.join("media", "ddfa", str(self.context['plan']['ctype']), f"{yadate}.xlsx")
            ddfa_excel = os.path.join("data","yuan_data","0","ddfad",f"{yadate}.xlsx")
            if not os.path.exists(ddfa_excel):
                raise Exception("调度方案单不存在")
            pd.set_option('display.notebook_repr_html', False)
            # 读取xls（绝对路径）
            df = pd.read_excel(io=ddfa_excel, header=None)
            if len(df) < 4:
                return """暂无数据"""

            ret = yautils.excel_to_dict(ddfa_excel)
            if ret is None:
                return """暂无数据"""
            
            skMapData, swMapData, date_list = ret
            skddresult = ""
            # funMap = {
            #     "小浪底": xld_sk,
            #     "三门峡": smx_sk,
            #     "陆浑": lh_sk,
            #     "故县": gx_sk,
            #     "河口村": hkc_sk,
            #     "花园口": hyk_sk
            # }

            sk2image = {}
            for skname in skMapData:
                record = skMapData[skname]
                keys = list(record.keys())
                
                if "水位" not in keys:
                    continue
                swdata = list(record["水位"])
                max_sw = max(swdata)
                max_idx = swdata.index(max_sw)
                max_date = date_list[max_idx]

                #tmpimgpath = f"data/ddfaouts/{self.context['plan']['ctype']}/{self.context['plan']['yadate']}/imgs/{skname}.png"
                tmpimgpath = f"data/yuan_data/0/ddfadouts/{self.context['plan']['yadate']}/imgs/{skname}.png"
                #ddfa_excel = os.path.join("data","yuan_data","0","ddfad",f"{yadate}.xlsx")
                if not os.path.exists(tmpimgpath):
                    logger.debug(f"调度过程曲线不存在：{tmpimgpath}")
                    continue
                tmp_ddgc_img = img2base64(tmpimgpath)
                sk2image[skname] = tmp_ddgc_img
                tmp_ddgc_img_desc = f"{skname}调度过程({date_list[0]}~{date_list[-1]})"
                # TODO: 需要根据调度方案单的类型来确定调度方案单的函数
                tmp_ddjg_result = f"预计{skname}将于{max_date}达到最高水位{max_sw}m；\n"#，{xld_sk(sw=max_sw)}
                skddresult += paraHtml(tmp_ddjg_result) + divHtml("<img src='data:image/png;base64," + tmp_ddgc_img + "' width='50%'>") + "\n" + divHtml(tmp_ddgc_img_desc) + "\n"


            hd_result = ""
            sw2image = {}
            for swname in swMapData:
                #logger.debug("swMapdata:",swMapData)
                record = swMapData[swname]
                # logger.debug("records:",record)
                # keys = list(record.keys())
                if "流量" not in keys:
                    continue
                lldata = record  #list(record["流量"])
                max_ll = max(lldata)
                max_idx = lldata.index(max_ll)
                max_date = date_list[max_idx]

                #tmpimgpath = f"data/ddfaouts/{self.context['plan']['ctype']}/{self.context['plan']['yadate']}/imgs/{swname}.png"
                tmpimgpath = f"data/yuan_data/0/ddfadouts/{self.context['plan']['yadate']}/imgs/{swname}.png"
                if not os.path.exists(tmpimgpath):
                    logger.debug(f"调度过程曲线不存在：{tmpimgpath}")
                    continue
                sw2image[swname] = tmpimgpath
                tmp_ddgc_img = img2base64(tmpimgpath)
                tmp_ddgc_img_desc = f"{swname}调度过程({date_list[0]}~{date_list[-1]})"
                tmp_result = f"预计{max_date}，{swname}出现{max_ll}立方米每秒的洪峰流量\n"
                hd_result = paraHtml(tmp_result) + divHtml("<img src='data:image/png;base64," + tmp_ddgc_img + "' width='50%'>" ) + "\n" + paraHtml(tmp_ddgc_img_desc) + "\n"
            
            tqym = huanghe_tanqu_yanmo(self.params)
            keneng_danger = huanghe_keneng_danger(self.params)
            xiangying_level = huanghe_xiangying_level(self.params)
            diaodu_result = (f"\n"
                             f"1) 水库 \n"
                             f"{skddresult}\n"
                             f"2) 河道\n"
                             f"{hd_result}\n"
                             f"3) 滩区淹没\n"
                             f"{tqym}\n"
                             f"4) 可能出险情况\n"
                             f"{keneng_danger}\n"
                             f"5) 预警及响应等级\n"
                             f"{xiangying_level}"
                             )
            tb_ddjg = [
                {"名称": "滩区淹没", "调度结果": tqym},
                {"名称": "可能出险情况", "调度结果": keneng_danger},
                {"名称": "预警及响应等级", "调度结果": xiangying_level},
            ]
            df = pd.DataFrame(tb_ddjg)
            tb_ddjg_json = df.to_json(orient="records")
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="调度结果", content="水库", ctype=1)
            self.node.wordParagraphs.add(wp)

            for skname, ddcimg in sk2image.items():
                wp = WordParagraph.objects.create(title=f"{skname}过程曲线", content=ddcimg, ctype=2)
                self.node.wordParagraphs.add(wp)

            wp = WordParagraph.objects.create(title="调度结果", content="河道", ctype=1)
            self.node.wordParagraphs.add(wp)
            for swname, imgpath in sw2image.items():
                wp = WordParagraph.objects.create(title=f"{swname}过程曲线", content=imgpath, ctype=2)
                self.node.wordParagraphs.add(wp)

            wp = WordParagraph.objects.create(title="调度结果", content="滩区淹没", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="滩区淹没结果", content=tqym, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度结果", content="可能出险", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="可能出险情况", content=keneng_danger, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度结果", content="预警响应", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="预警响应及等级", content=xiangying_level, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度方案单", content=json.dumps(tb_ddjg_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="调度结果", content="滩区淹没", ctype=1)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="滩区淹没结果", content=tqym, ctype=1)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="调度结果", content="可能出险", ctype=1)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="可能出险情况", content=keneng_danger, ctype=1)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="调度结果", content="预警响应", ctype=1)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="预警响应及等级", content=xiangying_level, ctype=1)
            # self.node.wordParagraphs.add(wp)
            #TODO
            return diaodu_result
        elif self.context['type'] == 1:
            # 小浪底
            #TODO
            return ""
        elif self.context['type'] == 3:
            # 三花间
            #TODO
            return ""
        elif self.context['type'] == 4:
            # 伊洛河
            import pandas as pd
            import time
            yadate = self.context['plan']['yadate']
            ddfa_excel = os.path.join("data", "yuan_data", "4", "ddfad", f"{yadate}.xlsx")
            # logger.debug(ddfa_excel)
            if not os.path.exists(ddfa_excel):
                raise Exception("调度方案单不存在")
            if not os.path.exists(ddfa_excel):
                raise Exception("调度方案单不存在")
            else:
                # df = pd.read_excel(ddfa_excel)
                # ddfad = pd2HtmlCSS() + df.to_html(index=False, justify="center")
                html_table = excel_to_html_with_merged_cells(ddfa_excel)
                ddfad = pd2HtmlCSS()+html_table
            skMapData, swMapData, date_list = yautils.excel_to_dict(ddfa_excel)
            results = yautils.skddjy_new(ddfa_excel)
            # 初始化调度建议字符串
            ddjy_list = []
            # 遍历返回的结果字典
            for key, value in results.items():
                ckll = process_outflow(value, date_list)
                #ddjy_list.append(f"{key}水库：{ckll}")
                ddjy_list.append([key, ckll])
            df = pd.DataFrame(ddjy_list, columns=["水库", "调度方式"])
            ddjy = pd2HtmlCSS() + df.to_html(index=False)
            ddfs_json=df.to_json(orient="records")
            skMapData, swMapData, date_list = yautils.excel_to_dict(ddfa_excel)
            skddresult = ""
            sk_ddjg=[]
            sk2image = {}
            for skname in skMapData:
                record = skMapData[skname]
                keys = list(record.keys())
                if "水位" not in keys:
                    continue
                swdata = list(record["水位"])
                max_sw = max(swdata)
                max_idx = swdata.index(max_sw)
                max_date = date_list[max_idx]
                tmpimgpath = f"data/yuan_data/4/ddfadouts/{self.context['plan']['yadate']}/imgs/{skname}.png"
                if not os.path.exists(tmpimgpath):
                    logger.debug(f"调度过程曲线不存在：{tmpimgpath}")
                    continue
                tmp_ddgc_img = img2base64(tmpimgpath)
                sk2image[skname] = tmp_ddgc_img
                tmp_ddgc_img_desc = f"{skname}调度过程({date_list[0]}~{date_list[-1]})"
                # TODO: 需要根据调度方案单的类型来确定调度方案单的函数
                tmp_ddjg_result = f"预计{skname}将于{max_date}达到最高水位{max_sw}m；\n"#，{xld_sk(max_sw)['result']}
                skddresult += paraHtml(tmp_ddjg_result) + divHtml(
                    "<img src='data:image/png;base64," + tmp_ddgc_img + "'  width='50%' >") + "\n" + divHtml(
                    tmp_ddgc_img_desc) + "\n"
                sk_ddjg.append({"img64":tmp_ddgc_img,"desc":tmp_ddjg_result,"tmp_ddgc_img_desc":tmp_ddgc_img_desc})
            hd_result = ""
            hd_ddjg=[]
            sw2image = {}
            for swname in swMapData:
                record = swMapData[swname]
                lldata = record  # list(record["流量"])
                max_ll = max(lldata)
                max_idx = lldata.index(max_ll)
                max_date = date_list[max_idx]
                tmpimgpath = f"data/yuan_data/4/ddfadouts/{self.context['plan']['yadate']}/imgs/{swname}.png"
                if not os.path.exists(tmpimgpath):
                    #logger.debug(f"调度过程曲线不存在：{tmpimgpath}")
                    continue
                sw2image[swname] = tmpimgpath
                tmp_ddgc_img = img2base64(tmpimgpath)
                sw2image[swname] = tmp_ddgc_img
                tmp_ddgc_img_desc = f"{swname}调度过程({date_list[0]}~{date_list[-1]})"
                tmp_result = f"预计{max_date}，{swname}出现{max_ll}立方米每秒的洪峰流量\n"
                hd_result = paraHtml(tmp_result) + divHtml(
                    "<img src='data:image/png;base64," + tmp_ddgc_img + "'  width='60%' >") + "\n" + paraHtml(
                    tmp_ddgc_img_desc) + "\n"
                hd_ddjg.append({"img64": tmp_ddgc_img, "desc": tmp_result, "tmp_ddgc_img_desc": tmp_ddgc_img_desc})
            #tqym = huanghe_tanqu_yanmo(self.params)
            hyk_liuliang = 3000
            tqym = tanquyanmo(hyk_liuliang)["result"]

            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="调度方案", content="调度运用方式", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="水库调度方案", content=json.dumps(ddfs_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度结果", content="水库", ctype=1)
            self.node.wordParagraphs.add(wp)
            for item in sk_ddjg:
                wp = WordParagraph.objects.create(title="水库调度结果描述", content=item["desc"], ctype=1)
                self.node.wordParagraphs.add(wp)
                wp = WordParagraph.objects.create(title="水库调度结果图", content=item["img64"], ctype=2)
                self.node.wordParagraphs.add(wp)
                wp = WordParagraph.objects.create(title="水库调度过程", content=f"\t\t{item['tmp_ddgc_img_desc']}", ctype=1)
                self.node.wordParagraphs.add(wp)
            for item in hd_ddjg:
                wp = WordParagraph.objects.create(title="河道调度结果描述", content=item["desc"], ctype=1)
                self.node.wordParagraphs.add(wp)
                wp = WordParagraph.objects.create(title="河道调度结果图", content=item["img64"], ctype=2)
                self.node.wordParagraphs.add(wp)
                wp = WordParagraph.objects.create(title="河道调度过程", content=f"\t\t{item['tmp_ddgc_img_desc']}", ctype=1)
                self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度结果", content="滩区淹没", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="滩区淹没", content=tqym, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="调度方案", content="调度运用方案单", ctype=1)
            self.node.wordParagraphs.add(wp)
            ddfad_json = pd.read_excel(ddfa_excel).to_json(orient="records")
            wp = WordParagraph.objects.create(title="调度方案单", content=json.dumps(ddfad_json), ctype=3)
            self.node.wordParagraphs.add(wp)

            #(bold_left_align("调度运用方式")+ddjy+"\n"+bold_left_align("调度方案单")+ divHtml(f"伊洛河调度方案单\n")+ddfad)
            return (bold_left_align("调度运用方式")+ddjy+bold_left_align("水库")+skddresult+bold_left_align("河道")+hd_result+bold_left_align("滩区淹没")+tqym+"\n"+bold_left_align("调度方案单")+ divHtml(f"伊洛河调度方案单\n")+ddfad)#+
                    # bold_left_align("可能出险")+kncx+bold_left_align("应对措施") + ydcs+bold_left_align("分级响应") + yjdj +
                    # bold_left_align("河道破堤实施方案") + hdpdssfa+bold_left_align("人员转移方案")+ryzyfa  +  bold_left_align("防汛物资储备和防汛抢险队伍") + fxwz)

    def get_gcyp(self):
        if self.context['type'] == 0:
            # 黄河中下游
            #TODO
            return ""
        elif self.context['type'] == 1:
            # 小浪底
            #TODO
            xld_shukuyujing = engineer_safety_shuikuyj(self.params)
            xld_shuwenyujing = engineer_safety_shuiwenyj(self.params)
            xld_gongchengjcyj = engineer_safety_gongchengjcyj(self.params)
            yushui_result = (
                             f"水库预警情况表\n"
                             f"{xld_shukuyujing}\n"
                             f"水文站预警情况表\n"
                             f"{xld_shuwenyujing}\n"
                             f"工程监测指标预警情况表\n"
                             f"{xld_gongchengjcyj}\n"
                             )
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="工程研判", content="水库预警情况表", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = engineer_safety_shuikuyj_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="水库预警情况表", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="工程研判", content="水文站预警情况表", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = engineer_safety_shuiwenyj_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="水文站预警情况表", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="工程研判", content="工程监测指标预警情况表", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = engineer_safety_gongchengjcyj_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="工程监测指标预警情况表", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            return yushui_result
    def get_snyy(self):
        def ddgc_img(context):
            ddgc_img = context.get("visualEchartsImgUrl")
            tmpHtml = ""
            # for imgJson in jyyb_imgs:
            #     tmpdesc = imgJson['desc']
            #     tmpurl = imgJson['url']
            #     with open(os.path.join("static", tmpurl), "rb") as image_file:
            #         encoded_string = base64.b64encode(image_file.read())
            #         logger.debug(encoded_string.decode('utf-8'))
            wp = WordParagraph.objects.create(title="枢纽运用", content="预报小浪底水库的调度过程", ctype=1)
            self.node.wordParagraphs.add(wp)
            encoded_string = re.sub('^data:image/.+;base64,', '', ddgc_img)
            wp = WordParagraph.objects.create(title="降雨预报", content=encoded_string, ctype=2)
            self.node.wordParagraphs.add(wp)
            tmpHtml +=  "预报小浪底水库的调度过程" + "\n""<img src='data:image/png;base64," + encoded_string + "' width='50%'>" + "\n"
            return tmpHtml
        if self.context['type'] == 0:
            # 黄河中下游
            #TODO
            return ""
        elif self.context['type'] == 1:
            shuniu_apply = shuniuFangAn(self.params)
            JZStatus = xldJZStatus(self.params)
            holeStatus = xldholeStatus(self.params)
            HoleRecommend = JZHoleRecommend(self.params)
            JZHoleYunYong=(f"机组、孔洞运用方式推荐\n按照《黄河水利水电开发集团有限公司2021年防汛抢险应急预案》中的“小浪底水利枢纽泄洪系统孔洞组合运用方案”，结合目前孔洞开启情况，"
               f"{self.params['DFORECASTTIME']}，孔洞组合运用方式如下：\n"
               f"机组、孔洞运用方式推荐表")
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="枢纽运用方案", content=shuniu_apply, ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpHtml = ddgc_img(self.params)
            wp = WordParagraph.objects.create(title="枢纽运用方案", content="小浪底机组状态表", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = xldJZStatus_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="小浪底机组状态表", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="枢纽运用方案", content="小浪底孔洞状态表", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = xldholeStatus_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="小浪底孔洞状态表", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="枢纽运用方案", content= JZHoleYunYong, ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = JZHoleRecommend_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="小浪底孔洞状态表", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            shuniu_apply_result = (f"三   枢纽运用方案\n"
                                   f"{shuniu_apply}\n"
                                   f"{tmpHtml}\n"
                                   #f"预报小浪底水库的调度过程\n"
                                   f"小浪底机组状态表\n"
                                   f"{JZStatus}\n"
                                   f"小浪底孔洞状态表\n"
                                   f"{holeStatus}\n"
                                   f"机组、孔洞运用方式推荐\n"
                                   f"{HoleRecommend}\n"
                                   )
            # 小浪底
            #TODO
            return shuniu_apply_result
    def get_aqjc(self):
        if self.context['type'] == 0:
            return ""       
        elif self.context['type'] == 1:
            xld_yingji = YingjiResponse(self.params)
            zuzhibaozhang = OrganizeBaoZhang_leader(self.params)
            zhihuibaozhang = OrganizeBaoZhang_zhihuibu(self.params)
            gongsi_duty = company_duty(self.params)
            duiwu_baozhang = team_baozhang(self.params)
            fangxun_information = fangxun_table(self.params)
            diaodu_table = xld_diaodu_table(self.params)
            safety_result = (f"4.1  应急响应措施\n"
                            f"{xld_yingji}\n"
                            f"4.2  应急保障\n"
                            f"组织保障\n"
                            f"小浪底管理中心防汛领导小组人员信息表\n"
                            f"{zuzhibaozhang}\n"
                            f"小浪底水利枢纽、西霞院工程防汛应急抢险指挥部\n"
                            f"{zhihuibaozhang}\n"
                            f" 开发公司防汛指挥部成员防汛职责信息表\n"
                            f"{gongsi_duty}\n"
                            f"队伍保障人员信息表\n"
                            f"{duiwu_baozhang}\n"
                            f"防汛物资信息表\n"
                            f"{fangxun_information}\n"
                            f"附表1\n 预报小浪底水库的调度过程\n"
                            f"{diaodu_table}"
                            )
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="安全举措", content=f"应急响应措施\n{xld_yingji}", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="安全举措", content=f"组织保障\n小浪底管理中心防汛领导小组人员信息表", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = OrganizeBaoZhang_leader_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="安全举措", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="安全举措", content=f"小浪底水利枢纽、西霞院工程防汛应急抢险指挥部", ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = OrganizeBaoZhang_zhihuibu_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="小浪底水利枢纽、西霞院工程防汛应急抢险指挥部", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="安全举措", content=f"公司职责\n开发公司防汛指挥部成员防汛职责信息表",
                                            ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = company_duty_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="安全举措", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="安全举措", content=f"队伍保障\n队伍保障人员信息表",ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = team_baozhang_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="安全举措", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="安全举措", content=f"物资保障\n防汛物资信息表",ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = fangxun_table_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="安全举措", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="安全举措", content=f"附表1\n预报小浪底水库的调度过程",ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = xld_diaodu_table_json(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="安全举措", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            return safety_result
        elif self.context['type'] == 2:
            return ""
        elif self.context['type'] == 3:
            return ""
        elif self.context['type'] == 4:
            yjdj = yujingdengji()["level"]  # "黄色预警"
            ydcs = yujingdengji()["result"]
            df = pd.DataFrame(self.params["goodsTable"])
            fxwz = pd2HtmlCSS() + df.to_html(index=False)

            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="预警分级响应", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"预警等级", content=yjdj, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="应对措施", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"应对措施", content=ydcs, ctype=1)
            self.node.wordParagraphs.add(wp)
            zzbz= "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="组织保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"组织保障", content=zzbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            dwbz = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="队伍保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"队伍保障", content=dwbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            wuzi_json = pd.DataFrame(self.params["goodsTable"]).to_json(orient="records")
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="物资保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"物资保障", content=json.dumps(wuzi_json),ctype=3)
            self.node.wordParagraphs.add(wp)
            jsbz = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="技术保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"技术保障", content=jsbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            txbz = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="通信保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"通信保障", content=txbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            zmyjbz = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="照明应急保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"照明应急保障", content=zmyjbz , ctype=1)
            self.node.wordParagraphs.add(wp)
            aqbz = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="安全保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"安全保障", content=aqbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            wsbz = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="卫生保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"卫生保障", content=wsbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            qtbz = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="其他保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"其他保障", content=qtbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            xcyy = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="宣传和卫生演练", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"宣传和卫生演练", content=xcyy, ctype=1)
            self.node.wordParagraphs.add(wp)
            return bold_left_align("预警分级响应") + yjdj+bold_left_align("应对措施") + ydcs +bold_left_align("应急保障") +bold_left_align("组织保障")+zzbz+bold_left_align("队伍保障")+dwbz+bold_left_align("物资保障")+fxwz+bold_left_align("技术保障")+jsbz+bold_left_align("通信保障")+txbz+bold_left_align("照明应急保障")+zmyjbz+bold_left_align("安全保障")+aqbz+bold_left_align("卫生保障")+wsbz+bold_left_align("其他保障")+qtbz+bold_left_align("宣传和卫生演练")+xcyy
    def get_lsyg(self):
        if self.context['type'] == 0:
            return ""
        elif self.context['type'] == 1:
            return ""
        elif self.context['type'] == 2:
            return ""
        elif self.context['type'] == 3:
            for n in self.node.wordParagraphs.all():
                n.delete()
                # 新增描述部分
            tmp = shj_laishuiyugu_context(self.params)
            wp = WordParagraph.objects.create(title="来水预估", content=tmp, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="来水预估", content=f"黄河主要控制站及区间来水预估情况表",ctype=1)
            self.node.wordParagraphs.add(wp)
            tmpjson = shj_laishuiyugu_generate_dfjson(self.params)  # 新增表格部分
            wp = WordParagraph.objects.create(title="来水预估", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            return divHtml("黄河主要控制站及区间来水预估情况表\n") +shj_laishuiyugu_generate(self.params)

    def get_hdbjtj(self):
        if self.context['type'] == 0:
            return ""
        elif self.context['type'] == 1:
            return ""
        elif self.context['type'] == 2:
            return ""
        elif self.context['type'] == 3:
            hdbjtj = shj_hedaobijian_context(self.params)
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="安全举措", content=hdbjtj, ctype=1)
            self.node.wordParagraphs.add(wp)
            return hdbjtj
    def get_ddyz_ddmb(self):
        if self.context['type'] == 0:
            return ""
        elif self.context['type'] == 1:
            return ""
        elif self.context['type'] == 2:
            return ""
        elif self.context['type'] == 3:
            ddyz_ddmb = "以《中华人民共和国黄河保护法》《黄河流域生态保护和高质量发展规划纲要》为指导，遵循安全可控、统筹兼顾的原则，结合下游抗旱供水和中游水库腾库迎汛要求，科学调度三门峡、小浪底水库，实现保障抗旱用水安全、腾库迎汛、维持下游河道中水河槽过流能力和持续改善河口生态等目标，发挥水资源综合效益。"
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="调度原则和调度目标", content=ddyz_ddmb, ctype=1)
            self.node.wordParagraphs.add(wp)
            return ddyz_ddmb
    def get_ysgxq(self):
        if self.context['type'] == 0:
            # 黄河中下游的河道水情
            #TODO
            # logger.debug("self.params:",   self.params)
            # logger.debug("type(self.params):",type(self.params))
            tmp = huanghe_yuqing_generate(self.params)
            ## 对每段描述内容进行细分
            wp = WordParagraph.objects.create(title="雨情实况", content=tmp, ctype=1)
            # self.node.wordParagraphs.clear()
            for n in self.node.wordParagraphs.all():
                n.delete()
            self.node.wordParagraphs.add(wp)
            return tmp
            # return ""
        elif self.context['type'] == 1 or self.context['type'] == 2:
            # 小浪底河道水情
            #TODO
            #tmp = huanghe_yuqing_generate(self.params)
            tmp = xld_yushui_context(self.params)
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="雨情实况", content=tmp, ctype=1)
            self.node.wordParagraphs.add(wp)
            return xld_yushui_context(self.params)
        elif self.context['type'] == 3:
           return ""
        elif self.context['type'] == 4:
            #ylh_yuqing = yiluohe_yuqing_generate(self.params)
            ylh_yuqing = self.params["yuqing"]
            hdsq = huanghe_hedaoshuiqing_generate(self.params)
            sksq = huanghe_shuikushuiqing_generate(self.params)
#            gqxq = huanghe_gongqing_generate_html(self.params)
            gqxq = self.params['xianqing']
            # 返回网页表格数据
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title="雨情实况", content="雨情", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="雨情实况描述", content=ylh_yuqing, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="雨情实况", content="河道水情", ctype=1)
            self.node.wordParagraphs.add(wp)
            df = pd.DataFrame(self.params['hdsq'])
            hdsq_json = df.to_json(orient='records')
            wp = WordParagraph.objects.create(title="河道水情表格", content=json.dumps(hdsq_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="雨情实况", content="水库水情", ctype=1)
            self.node.wordParagraphs.add(wp)
            df = pd.DataFrame(self.params['sksq'])
            sksq_json = df.to_json(orient='records')
            wp = WordParagraph.objects.create(title="水库水情表格", content=json.dumps(sksq_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="雨情实况", content="工情险情", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="工情险情描述", content=gqxq, ctype=1)
            self.node.wordParagraphs.add(wp)
            return bold_left_align("雨情")+"\n"+ylh_yuqing+bold_left_align("水情")+"\n"+bold_left_align("河道水情")+divHtml(f"黄河主要站点流量表\n") + hdsq+ bold_left_align("水库水情")+ divHtml(f"黄河主要水库蓄水情况表\n") + sksq +bold_left_align("工情险情") + gqxq

    def make_context(self,):
        # logger.debug("make_context:", self.context, self.params)
        label = self.node.label
        logger.debug(f"label: {label}")
        #label = map_input_to_label(user_input=label)
        if label == "雨情实况" or label =="实时雨水情":
            logger.debug("雨情实况 get_ysq")
            result = self.get_ysq()
        elif label == "河道水情":
            logger.debug("河道水情 get_hdsq")
            result = self.get_hdsq()
        elif label == "水库水情":
            logger.debug("水库水情 get_sksq")
            result = self.get_sksq()
        elif label == "工情险情实况" or label == "工情险情":
            logger.debug("工情险情实况 get_gqxq")
            result = self.get_gqxq() #ori_ctx
        elif label == "降雨预报" or label == "预报":
            logger.debug("降雨预报 get_jyyb")
            result = self.get_jyyb()
        elif label == "洪水预报":
            logger.debug("洪水预报 get_hsyb")
            result = self.get_hsyb()
        elif label == "调度方案" or label == "水库调度方案":
            logger.debug("调度方案 get_ddfa")
            result = self.get_ddfa()
        elif label == "调度结果" or label == "调度结果及应对措施":
            logger.debug("调度结果 get_ddjg")
            result = self.get_ddjg()
        elif label =="工程研判":
            logger.debug("工程研判 get_gcyp")
            result = self.get_gcyp()
        elif label =="枢纽运用方案":
            logger.debug("枢纽运用方案 get_snyy")
            result = self.get_snyy()
        elif label == "安全举措" or label =="防御措施":
            logger.debug("安全举措 get_aqjc")
            result = self.get_aqjc()
        elif label == "来水预估":
            logger.debug("安全举措 get_lsyg")
            result = self.get_lsyg()
        elif label =="河道边界条件":
            logger.debug("河道边界条件 get_hdbjtj")
            result = self.get_hdbjtj()
        elif label == "调度原则和调度目标":
            logger.debug("调度原则和调度目标 get_ddyz_ddmb")
            result = self.get_ddyz_ddmb()
        elif label == "实时雨水工险情":
            logger.debug("雨水工险情 get_ysgxq")
            result =self.get_ysgxq()
        else: 
            result = generate_description_for_label(label)
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title=label, content=f"\n{result}", ctype=1)
            self.node.wordParagraphs.add(wp)
        self.node.result = result
        self.node.save()
        # logger.debug("make ctt result:", result)
