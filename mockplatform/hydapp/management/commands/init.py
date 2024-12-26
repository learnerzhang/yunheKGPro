from django.core.management.base import BaseCommand, CommandError
from hydapp.models import *
from datetime import datetime, timedelta

sk_stcds = [('40104720', '西霞院'), ('40104690', '小浪底')]
sw_stcds = [('40105150', '花园口'), ('40104450', '三门峡'), ('40104360', '潼关')]

def init_stcds():
    """
    站点数据初始化
    """
    ShuiKu.objects.all().delete()

    for stcd, name in sk_stcds:
        ShuiKu.objects.create(name=name, stcd=stcd)

    ShuiWen.objects.all().delete()
    
    for stcd, name in sw_stcds:
        ShuiWen.objects.create(name=name, stcd=stcd)
    print("init stcds done")




def generate_normal_distribution_samples(mean, std_dev, count):
    import numpy as np
    """
    生成一个正态分布的随机样本。
    
    :param mean: 正态分布的均值。
    :param std_dev: 正态分布的标准差。
    :param count: 要生成的样本数量。
    :return: 一个包含随机样本的numpy数组。
    """
    samples = np.random.normal(loc=mean, scale=std_dev, size=count)
    return samples


def init_history():
    print("init history")
    HeDaoData.objects.all().delete()
    # 获取当前日期
    today = datetime.now()
    N = 10
    past_10_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(N)]
    sw2flower = {
        "花园口": 668.0,
        "三门峡": 111.0,
        "潼关": 364.0,
    }

    for stcd, name in sw_stcds:
        tmpflow = sw2flower[name]
        samples = generate_normal_distribution_samples(mean=tmpflow, std_dev=50, count=N)
        tmpsk, _ = ShuiWen.objects.get_or_create(name=name, stcd=stcd)
        for i, tmpdate in enumerate(past_10_days):
            HeDaoData.objects.create(sw_pk=tmpsk, flow_h8=samples[i], date=tmpdate, name=name, stcd=stcd)

    
    sk2kr = {
        "小浪底": [126.5, 666, 777, 243, 305, 13.6, ],
        "西霞院": [1.62, 2690, 2790, 129.52, 275, 1.26],
    }


    for stcd, name in sk_stcds:
        tmpinflow = sk2kr[name][1]
        tmpoutflow = sk2kr[name][2]
        tmpkr = sk2kr[name][0]
        tmpsw = sk2kr[name][3]
        tmp_xx_sw = sk2kr[name][4]
        tmp_xl = sk2kr[name][5]

        inflow_samples = generate_normal_distribution_samples(mean=tmpinflow, std_dev=100, count=N)
        outflow_samples = generate_normal_distribution_samples(mean=tmpoutflow, std_dev=100, count=N)
        sw_samples = generate_normal_distribution_samples(mean=tmpsw, std_dev=10, count=N)
        xx_sw_samples = generate_normal_distribution_samples(mean=tmp_xx_sw, std_dev=10, count=N)
        xl_samples = generate_normal_distribution_samples(mean=tmp_xl, std_dev=5, count=N)


        tmpsk, _ = ShuiKu.objects.get_or_create(name=name, stcd=stcd)
        for i, tmpdate in enumerate(past_10_days):
            inflow = inflow_samples[i]
            outflow = outflow_samples[i]
            sw = sw_samples[i]
            xx_sw = xx_sw_samples[i]
            xl = xl_samples[i]
            diff_xl = xl - tmp_xl
            sy_kr = tmpkr
            ShuiKuData.objects.create(sk_pk=tmpsk, date=tmpdate, name=name, stcd=stcd, inflow=inflow, outflow=outflow, sw=sw, xx_sw=xx_sw, xl=xl, diff_xl=diff_xl, sy_kr=sy_kr, sediment=0, sediment_rate=0)

    print("init history done")


def init_future():
    print("init future")

    today = datetime.now()
    N = 15
    past_10_days = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(N)]
    sw2flower = {
        "花园口": 668.0,
        "三门峡": 111.0,
        "潼关": 364.0,
    }
    for stcd, name in sw_stcds:
        tmpflow = sw2flower[name]
        samples = generate_normal_distribution_samples(mean=tmpflow, std_dev=20, count=N)
        tmpsk, _ = ShuiWen.objects.get_or_create(name=name, stcd=stcd)
        for i, tmpdate in enumerate(past_10_days):
            FutureHeDaoData.objects.create(sw_pk=tmpsk, flow_h8=samples[i], model_name="默认模型", date=tmpdate, name=name, stcd=stcd)

    
    sk2kr = {
        "小浪底": [126.5, 666, 777, 243, 305, 13.6, ],
        "西霞院": [1.62, 2690, 2790, 129.52, 275, 1.26],
    }

    for stcd, name in sk_stcds:
        tmpinflow = sk2kr[name][1]
        tmpoutflow = sk2kr[name][2]
        tmpkr = sk2kr[name][0]
        tmpsw = sk2kr[name][3]
        tmp_xx_sw = sk2kr[name][4]
        tmp_xl = sk2kr[name][5]

        inflow_samples = generate_normal_distribution_samples(mean=tmpinflow, std_dev=100, count=N)
        outflow_samples = generate_normal_distribution_samples(mean=tmpoutflow, std_dev=100, count=N)
        sw_samples = generate_normal_distribution_samples(mean=tmpsw, std_dev=10, count=N)
        xx_sw_samples = generate_normal_distribution_samples(mean=tmp_xx_sw, std_dev=10, count=N)
        xl_samples = generate_normal_distribution_samples(mean=tmp_xl, std_dev=5, count=N)


        tmpsk, _ = ShuiKu.objects.get_or_create(name=name, stcd=stcd)
        for i, tmpdate in enumerate(past_10_days):
            inflow = inflow_samples[i]
            outflow = outflow_samples[i]
            sw = sw_samples[i]
            xx_sw = xx_sw_samples[i]
            xl = xl_samples[i]
            diff_xl = xl - tmp_xl
            sy_kr = tmpkr
            FutureShuiKuData.objects.create(sk_pk=tmpsk, date=tmpdate, name=name, stcd=stcd, model_name="默认模型",
                                            inflow=inflow, outflow=outflow, sw=sw, xx_sw=xx_sw, xl=xl, diff_xl=diff_xl, sy_kr=sy_kr, sediment=0, sediment_rate=0)

    print("init history done")
    print("init future done")


class Command(BaseCommand):
    help = 'Describe what this command does'

    def add_arguments(self, parser):
        # 你可以在这里添加命令行参数
        parser.add_argument('arg', nargs='?', type=str, help='An argument for my command')

    def handle(self, *args, **options):
        # 这里写命令的逻辑
        arg = options['arg']
        if arg:
            self.stdout.write(self.style.SUCCESS('The argument is "%s"' % arg))
            if arg == 'history' or arg == 'h' or arg == 'hist':
                init_history()
            if arg == 'future' or arg == 'fut' or arg == 'f':
                init_future()
            if arg == 'stcds':
                init_stcds()
        else:
            self.stdout.write(self.style.WARNING('No argument provided'))
            init_stcds()
            init_history()
            init_future()
            