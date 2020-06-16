import requests
import os
import json
import re
import random

from hoshino.service import Service

config_path = os.path.dirname(__file__)+'/config.json'
sv = Service('damage_dragon', enable_on_default=False)

@sv.on_keyword(keywords=('迫害龙王'))
async def _(bot, ctx):
    gid = ctx.get('group_id')
    try:
        cookies = await bot.get_cookies(domain='qun.qq.com')
    except:
        await bot.send(ctx, '获取cookies失败')
    headers = {
        "cookie": cookies['cookies']
    }
    url = f'https://qun.qq.com/interactive/honorlist?gc={gid}&type=1'
    with requests.post(url, headers=headers) as resp:
        text = resp.text
        json_text = re.search(
            'window.__INITIAL_STATE__=(.+?)</script>', text).group(1)
        data = json.loads(json_text)
        dragon_king = data['talkativeList'][0]['uin']
    replys = [
        '龙王出来喷水',
        # '[CQ:image,file=505BBF25835D6597848E6AD57B635E68.jpg]'
    ]
    reply = random.sample(replys, 1)[0]
    await bot.send(ctx, f'[CQ:at,qq={dragon_king}] {reply}')


@sv.on_keyword(keywords=('龙王是谁'))
async def _(bot, ctx):
    gid = ctx.get('group_id')
    try:
        cookies = await bot.get_cookies(domain='qun.qq.com')
    except:
        await bot.send(ctx, '获取cookies失败')
    headers = {
        "cookie": cookies['cookies']
    }
    url = f'https://qun.qq.com/interactive/honorlist?gc={gid}&type=1'
    with requests.post(url, headers=headers) as resp:
        text = resp.text
        json_text = re.search(
            'window.__INITIAL_STATE__=(.+?)</script>', text).group(1)
        data = json.loads(json_text)
        dragon_king = data['talkativeList'][0]['name']
    replys = [
        '龙王出来喷水',
        # '[CQ:image,file=505BBF25835D6597848E6AD57B635E68.jpg]'
    ]
    await bot.send(ctx, f'本群的龙王是{dragon_king}哦，ヤバイですね☆')
