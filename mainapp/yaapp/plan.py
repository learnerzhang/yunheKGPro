import json
from yaapp import yautils
from yaapp import divHtml, gx_sk, hkc_sk, img2base64, lhbs_sk, paraHtml, smx_sjt_sk, xld_sk, generate_ddjy, process_outflow,bold_left_align,pd2HtmlCSS,excel_to_html_with_merged_cells,generate_rainfall_report,get_rainfall_data_day,format_hydrometric_data,format_reservoir_data
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

        self.yadate = self.context['yadate']
        self.yatype = self.context['type']
        self.ddfa_excel = os.path.join("data", "yuan_data", f"{self.yatype}", "ddfad", f"{self.yadate}.xlsx")
        # logger.debug(ddfa_excel)
        if not os.path.exists(self.ddfa_excel):
            self.ddfa_excel = os.path.join("data", "yuan_data", "4", "ddfad", "default.xlsx")
            logger.info(f"当天调度方案单不存在,采用默认调度方案单 {self.ddfa_excel}")
        else:
            logger.info(f"存在{self.ddfa_excel}调度方案单")
        self.skMapData, self.swMapData, self.date_list = yautils.excel_to_dict(self.ddfa_excel)
        logger.info("水库站点数据： %s "% self.skMapData.keys())
        logger.info("水文站点数据： %s "% self.swMapData.keys())
        logger.info("日期列表数量： %s "% len(self.date_list))
        logger.info("FC DONE!")

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

    def get_jyyb_api(self):
        if self.context['type'] == 4:
            jyyb_desc = self.params['jyyb_desc'] if 'jyyb_desc' in self.params else "暂无降雨信息"
            self.context['results']['jyyb_desc'] = {
                "value": jyyb_desc,
                "desc": "降雨预报总览信息"
            }

            jyyb_imgs = self.params['jyyb_imgs'] if 'jyyb_imgs' in self.params else []
            for imgent in jyyb_imgs:
                imgent['urlpath'] = f"data/yuan_data/{self.context['type']}/yubao/{self.context['yadate']}/{imgent['url']}"
            
            self.context['results']['jyyb_imgs'] = {
                "value": jyyb_imgs,
                "desc": "N天的降雨预报图"
            }

            ylhjyyb = self.params['ylhjyyb'] if 'ylhjyyb' in self.params else []
            self.context['results']['fenquyubao'] = {
                "value": ylhjyyb,
                "desc": "分区的降雨预报"
            }

            qjsyj = self.params['qjsyj'] if 'qjsyj' in self.params else "暂无强降雨预报信息"
            self.context['results']['qiangjiangyuyubao'] = {
                "value": qjsyj,
                "desc": "强降雨预报信息"
            }

            self.context['results']['future7dayspredict'] = {
                "value": [],
                "desc": "未来7天径流预报"
            }

            hhfloodforecast = self.params['hhfloodforecast'] if 'hhfloodforecast' in self.params else []
            self.context['results']['future7daysavgpredict'] = {
                "value": hhfloodforecast,
                "desc": "未来7天均流预报"
            }


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
                ddfa_excel = os.path.join("data", "yuan_data", "4", "ddfad", "default.xlsx")
                logger.info(f"当天调度方案单不存在,采用默认调度方案单 {ddfa_excel}")
                yautils.plot_save_html(ddfa_excel, business_type=4, myDate=yadate)
                logger.info(f"{yadate}调度方案单绘制图片")
            else:
                logger.info(f"{yadate}调度方案单已存在")

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
                    logger.warning(f"调度过程曲线不存在：{tmpimgpath}")
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
                    logger.warning(f"调度过程曲线不存在：{tmpimgpath}")
                    continue
                sw2image[swname] = tmpimgpath
                tmp_ddgc_img = img2base64(tmpimgpath)
                sw2image[swname] = tmp_ddgc_img
                tmp_ddgc_img_desc = f"{swname}调度过程({date_list[0]}~{date_list[-1]})"
                tmp_result = f"预计{max_date}，{swname}出现{max_ll}立方米每秒的洪峰流量\n"
                hd_result += paraHtml(tmp_result) + divHtml(
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

    def get_ddjg_api(self):
        if self.context['type'] == 4:
            # 伊洛河
            import pandas as pd
            import time
            yadate = self.context['plan']['yadate']
            ddfa_excel = os.path.join("data", "yuan_data", "4", "ddfad", f"{yadate}.xlsx")
            # logger.debug(ddfa_excel)
            if not os.path.exists(ddfa_excel):
                ddfa_excel = os.path.join("data", "yuan_data", "4", "ddfad", "default.xlsx")
                logger.info(f"当天调度方案单不存在,采用默认调度方案单 {ddfa_excel}")
            else:
                logger.info(f"存在{ddfa_excel}调度方案单")
            
            skMapData, swMapData, date_list = yautils.excel_to_dict(ddfa_excel)
            ## 根据调度方案生成水库运作方式
            results = yautils.skddjy_new(ddfa_excel)
            # 初始化调度建议字符串
            ddjy_list = []
            # 遍历返回的结果字典
            for key, value in results.items():
                ckll = process_outflow(value, date_list)
                #ddjy_list.append(f"{key}水库：{ckll}")
                ddjy_list.append([key, ckll])
            # 按照《黄河洪水调度方案》确定的水库群分级调度规则，建议中游五库调度原则如下
            self.context['results']['ddyyfs'] = {
                "baserule": "按照《黄河洪水调度方案》确定的水库群分级调度规则，建议中游五库调度原则如下",
                "value": ddjy_list,
                "desc": "调度应用方式描述"
            }

            skMapDesc = {}
            swMapDesc = {}
            for sk, record in skMapData.items():
                keys = list(record.keys())
                if "水位" not in keys:
                    continue
                swdata = list(record["水位"])
                max_sw = max(swdata)
                max_idx = swdata.index(max_sw)
                max_date = date_list[max_idx]
                max_sw = round(max_sw, 2)
                tmp_desc_result = f"预计{sk}将于{max_date}达到最高水位{max_sw}m;"
                skMapDesc[sk] = tmp_desc_result

            hyk_liuliang = 3000
            for sw, lldata in swMapData.items():
                max_ll = round(max(lldata), 2)
                max_idx = lldata.index(max_ll)
                max_date = date_list[max_idx]
                max_ll = round(max_ll, 2)
                if sw == '花园口':
                    hyk_liuliang = max_ll
                tmp_result = f"预计{max_date}，{sw}出现{max_ll}立方米每秒的洪峰流量\n"
                swMapDesc[sw] = tmp_result

            self.context['results']['sk_ddgc'] = {
                "value":{
                    "data_list": date_list,
                    "sk_map_data": skMapData,
                    'sk_map_desc': skMapDesc,
                },
                "desc": "水库的调度过程曲线"
            }

            self.context['results']['hd_ddgc'] = {
                "value":{
                    "data_list": date_list,
                    "hd_map_data": swMapData,
                    'sw_map_desc': swMapDesc,
                },
                "desc": "河道的调度过程曲线"
            }

            self.context['results']['ddfad_path'] = {
                "value": ddfa_excel,
                "desc": "调度方案url位置"
            }

            tqym = '根据<span class="hn">《河南省黄河滩区运用预案》</span>、<span class="sd">《山东省黄河滩区运用预案》</span>，'  + tanquyanmo(hyk_liuliang, usetag=True)["result"]
            self.context['results']['tanquyanmo'] = {
                "value": tqym,
                "desc": "滩区淹没"
            }


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
            # 获取各段预警等级
            hh_res = hh_yujingdengji(lh_sw=317.5)
            ylh_res = ylh_yujingdengji(bms_ll=4000)
            gx_res = gx_yujingdengji(ls_ll=7450)
            lh_res = lh_yujingdengji(lh_ll=5622)

            # 找出最高预警等级（数字最小的）
            all_levels = [hh_res["level"], ylh_res["level"], gx_res["level"], lh_res["level"]]
            final_level = min(all_levels)

            # 确定最终应对措施
            if final_level == hh_res["level"]:
                final_measures = hh_res["result"]
            elif final_level == ylh_res["level"]:
                final_measures = ylh_res["result"]
            elif final_level == gx_res["level"]:
                final_measures = gx_res["result"]
            else:
                final_measures = lh_res["result"]
            # 如果需要合并所有措施（不推荐简单拼接）
            # final_measures = "\n".join([hh_res["result"], ylh_res["result"], ...])
            # 最终结果
            yjdj = final_level
            ydcs = final_measures
            sx_ydcs = sx_yujingdengji(lh_sw=323)["result"]
            ydcs += sx_ydcs
            df = pd.DataFrame(self.params["goodsTable"])
            fxwz = pd2HtmlCSS() + df.to_html(index=False)
            if yjdj == 1:
                final_level = "一级预警"
            elif yjdj == 2:
                final_level = "二级预警"
            elif yjdj == 3:
                final_level = "三级预警"
            elif yjdj == 4:
                final_level = "四级预警"
            elif yjdj == 5:
                final_level = "无预警"
            else:
                final_level = "无预警"  # 处理意外输入
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="预警分级响应", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"预警等级", content=final_level, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="应对措施", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"应对措施", content=ydcs, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="人员转移方案", ctype=1)
            self.node.wordParagraphs.add(wp)
            ryzyfa = ("根据《故县水库卢氏库区汛期高水位运用应急预案>>统计库区转移人口,供调度参考,具体转移方案见水库库区汛期高水位运用部分；\n"
                      "水库下游根据《故县水库抗险应急预案》具体转移方案由地方政府制定并组织实施，尽量减少损失。故县水库下游共有洛宁县、宜阳县、洛阳城区、偃师和巩义")
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content=ryzyfa, ctype=1)
            self.node.wordParagraphs.add(wp)
            zzbz= "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责。\n  为保证故县水库抢险应急工作落实，故县水利枢纽管理局(以下简称“故县局”)设立防汛指挥部，在黄河水利委员会(以下简称“黄委”)、洛阳市防汛抗旱指挥部(以下简称“洛阳市防指”)的领导下，统一组织、指挥、协调、指导和督促全局防."
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="组织保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"组织保障", content=zzbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"组织保障", content="\t\t\t陆浑水库防汛指挥部领导成员责任人及联系方式", ctype=1)
            self.node.wordParagraphs.add(wp)
            zzbz_json = pd.DataFrame(self.params["zzbzTable"]).to_json(orient="records")
            wp = WordParagraph.objects.create(title=f"组织保障表", content=json.dumps(zzbz_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            dwbz = "\t陆浑水库汛期常设防汛巡逻队和水库处职工一起，主要负责险情巡查报告工作，并协助水库应急抢险专家组，做好抢险技术指导工作。\n\t人民解放军洛阳驻军部队是水库应急抢险的主力军嵩具和伊川人武部地方基干民兵是水库应急抢险的骨干和后备军，主要负责水库防汛抢险工作，同时也要协助地方政府做好下游危险区域人员和财产的应急转移安置工作及转移后的警戒工作。\n\t陆浑水库的防汛抢险实行军民联防制，以部队为主力，地方基干民兵为骨干，在陆浑水库防汛指挥部的统一领导下和水库职工一起，同心同德、众志成城，确保水库安全度汛。拟定部队官兵300名，嵩县民兵1200人，伊川县抢险后备队1000人，共计2500人，参加防汛抢险人员于每年6月10日完成编队造册，做到官民官兵相识，并报到陆浑水库防汛指挥部办公室，随时听调。防汛抢险人员调动安排由水库防指统一指挥。"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="队伍保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"队伍保障", content=dwbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            dwbz_json = pd.DataFrame(self.params["dwbzTable"]).to_json(orient="records")
            wp = WordParagraph.objects.create(title=f"队伍保障表", content=json.dumps(dwbz_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            wuzi_json = pd.DataFrame(self.params["goodsTable"]).to_json(orient="records")
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="物资保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"物资保障", content=json.dumps(wuzi_json),ctype=3)
            self.node.wordParagraphs.add(wp)
            jsbz = "\t黄委及洛阳市防指建立有防汛抢险专家库。当故县水库发生大洪水灾害时，由黄委及洛阳市防指负责防洪抢险及迁安救护统一调度，并派出专家组，指导故县水库防洪抢险及迁安救护工作。"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="技术保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"技术保障", content=jsbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            jsbz_json = pd.DataFrame(self.params["jsbzTable"]).to_json(orient="records")
            wp = WordParagraph.objects.create(title=f"技术保障表", content=json.dumps(jsbz_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            txbz = ("\t陆浑水库现有三条对外通讯途径:其一，从田湖向水库防汛值班室接单机电话，可通过嵩县网通对外通话，但受外界干扰较大，保证率不高。其二，从水库陆浑通讯站到洛阳和郑州(黄委)的程控电话。其三，水库与运行中心机关，配有防汛5部专用移动卫星手机电话，确保联系畅通。"
                    "\n\t故县水库工程通信系统主要由黄河防汛专网、联通公司公网、公共移动通信网络、卫星通信电话和故县局内通信网构成。正常情况下，可以满足防汛抢险工作要求。\n防汛专网"
                    "\n\t通过洛--故微波通道上联至三门峡黄河明珠集团有限公司(以下简称“明珠集团”)局域网并接入黄委办公网，分别实现黄委政务内网访问与黄委内部语音接入，并实现遥测系统雨水情数据信息传递、上级指令的传达以及内网的日常办公。\n 联通公司公用通讯网"
                    "\n\t已从洛宁县故县镇电信所接入多部外线电话和中继线，分别装于故县局主要部门及电话总机机房。\n公共移动通信网络"
                    "\n\t本辖区有移动公司、电信公司和联通公司的手机通信基站，手机信号已覆盖大部分办公场所，其中移动公司在大坝附近设置有手机信号放大器，对大坝和电厂的信号覆盖要好于其它通信公司。目前移动通信基站的供电有一些单薄，需要时刻关注，必要时提供帮助。\n卫星通信电话"
                    "\n\t目前故县局有3台手持式卫星电话，能确保与黄委、国家防御局进行通信。")
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="通信保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"通信保障", content=txbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            self.node.wordParagraphs.add(wp)
            txbz_json = pd.DataFrame(self.params["txbzTable"]).to_json(orient="records")
            wp = WordParagraph.objects.create(title=f"技术保障表", content=json.dumps(txbz_json), ctype=3)
            self.node.wordParagraphs.add(wp)
            zmyjbz = "\t陆浑水库防汛照明系统有:(一)沿防汛公路照明系故县局目前储备有室外移动式汽油发电机、电缆、照明灯具统:共有照明灯具92个，功率为250W;（二)坝顶明灯具，东西坝头高杆灯2个，东坝头功率为2000W，西坝头可满足室外应急照明。小型发动机、柴油(或汽油)功率为14~400W;(三)大坝背水坡面320平台东西发电机组存二坝肩高杆灯2个，东坝肩功率为8~400W，_西坝肩功放时，应分类、分规格摆放整齐，铭牌朝外，存放在底层。功率为2*2000W;(四)溢洪道闸墩照明灯具2个，功率为400W;(五)泄洪洞交通桥照明灯具2个功率为400W;(六)防汛仓库便携式工作灯55个，投光灯4只。"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="照明应急保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"照明应急保障", content=zmyjbz , ctype=1)
            self.node.wordParagraphs.add(wp)
            aqbz = ("\t故县局成立安全生产管理委员会，构成故县局安全生产管理领导机构，对故县局安全生产工作进行管理决策。建立安全生产管理网络，开展故县局安全生产管理工作，各单位、分场、班组三级专(兼)职安全管理人员，构成本单位三级安全生产管理网络，担负各自职责范围内的安全生产管理责任，开展本单位安全生产管理工作。"
                    "\n\t各单位主要负责人对本单位安全生产工作负全面领导责任;分管安全生产的负责人对本单位安全生产工作负综合监管领导责任;工程管理处负安全技术责任;分管其它业务的行政副职和各职能部门，对分管业务范围内的安全生产工作负直接领导责任;职工对所从事岗位的安全生产工作负责。"
                    "\n\t深入开展事故隐患排查治理，消除各类安全生产事故隐患通过定期、不定期及专项等各种形式安全检查，排查各类安全隐患，落实整改，及时纠正各种不安全现象和行为，有效的控制和预防安全事故的发生;持续推进双重预防体系建设，对设备、设")
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="安全保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"安全保障", content=aqbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            wsbz = ("\t水库防汛工作与卫生保障密切相关，必须统筹推进以确保安全度汛和公众健康。在防汛方面，要严格落实责任制，加强大坝、泄洪设施和水位监测系统的巡查维护，科学调度库容并严格执行汛限水位管控，同时完善应急预案，强化24小时值守和抢险演练。在卫生保障方面，需重点防范汛期可能引发的水源污染和传染病风险，加强水质监测和饮用水安全保护，做好洪水退后的环境消杀和病媒生物防治，配备应急医疗力量并储备防疫物资，同时向群众普及汛期卫生防病知识。只有将防汛抢险与卫生防控有机结合，构建从灾害预警到应急处置的全链条防护体系，才能有效降低洪涝灾害对人民群众生命健康和经济社会发展的影响。")
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="卫生保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"卫生保障", content=wsbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            qtbz = ("（1）现场救援和工程抢险保障\n\t当出现新的险情后，应派工程技术人员赶赴现场，研究优化除险方案，并由行政首长负责组织实施。洛阳市防指和故县局防指以及受洪水威胁的其他单位，储备的常规抢险机械、抗旱设备、物资和救生器材，能满足抢险急需\n"
                    "(2) 交通运输保障\n\t故县局通往外界的交通有水陆两种方式。\n\t若故县至郑卢高速路中断，要及时向地方防汛指挥部反映;若短时问不能抢修通行时，可由故县至杜河的“村村通”公路和故县至兴华镇省道或利用水库水面交通工具通过卢氏县运输防汛物咨和抢险人员、也可以用车辆倒坛工作人员经过道路塌方段，及时让抢险人员到达工作岗位。"
                    "\n(3) 治安保障\n\t  洛阳市及所辖公安部门负贵做好故县水库有关灾区的治安管理工作，依法严厉打击破坏抗洪抢险行动和工程设施安全的行为，保证抗灾救灾工作的顺利进行;负责组织搞好防洪抢险的戒严、警卫工作。故县局库区管理分局和洛河发电公司负责故县水库抗洪抢险的治安管理和安全保卫工作。\n(4)供电保障"
                    "\n\t故县水库防汛电源有三种方式保障:一是10kv电网系统正常供电，二是电厂厂用电 400v系统备用供电，三是备用发电机。")
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="其他保障", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"其他保障", content=qtbz, ctype=1)
            self.node.wordParagraphs.add(wp)
            xcyy = "\t故县水库汛情、工情、险情、灾情及防洪抢险工作等方面的公众信息交流，实行分级负责制，一般公众信息由洛阳市防指负责同志审批后，可通过媒体向社会发布。故县局内部根据需要可通过电话、手机短信、微信群和办公自动化网络等形式发布，当洛河发生超警戒水位以上洪水，呈上涨趋势;山区发生暴雨山洪，造成较为严重影响，按分管权限，由洛阳市防指统一发布汛情、险情通报，以引起社会公众关注，参与防洪抢险工作。"
            wp = WordParagraph.objects.create(title=f"调度结果及应对措施", content="宣传和卫生演练", ctype=1)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title=f"宣传和卫生演练", content=xcyy, ctype=1)
            self.node.wordParagraphs.add(wp)
        return bold_left_align("预警分级响应") + str(yjdj)+"级预警"+bold_left_align("应对措施") + ydcs +bold_left_align("应急保障") +bold_left_align("组织保障")+zzbz+bold_left_align("队伍保障")+dwbz+bold_left_align("物资保障")+fxwz+bold_left_align("技术保障")+jsbz+bold_left_align("通信保障")+txbz+bold_left_align("照明应急保障")+zmyjbz+bold_left_align("安全保障")+aqbz+bold_left_align("卫生保障")+wsbz+bold_left_align("其他保障")+qtbz+bold_left_align("宣传和卫生演练")+xcyy
    

    def yjdj_api(self):
        yjdj = yujingdengji()["level"]  # "黄色预警"

        
        hdsq = self.params["hdsq"] if "hdsq" in self.params else []
        sksq = self.params["sksq"] if "sksq" in self.params else []
        sk2RealData = {ent['水库名称']: ent for ent in sksq}
        sw2RealData = {ent['站名']: ent for ent in hdsq}
        tmpskdesc = {}
        tmpswdesc = {}
        for sk, skData in self.skMapData.items():
            max_index = skData['水位'].index(max(skData['水位']))
            max_data = skData['水位'][max_index]
            max_time = self.date_list[max_index]
            tmpskdesc[sk] = {
                'sw': sk2RealData[sk]['水位（m）'],
                'max_sw': max_data,
                'max_time': max_time,
            } if sk in sk2RealData else {}
        for sw, swData in self.swMapData.items():
            max_index = swData.index(max(swData))
            max_data = swData[max_index]
            max_time = self.date_list[max_index]
            tmpswdesc[sw] = {
                'll': sw2RealData[sw]['流量(m³/s)'],
                'max_ll': max_data,
                'max_time': max_time,
            } if sw in sw2RealData else {}

        def dateformat(date_str):
            # 将字符串解析为datetime对象
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            # 格式化为月日格式
            new_date_str = date_obj.strftime("%m月%d日")
            return new_date_str

        yjdj =  f"陆浑水库当前水位({round(tmpskdesc['陆浑']['sw'], 2)}米，预计在{dateformat(tmpskdesc['陆浑']['max_time'])}达到最高水位{round(tmpskdesc['陆浑']['max_sw'], 2)}米，"\
                f"故县水库当前水位{tmpskdesc['故县']['sw']}米，预计在{dateformat(tmpskdesc['故县']['max_time'])}日达到最高水位{round(tmpskdesc['故县']['max_sw'], 2)}米。"\
                f"龙门镇水文站当前流量{round(tmpswdesc['龙门镇']['ll'], 2) if 'll' in tmpswdesc['龙门镇'] and tmpswdesc['龙门镇']['ll'] else '-' }m3/s，预计{dateformat(tmpswdesc['龙门镇']['max_time']) if 'max_time' in tmpswdesc['龙门镇'] else '-'}达到最大流量{round(tmpswdesc['龙门镇']['max_ll'] ) if 'max_ll' in tmpswdesc['龙门镇'] else '-'}m3/s,"\
                f"白马寺水文站当前流量{round(tmpswdesc['白马寺']['ll']) if 'll' in tmpswdesc['白马寺'] else '-'}m3/s、预计在{dateformat(tmpswdesc['白马寺']['max_time']) if 'max_time' in tmpswdesc['白马寺'] else '-'}达到{round(tmpswdesc['白马寺']['max_ll'], 2) if 'max_ll' in tmpswdesc['白马寺'] else '-'}m3/s,"\
                f"建议按照《黄河防汛抗旱应急预案（试行）》启动Ⅰ级应急响；按照《陆浑水库2024年防汛抢险应急预案》启动Ⅲ级应急响应；按照《故县水库应急抢险预案》启动Ⅲ级应急响应、《故县水库卢氏库区汛期高水位运用应急预案》启动Ⅰ级应急响应."

        self.context['results']['yuyingfenji'] = {
            "value": yjdj,
            "desc": "预警分级响应"
        }
        ydcs = yujingdengji(lh_sw=tmpskdesc['陆浑']['max_sw'], 
                            gx_sw=tmpskdesc['故县']['max_sw'],
                            lm_ll=tmpswdesc['龙门镇']['max_ll'],
                            act_flag=True, lev='Ⅰ'
                            )["result"]
        self.context['results']['yingducuoshi'] = {
            "value": ydcs,
            "desc": "应对措施"
        }
    def get_aqjc_api(self):
        if self.context['type'] == 4:
            self.yjdj_api()

            ryzq = self.params['ryzyfa'] if 'ryzyfa' in self.params else []
            self.context['results']['renyuanzhuanyi'] = {
                "ryzq": ryzq,
                "desc": "人员转移方案"
            }
            zzbz = "故县水库行政责任人:洛阳市委常委，常务副市长\n职责:负贵故县水库大坝安全然管领导责任，统 指泽故县水车防讯抗早、拍险救灾工作，协调指导解决故县水库大规安全管理的重大问题，组织面大实发事件和安全事故的应急处置，负责放县水库应食拾险和于安救护工作，督促水库主管部门责任人、技术责任人、巡查责任人履行工作职责,"
            dwbz = "陆浑水库汛期常设防汛巡逻队和水库处职工一起，主要负责险情巡查报告工作，并协助水库应急抢险专家组，做好抢险技术指导工作。\n\t人民解放军洛阳驻军部队是水库应急抢险的主力军嵩具和伊川人武部地方基干民兵是水库应急抢险的骨干和后备军，主要负责水库防汛抢险工作，同时也要协助地方政府做好下游危险区域人员和财产的应急转移安置工作及转移后的警戒工作。\n\t陆浑水库的防汛抢险实行军民联防制，以部队为主力，地方基干民兵为骨干，在陆浑水库防汛指挥部的统一领导下和水库职工一起，同心同德、众志成城，确保水库安全度汛。拟定部队官兵300名，嵩县民兵1200人，伊川县抢险后备队1000人，共计2500人，参加防汛抢险人员于每年6月10日完成编队造册，做到官民官兵相识，并报到陆浑水库防汛指挥部办公室，随时听调。防汛抢险人员调动安排由水库防指统一指挥。"
            wzbz = self.params["goodsTable"] if 'goodsTable' in self.params else []
            jsbz = "黄委及洛阳市防指建立有防汛抢险专家库。当故县水库发生大洪水灾害时，由黄委及洛阳市防指负责防洪抢险及迁安救护统一调度，并派出专家组，指导故县水库防洪抢险及迁安救护工作。"
            txbz = ("陆浑水库现有三条对外通讯途径:其一，从田湖向水库防汛值班室接单机电话，可通过嵩县网通对外通话，但受外界干扰较大，保证率不高。其二，从水库陆浑通讯站到洛阳和郑州(黄委)的程控电话。其三，水库与运行中心机关，配有防汛5部专用移动卫星手机电话，确保联系畅通。"
                    "\n故县水库工程通信系统主要由黄河防汛专网、联通公司公网、公共移动通信网络、卫星通信电话和故县局内通信网构成。正常情况下，可以满足防汛抢险工作要求。\n防汛专网"
                    "\n通过洛--故微波通道上联至三门峡黄河明珠集团有限公司(以下简称“明珠集团”)局域网并接入黄委办公网，分别实现黄委政务内网访问与黄委内部语音接入，并实现遥测系统雨水情数据信息传递、上级指令的传达以及内网的日常办公。\n 联通公司公用通讯网"
                    "\n已从洛宁县故县镇电信所接入多部外线电话和中继线，分别装于故县局主要部门及电话总机机房。\n公共移动通信网络"
                    "\n本辖区有移动公司、电信公司和联通公司的手机通信基站，手机信号已覆盖大部分办公场所，其中移动公司在大坝附近设置有手机信号放大器，对大坝和电厂的信号覆盖要好于其它通信公司。目前移动通信基站的供电有一些单薄，需要时刻关注，必要时提供帮助。\n卫星通信电话"
                    "\n目前故县局有3台手持式卫星电话，能确保与黄委、国家防御局进行通信。")
            zmyjbz = "陆浑水库防汛照明系统有:(一)沿防汛公路照明系故县局目前储备有室外移动式汽油发电机、电缆、照明灯具统:共有照明灯具92个，功率为250W;（二)坝顶明灯具，东西坝头高杆灯2个，东坝头功率为2000W，西坝头可满足室外应急照明。小型发动机、柴油(或汽油)功率为14~400W;(三)大坝背水坡面320平台东西发电机组存二坝肩高杆灯2个，东坝肩功率为8~400W，_西坝肩功放时，应分类、分规格摆放整齐，铭牌朝外，存放在底层。功率为2*2000W;(四)溢洪道闸墩照明灯具2个，功率为400W;(五)泄洪洞交通桥照明灯具2个功率为400W;(六)防汛仓库便携式工作灯55个，投光灯4只。"
            aqbz = ("故县局成立安全生产管理委员会，构成故县局安全生产管理领导机构，对故县局安全生产工作进行管理决策。建立安全生产管理网络，开展故县局安全生产管理工作，各单位、分场、班组三级专(兼)职安全管理人员，构成本单位三级安全生产管理网络，担负各自职责范围内的安全生产管理责任，开展本单位安全生产管理工作。"
                    "\n各单位主要负责人对本单位安全生产工作负全面领导责任;分管安全生产的负责人对本单位安全生产工作负综合监管领导责任;工程管理处负安全技术责任;分管其它业务的行政副职和各职能部门，对分管业务范围内的安全生产工作负直接领导责任;职工对所从事岗位的安全生产工作负责。"
                    "\n深入开展事故隐患排查治理，消除各类安全生产事故隐患通过定期、不定期及专项等各种形式安全检查，排查各类安全隐患，落实整改，及时纠正各种不安全现象和行为，有效的控制和预防安全事故的发生;持续推进双重预防体系建设，对设备、设")
            
            wsbz = ("水库防汛工作与卫生保障密切相关，必须统筹推进以确保安全度汛和公众健康。在防汛方面，要严格落实责任制，加强大坝、泄洪设施和水位监测系统的巡查维护，科学调度库容并严格执行汛限水位管控，同时完善应急预案，强化24小时值守和抢险演练。在卫生保障方面，需重点防范汛期可能引发的水源污染和传染病风险，加强水质监测和饮用水安全保护，做好洪水退后的环境消杀和病媒生物防治，配备应急医疗力量并储备防疫物资，同时向群众普及汛期卫生防病知识。只有将防汛抢险与卫生防控有机结合，构建从灾害预警到应急处置的全链条防护体系，才能有效降低洪涝灾害对人民群众生命健康和经济社会发展的影响。")
            
            qtbz = ("（1）现场救援和工程抢险保障\n\t当出现新的险情后，应派工程技术人员赶赴现场，研究优化除险方案，并由行政首长负责组织实施。洛阳市防指和故县局防指以及受洪水威胁的其他单位，储备的常规抢险机械、抗旱设备、物资和救生器材，能满足抢险急需\n"
                    "(2) 交通运输保障\n\t故县局通往外界的交通有水陆两种方式。\n\t若故县至郑卢高速路中断，要及时向地方防汛指挥部反映;若短时问不能抢修通行时，可由故县至杜河的“村村通”公路和故县至兴华镇省道或利用水库水面交通工具通过卢氏县运输防汛物咨和抢险人员、也可以用车辆倒坛工作人员经过道路塌方段，及时让抢险人员到达工作岗位。"
                    "\n(3) 治安保障\n\t  洛阳市及所辖公安部门负贵做好故县水库有关灾区的治安管理工作，依法严厉打击破坏抗洪抢险行动和工程设施安全的行为，保证抗灾救灾工作的顺利进行;负责组织搞好防洪抢险的戒严、警卫工作。故县局库区管理分局和洛河发电公司负责故县水库抗洪抢险的治安管理和安全保卫工作。\n(4)供电保障"
                    "\n\t故县水库防汛电源有三种方式保障:一是10kv电网系统正常供电，二是电厂厂用电 400v系统备用供电，三是备用发电机。")
            self.context['results']['yingjibaozhang'] = {
                "value": {
                    'zzbz': zzbz,
                    'zzbzTable': self.params["zzbzTable"] if 'zzbzTable' in self.params else [],
                    'dwbz': dwbz,
                    'dwbzTable': self.params["dwbzTable"] if 'dwbzTable' in self.params else [],
                    'wzbz': wzbz,
                    'jsbz': jsbz,
                    'jsbzTable': self.params["jsbzTable"] if 'jsbzTable' in self.params else [],
                    'txbz': txbz,
                    'txbzTable': self.params["txbzTable"] if 'txbzTable' in self.params else [],
                    'zmyjbz': zmyjbz,
                    'aqbz': aqbz,
                    'wsbz': wsbz,
                    'qtbz': qtbz,
                },
                "desc": "应急保障"
            }
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
            #gqxq = huanghe_gongqing_generate_html(self.params)
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


    def get_ysgxq_api(self):
        if self.context['type'] == 4:
            #ylh_yuqing = yiluohe_yuqing_generate(self.params)
            ylh_yuqing = self.params["yuqing"] if 'yuqing' in self.params else "暂无雨情数据"
            # status, data = get_rainfall_data_day()
            # ylh_yuqing = generate_rainfall_report(data)
            self.context['results']['yuqing'] = {
                "value": ylh_yuqing,
                "desc": "伊洛河区域雨情数据"
            }
            # code, res = format_hydrometric_data()
            # hdsq = res["hdsq"]
            # res = format_reservoir_data()
            # sksq = res["sksq"]
            hdsq = self.params['hdsq'] if self.params else []
            sksq = self.params['sksq'] if self.params else []

            self.context['results']['shuiqing'] = {
                "hdsq":{
                    "value": hdsq,
                    "desc": "伊洛河区域河道水情"
                },
                "sksq":{
                    "value": sksq,
                    "desc": "伊洛河区域水库水情"
                }
            }
#            gqxq = huanghe_gongqing_generate_html(self.params)
            gqxq = self.params['xianqing']
            self.context['results']['xianqing'] = {
                "value": gqxq,
                "desc": "伊洛河区域险情描述"
            }


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
            logger.debug("来水预估 get_lsyg")
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


    def make_context_api(self,):
        label = self.node.label
        logger.info(f"make_context_api label: {label}")
        if label == "实时雨水工险情":
            self.get_ysgxq_api()
        elif label == '预报':
            self.get_jyyb_api()
        elif label == '调度结果':
            self.get_ddjg_api()
        elif label == '防御措施':
            self.get_aqjc_api()