
import re
import os
import ujson as json

import datetime

from hoshino.service import Service, Privilege as Priv
from hoshino import R
sv = Service('buildtime', manage_priv=Priv.SUPERUSER, enable_on_default=True)

# bot = get_bot()


# 这里定义活动名称

ACTIVITY = "穹顶下的圣咏曲"


def get_build_time_activity_gacha(ACTIVITY_NAME):
    filename = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(filename, encoding='utf8') as f:
        config = json.load(f)
    return config["ACTIVITY_GACHA"][ACTIVITY_NAME]


def get_build_time_general_gacha():
    filename = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(filename, encoding='utf8') as f:
        config = json.load(f)
    return config["GENERAL_GACHA"]


def get_time(get_day):
    # 剩余天数是0
    if 0 == get_day.days:
        # 24小时内未满2位数小时
        if str(get_day)[1] == ":":
            '''
            print("0") 				# 天
            print(str(day)[0]) 		# 时
            print(str(day)[2:4])	# 分
            print(str(day)[5:7])	# 秒
            '''
            day = "0"
            hour = str(get_day)[0]
            minute = str(get_day)[2:4]
            second = str(get_day)[5:7]
            return day, hour, minute, second
        # 24小时内满足2位数小时
        else:
            '''
            print("0") 				# 天
            print(str(day)[0:2]) 	# 时
            print(str(day)[3:5])	# 分
            print(str(day)[6:8])	# 秒
            '''
            day = "0"
            hour = str(get_day)[0:2]
            minute = str(get_day)[3:5]
            second = str(get_day)[6:8]
            return day, hour, minute, second
    # 剩余天数是1位数
    elif 1 <= get_day.days <= 9:
        # 24小时内未满2位数小时
        if str(get_day)[8] == ":":
            '''
            print(str(day)[0]) 		# 天
            print(str(day)[7]) 		# 时
            print(str(day)[9:11])	# 分
            print(str(day)[12:14])	# 秒
            '''
            day = str(get_day)[0]
            hour = str(get_day)[7]
            minute = str(get_day)[9:11]
            second = str(get_day)[12:14]
            return day, hour, minute, second
        # 24小时内已满2位数小时
        else:
            '''
            print(str(day)[0]) 		# 天
            print(str(day)[7:9]) 	# 时
            print(str(day)[10:12])	# 分
            print(str(day)[13:15])	# 秒
            '''
            day = str(get_day)[0]
            hour = str(get_day)[7:9]
            minute = str(get_day)[10:12]
            second = str(get_day)[13:15]
            return day, hour, minute, second
    # 剩余天数是2位数
    elif 10 <= get_day.days:
        # 24小时内未满2位数小时
        if str(get_day)[10] == ":":
            '''
            print(str(day)[0:2]) 	# 天
            print(str(day)[9]) 		# 时
            print(str(day)[11:13])	# 分
            print(str(day)[14:16])	# 秒
            '''
            day = str(get_day)[0:2]
            hour = str(get_day)[9]
            minute = str(get_day)[11:13]
            second = str(get_day)[14:16]
            return day, hour, minute, second
        # 24小时内已满2位数小时
        else:
            '''
            print(str(day)[0:2]) 	# 天
            print(str(day)[9:11]) 	# 时
            print(str(day)[12:14])	# 分
            print(str(day)[15:17])	# 秒
            '''
            day = str(get_day)[0:2]
            hour = str(get_day)[9:11]
            minute = str(get_day)[12:14]
            second = str(get_day)[15:17]
            return day, hour, minute, second


@sv.on_message('group')
async def handle(bot,  context):
    message = context['raw_message']
    if message.startswith('建造时间'):
        msg = message[4:]
        msg = msg.strip()
        # 获取卡池
        general_gacha = get_build_time_general_gacha()
        if msg in general_gacha.keys():
            s = msg + "：\n"
            for subkey, subvalue in general_gacha[msg].items():
                s = s + subkey + "：" + subvalue + "\n"
            s = s[:-1]
            await bot.send(context, f'{s}', at_sender=False)
            return
        await bot.send(context, f'不存在该舰娘，请重新查询', at_sender=False)
        return
    elif re.match(r'^活动建造[表(时间)]', message):
        msg = get_build_time_activity_gacha(ACTIVITY)
        # 活动时间-当前时间
        day = (datetime.datetime(msg["time"]["year"],
                                 msg["time"]["month"], msg["time"]["day"]) +
               datetime.timedelta(hours=msg["time"]["hour"]) -
               datetime.datetime.now())

        if 0 <= day.days:
            # 活动还在进行中
            s = ""
            for key in msg["warships"].keys():
                s1 = key + "："
                for subkey, subvalue in msg["warships"][key].items():
                    s1 = s1 + subkey + "：" + subvalue + "，"
                s1 = s1[:-1]
                s = s + s1 + "\n"
            # 距离活动结束的时间
            end_day, end_hour, end_minute, end_second = get_time(day)
            s = s + \
                f'距离活动『{ACTIVITY}』结束还有{end_day}天{end_hour}时{end_minute}分{end_second}秒'
            await bot.send(context, f'{s}', at_sender=False)
            return
        else:
            # 活动结束了
            day = (datetime.datetime.now() -
                   datetime.datetime(msg["time"]["year"],
                                     msg["time"]["month"], msg["time"]["day"]) -
                   datetime.timedelta(hours=msg["time"]["hour"]))
            # 活动结束的时间
            end_day, end_hour, end_minute, end_second = get_time(day)
            await bot.send(context, f'活动『{ACTIVITY}』已经结束{end_day}天{end_hour}时{end_minute}分{end_second}秒', at_sender=False)
            return
    elif re.match(r'^活动还[剩有]多久(结束)?', message):
        msg = get_build_time_activity_gacha(ACTIVITY)
        # 活动时间-当前时间
        day = (datetime.datetime(msg["time"]["year"],
                                 msg["time"]["month"], msg["time"]["day"]) +
               datetime.timedelta(hours=msg["time"]["hour"]) -
               datetime.datetime.now())

        if 0 <= day.days:
            # 活动还在进行中
            end_day, end_hour, end_minute, end_second = get_time(day)
            s = f'距离活动『{ACTIVITY}』结束还有{end_day}天{end_hour}时{end_minute}分{end_second}秒'
            await bot.send(context, f'{s}', at_sender=False)
            return
        else:
            # 活动结束了
            day = (datetime.datetime.now() -
                   datetime.datetime(msg["time"]["year"],
                                     msg["time"]["month"], msg["time"]["day"]) -
                   datetime.timedelta(hours=msg["time"]["hour"]))
            # 活动结束的时间
            end_day, end_hour, end_minute, end_second = get_time(day)
            await bot.send(context, f'活动『{ACTIVITY}』已经结束{end_day}天{end_hour}时{end_minute}分{end_second}秒', at_sender=False)
            return

report_chat = R.img('azurlane/活动计划.jpg').cqcode


@sv.on_message('group')
async def report(bot,  context):
    message = context['raw_message']
    if message.startswith('活动进度表'):
        await bot.send(context, f'{report_chat}', at_sender=False)


# 独立测试用
'''
@bot.on_message('group')
async def handle(context):
    message = context['raw_message']
    if message.startswith('测试'):
        return {'reply': '======================\n                        -正文-\n======================', 'at_sender': False}
'''
