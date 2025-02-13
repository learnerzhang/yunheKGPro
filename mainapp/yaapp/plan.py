import json
from yaapp import divHtml, gx_sk, hkc_sk, img2base64, lhbs_sk, paraHtml, smx_sjt_sk, xld_sk, generate_ddjy
from yaapp.api_yuan import (huanghe_diaodu_plan_ctx, huanghe_diaodu_plan_dfjson, huanghe_hedaoshuiqing_generate_dfjson, huanghe_shuikushuiqing_generate_dfjson, huanghe_yuqing_generate,huanghe_hedaoshuiqing_generate,huanghe_shuikushuiqing_generate,huanghe_gongqing_generate,huanghe_jiangyu13_forecast,huanghe_fenqu_jiangyu_forecast,huanghe_jiangyu47_forecast,huanghe_flood_forecast,huanghe_diaodu_plan,huanghe_shuiku_diaodu_result,huanghe_tanqu_yanmo,huanghe_keneng_danger,huanghe_xiangying_level,xld_yushui_context,
                            engineer_safety_shuikuyj,engineer_safety_shuiwenyj,engineer_safety_gongchengjcyj,shuniuFangAn,xldJZStatus,xldholeStatus,JZHoleRecommend,YingjiResponse,OrganizeBaoZhang_leader,OrganizeBaoZhang_zhihuibu,company_duty,team_baozhang,fangxun_table,xld_diaodu_table,huanghe_fenqu_jiangyu_forecast_json,huanghe_flood_forecast_json,engineer_safety_shuikuyj_json,engineer_safety_shuiwenyj_json,engineer_safety_gongchengjcyj_json,xldJZStatus_json,JZHoleRecommend_json,xldholeStatus_json,
                            OrganizeBaoZhang_leader_json,OrganizeBaoZhang_zhihuibu_json,company_duty_json,team_baozhang_json,fangxun_table_json,xld_diaodu_table_json,huanghe_fenqu_jiangyu_forecast_dfjson,generate_description_for_label,map_input_to_label, huanghe_gongqing_generate_html,huanghe_diaodu_plan_yuanze_ctx,huanghe_diaodu_plan_yuanze_html,huanghe_diaodu_plan_jianyi_ctx,huanghe_diaodu_plan_jianyi_html,shj_yushui_context,shj_shuikuxushui_generate_dfjson,shj_shuikuxushui_generate,
                            shj_hedaoshuiqing_generate_dfjson,shj_hedaoshuiqing_generate,shj_laishuiyugu_context,shj_laishuiyugu_generate_dfjson,shj_laishuiyugu_generate,shj_hedaobijian_context)
from yaapp.models import TemplateNode, WordParagraph
from datetime import datetime
import os
import base64
import re
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
            # print("self.params:",   self.params)
            # print("type(self.params):",type(self.params))
            tmp = huanghe_yuqing_generate(self.params)
            ## 对每段描述内容进行细分
            wp = WordParagraph.objects.create(title="雨情实况", content=tmp, ctype=1)
            # self.node.wordParagraphs.clear()
            for n in self.node.wordParagraphs.all():
                n.delete()
            self.node.wordParagraphs.add(wp)
            return tmp
            # return ""
        elif self.context['type'] == 1:
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
            return divHtml(f"黄河主要站点流量表（{current_date}）\n") + tmp
        elif self.context['type'] == 1:
            # 小浪底河道水情
            #TODO
            print("# 小浪底河道水情#TODO")
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
            return divHtml(f"黄河主要水库蓄水情况表（{current_date}）\n") + huanghe_shuikushuiqing_generate(self.params)
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
        print("get_jyyb", self.context)
        def jyyb_imgs(context):
            jyyb_imgs = context.get("jyyb_imgs", [])
            tmpHtml = ""
            for imgJson in jyyb_imgs:
                print("jyyb img:",imgJson)
                tmpdesc = imgJson['desc']
                tmpfname = imgJson['url']
                tmppath = os.path.join("data", "imgs", self.context['yadate'], tmpfname)
                if not os.path.exists(tmppath):
                    continue
                encoded_string = img2base64(tmppath)
                wp = WordParagraph.objects.create(title="降雨预报", content=encoded_string, ctype=2)
                self.node.wordParagraphs.add(wp)
                wp = WordParagraph.objects.create(title="降雨预报", content=tmpdesc, ctype=1)
                self.node.wordParagraphs.add(wp)
                tmpHtml += divHtml("<image src='data:image/png;base64," + encoded_string + "'>") + "\n" + paraHtml(tmpdesc) + "\n"
            return tmpHtml

        if self.context['type'] == 0:
            # 黄河中下游
            for n in self.node.wordParagraphs.all():
                n.delete()
            jiangyu13 = huanghe_jiangyu13_forecast(self.params)
            # wp = WordParagraph.objects.create(title="降雨预报", content="1） 降雨预报   \n", ctype=0)
            # self.node.wordParagraphs.add(wp)
            # wp = WordParagraph.objects.create(title="降雨预报", content=jiangyu13, ctype=1)
            # self.node.wordParagraphs.add(wp)
            jyyb_img_html = jyyb_imgs(self.params)
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
            yubao = (f"降雨预报\n"
                     f"\t{jyyb_img_html}\n"
                     f"分区面平均雨量预报   \n" + 
                     divHtml(f"黄河流域分区面平均雨量预报（单位：mm）  \n") + 
                     f"\t{jiangyu_table}\n")
                     # f"4）未来4—7天降水预报  \n"
                     # f"\t{jiangyu47}\n")
            #print("预报：",yubao)
            return yubao
        elif self.context['type'] == 1:
            # 小浪底
            #TODO
            return ""
    
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
            #print("XXXXXXXXXXXXXX")
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
            ddfa_excel = os.path.join("media", "ddfa", f"{yadate}.xlsx")
            if not os.path.exists(ddfa_excel):
                raise Exception("调度方案单不存在")
            ddjy=generate_ddjy(ddfa_excel)
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
            # 三花间
            import pandas as pd
            import time
            yadate = self.context['plan']['yadate']
            ddfa_excel = os.path.join("media", "ddfa", f"{yadate}.xlsx")
            if not os.path.exists(ddfa_excel):
                raise Exception("调度方案单不存在")
            ddjy = generate_ddjy(ddfa_excel)
            for n in self.node.wordParagraphs.all():
                n.delete()
            tmpjson = huanghe_diaodu_plan_jianyi_ctx(ddjy)
            wp = WordParagraph.objects.create(title="调度方案单", content=json.dumps(tmpjson), ctype=3)
            self.node.wordParagraphs.add(wp)
            #TODO
            return huanghe_diaodu_plan_jianyi_html(ddjy)
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
            ddfa_excel = os.path.join("media", "ddfa", f"{yadate}.xlsx")
            if not os.path.exists(ddfa_excel):
                raise Exception("调度方案单不存在")
            pd.set_option('display.notebook_repr_html', False)
            # 读取xls（绝对路径）
            df = pd.read_excel(io=ddfa_excel, header=None)
            if len(df) < 4:
                return """暂无数据"""
            xld_max_sw, xld_max_d = None, None
            smx_max_sw, smx_max_d = None, None
            hkc_max_sw, hkc_max_d = None, None
            lh_max_sw, lh_max_d = None, None
            gx_max_sw, gx_max_d = None, None
            hyk_max_ll, tg_max_ll, hyk_max_d, tg_max_d = None, None, None, None
            x_days = []
            y_xld_sw, y_smx_sw, y_hkc_sw, y_lh_sw, y_gx_sw = [], [], [], [], []
            y_xld_ifs, y_smx_ifs, y_hkc_ifs, y_lh_ifs, y_gx_ifs = [], [], [], [], []
            y_xld_ofs, y_smx_ofs, y_hkc_ofs, y_lh_ofs, y_gx_ofs = [], [], [], [], []
            for i, r in df.iterrows():
                if i < 3:
                    continue
                try:
                    d = r[0]
                    if isinstance(d, datetime.datetime):
                        d = d.strftime('%Y{}%m{}%d{}%H{}').format("年", "月", "日", "时")
                    elif isinstance(d, str):
                        timeArray = time.strptime(d, "%Y-%m-%d %H:%M:%S")
                        d = time.strftime('%Y{}%m{}%d{}%H{}', timeArray).format("年", "月", "日", "时")
                except:
                    d = r[0]
                    pass
                tg_ll = r[1]
                smx_sw = round(r[4], 2)
                smx_inflow = r[2]
                smx_outflow = r[3]
                xld_sw = round(r[8], 2)
                xld_inflow = r[6]
                xld_outflow = r[7]
                lh_sw = round(r[12], 2)
                lh_inflow = r[10]
                lh_outflow = r[11]
                gx_sw = round(r[16], 2)
                gx_inflow = r[14]
                gx_outflow = r[15]
                hkc_sw = round(r[20], 2)
                hkc_inflow = r[18]
                hkc_outflow = r[19]

                hyk_ll = r[22]
                x_days.append(str(d))
                y_xld_sw.append(xld_sw)
                y_xld_ifs.append(xld_inflow)
                y_xld_ofs.append(xld_outflow)

                y_smx_sw.append(smx_sw)
                y_smx_ifs.append(smx_inflow)
                y_smx_ofs.append(smx_outflow)

                y_gx_sw.append(gx_sw)
                y_gx_ifs.append(gx_inflow)
                y_gx_ofs.append(gx_outflow)

                y_hkc_sw.append(hkc_sw)
                y_hkc_ifs.append(hkc_inflow)
                y_hkc_ofs.append(hkc_outflow)

                y_lh_sw.append(lh_sw)
                y_lh_ifs.append(lh_inflow)
                y_lh_ofs.append(lh_outflow)

                ## 河道
                if hyk_max_ll is None:
                    hyk_max_ll = hyk_ll
                    hyk_max_d = d
                if hyk_max_ll < hyk_ll:
                    hyk_max_ll = hyk_ll
                    hyk_max_d = d
                if tg_max_ll is None:
                    tg_max_ll = tg_ll
                    tg_max_d = d
                if tg_max_ll < tg_ll:
                    tg_max_ll = tg_ll
                    tg_max_d = d
                ## 水库
                if xld_max_sw is None:
                    xld_max_sw = xld_sw
                    xld_max_d = d
                if xld_max_sw < xld_sw:
                    xld_max_sw = xld_sw
                    xld_max_d = d
                if smx_max_sw is None:
                    smx_max_sw = smx_sw
                    smx_max_d = d
                if smx_max_sw < smx_sw:
                    smx_max_sw = smx_sw
                    smx_max_d = d

                if hkc_max_sw is None:
                    hkc_max_sw = hkc_sw
                    hkc_max_d = d
                if hkc_max_sw < hkc_sw:
                    hkc_max_d = d
                if lh_max_sw is None:
                    lh_max_sw = lh_sw
                    lh_max_d = d
                if lh_max_sw < lh_sw:
                    lh_max_sw = lh_sw
                    lh_max_d = d
                if gx_max_sw is None:
                    gx_max_sw = gx_sw
                    gx_max_d = d
                if gx_max_sw < gx_sw:
                    gx_max_sw = gx_sw
                    gx_max_d = d

            xld_max_d = str(xld_max_d).split(' ')[0]
            xld_max_sw = round(xld_max_sw, 2)
            smx_max_d = str(smx_max_d).split(' ')[0]
            smx_max_sw = round(smx_max_sw, 2)

            hkc_max_d = str(hkc_max_d).split(' ')[0]
            hkc_max_sw = round(hkc_max_sw, 2)

            gx_max_d = str(gx_max_d).split(' ')[0]
            gx_max_sw = round(gx_max_sw, 2)

            lh_max_d = str(lh_max_d).split(' ')[0]
            lh_max_sw = round(lh_max_sw, 2)


            skddresult = ""
            xld_ddgc_img_path = f"data/{self.context['plan']['yadate']}/imgs/xld.png"
            xld_ddgc_img = img2base64(xld_ddgc_img_path)
            xld_ddgc_img_desc = f"小浪底水库调度过程({x_days[0]}~{x_days[-1]})"
            xld_ddjg_result = f"预计小浪底水库将于{xld_max_d}达到最高水位{xld_max_sw}m，{xld_sk(sw=xld_max_sw)}；\n"
            
            skddresult += paraHtml(xld_ddjg_result) + divHtml("<image src='data:image/png;base64," + xld_ddgc_img + "'>") + "\n" + divHtml(xld_ddgc_img_desc) + "\n"

            smx_ddgc_img_path = f"data/{self.context['plan']['yadate']}/imgs/smx.png"
            smx_ddjg_img = img2base64(smx_ddgc_img_path)
            smx_ddgc_img_desc = f"三门峡水库调度过程({x_days[0]}~{x_days[-1]})"
            smx_ddjg_result = f"预计三门峡水库将于{smx_max_d}达到最高水位{smx_max_sw}m，{smx_sjt_sk(sw=smx_max_sw)}；\n"
            skddresult += paraHtml(smx_ddjg_result) + divHtml("<image src='data:image/png;base64," + smx_ddjg_img + "'>") + "\n" + divHtml(smx_ddgc_img_desc) + "\n"


            lh_ddgc_img_path = f"data/{self.context['plan']['yadate']}/imgs/lh.png"
            lh_ddgc_img = img2base64(lh_ddgc_img_path)
            lh_ddgc_img_desc = f"陆浑水库调度过程（{x_days[0]}~{x_days[-1]}）"
            lh_ddjg_result = f"预计陆浑水库将于{lh_max_d}达到最高水位{lh_max_sw}m，{lhbs_sk(sw=lh_max_sw)}；\n"
            skddresult += paraHtml(lh_ddjg_result) + divHtml("<image src='data:image/png;base64," + lh_ddgc_img + "'>") + "\n" + divHtml(lh_ddgc_img_desc) + "\n"

            
            gx_ddgc_img_path = f"data/{self.context['plan']['yadate']}/imgs/gx.png"
            gx_ddgc_img = img2base64(gx_ddgc_img_path)
            gx_ddgc_img_desc = "故县水库调度过程（{x_days[0]}~{x_days[-1]}）\n"
            gx_ddjg_result = f"预计故县水库将于{gx_max_d}达到最高水位{gx_max_sw}m，{gx_sk(sw=gx_max_sw)}；"
            skddresult += paraHtml(gx_ddjg_result) + divHtml("<image src='data:image/png;base64," + gx_ddgc_img + "'>") + "\n" + divHtml(gx_ddgc_img_desc) + "\n"

            hkc_ddgc_img_path = f"data/{self.context['plan']['yadate']}/imgs/hkc.png"
            hkc_ddgc_img = img2base64(hkc_ddgc_img_path)
            hkc_ddgc_img_desc = f"河口村水库调度过程({x_days[0]}~{x_days[-1]})\n"
            hkc_ddjg_result = f"预计河口村水库将于{hkc_max_d}达到最高水位{hkc_max_sw}m，{hkc_sk(sw=hkc_max_sw)}；"
            skddresult += paraHtml(hkc_ddjg_result) + divHtml("<image src='data:image/png;base64," + hkc_ddgc_img + "'>") + "\n" + divHtml(hkc_ddgc_img_desc) + "\n"

            # skddresult = xld_ddjg_result + smx_ddjg_result + lh_ddjg_result + gx_ddjg_result + hkc_ddjg_result

            # 河道
            hd_ddgc_img_path = f"data/{self.context['plan']['yadate']}/imgs/hyk.png"
            hd_ddgc_img = img2base64(hd_ddgc_img_path)
            hd_ddgc_img_desc = f"花园口调度过程（{x_days[0]}~{x_days[-1]}）"
            hd_hyk_result = f"预计{hyk_max_d}，花园口出现{hyk_max_ll}立方米每秒的洪峰流量\n"
            hd_result = paraHtml(hd_hyk_result) + divHtml("<image src='data:image/png;base64," + hd_ddgc_img + "'>" ) + "\n" + paraHtml(hd_ddgc_img_desc) + "\n"
            
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
            wp = WordParagraph.objects.create(title="小浪底水库过程曲线", content=xld_ddgc_img, ctype=2)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="三门峡水库过程曲线", content=smx_ddjg_img, ctype=2)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="陆浑水库过程曲线", content=lh_ddgc_img, ctype=2)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="故县水库过程曲线", content=gx_ddgc_img, ctype=2)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="河口村水库过程曲线", content=hkc_ddgc_img, ctype=2)
            self.node.wordParagraphs.add(wp)
            wp = WordParagraph.objects.create(title="花园口过程曲线", content=hd_ddgc_img, ctype=2)
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
            #         print(encoded_string.decode('utf-8'))
            wp = WordParagraph.objects.create(title="枢纽运用", content="预报小浪底水库的调度过程", ctype=1)
            self.node.wordParagraphs.add(wp)
            encoded_string = re.sub('^data:image/.+;base64,', '', ddgc_img)
            wp = WordParagraph.objects.create(title="降雨预报", content=encoded_string, ctype=2)
            self.node.wordParagraphs.add(wp)
            tmpHtml +=  "预报小浪底水库的调度过程" + "\n""<image src='data:image/png;base64," + encoded_string + "'>" + "\n"
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
    def make_context(self,):
        # print("make_context:", self.context, self.params)
        label = self.node.label
        print("label:", label)
        #label = map_input_to_label(user_input=label)
        if label == "雨情实况" or label =="实时雨水情":
            print("雨情实况 get_ysq")
            result = self.get_ysq()
        elif label == "河道水情":
            print("河道水情 get_hdsq")
            result = self.get_hdsq()
        elif label == "水库水情":
            print("水库水情 get_sksq")
            result = self.get_sksq()
        elif label == "工情险情实况" or label == "工情险情":
            print("工情险情实况 get_gqxq")
            result = self.get_gqxq() #ori_ctx
        elif label == "降雨预报":
            print("降雨预报 get_jyyb")
            result = self.get_jyyb()
        elif label == "洪水预报":
            print("洪水预报 get_hsyb")
            result = self.get_hsyb()
        elif label == "调度方案" or label == "水库调度方案":
            print("调度方案 get_ddfa")
            result = self.get_ddfa()
        elif label == "调度结果":
            print("调度结果 get_ddjg")
            result = self.get_ddjg()
        elif label =="工程研判":
            print("工程研判 get_gcyp")
            result = self.get_gcyp()
        elif label =="枢纽运用方案":
            print("枢纽运用方案 get_snyy")
            result = self.get_snyy()
        elif label == "安全举措":
            print("安全举措 get_aqjc")
            result = self.get_aqjc()
        elif label == "来水预估":
            print("安全举措 get_lsyg")
            result = self.get_lsyg()
        elif label =="河道边界条件":
            print("河道边界条件 get_hdbjtj")
            result = self.get_hdbjtj()
        elif label == "调度原则和调度目标":
            print("调度原则和调度目标 get_ddyz_ddmb")
            result = self.get_ddyz_ddmb()
        else: 
            result = generate_description_for_label(label)
            for n in self.node.wordParagraphs.all():
                n.delete()
            wp = WordParagraph.objects.create(title=label, content=f"\n{result}", ctype=1)
            self.node.wordParagraphs.add(wp)
        self.node.result = result
        self.node.save()
        # print("make ctt result:", result)
