# -*- coding: utf-8 -*-
import os
import sys
import datetime
import configparser
import re
import click
from colorama import init, Fore
from zhdate import ZhDate as lunar_date

def get_cache_folder():
    if os.name == 'nt':  # Windows
        cache_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'mofish_cli')
    elif os.name == 'posix':  # macOS or Linux
        cache_folder = os.path.expanduser('~/Library/Caches/mofish_cli') if sys.platform == 'darwin' else os.path.expanduser('~/.cache/mofish_cli')
    else:
        raise NotImplementedError("Unsupported operating system")

    os.makedirs(cache_folder, exist_ok=True)
    return cache_folder

def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


def get_rush_hour(rush_hour, rush_hour_friday):
    now = datetime.datetime.now()
    if now.weekday() == 4:  # Friday
        target_time = rush_hour_friday
    else:
        target_time = rush_hour

    target = datetime.datetime.strptime(f"{now.year}-{now.month}-{now.day} {target_time}", '%Y-%m-%d %H:%M')
    if now < target:
        time_delta = target - now
        hours = time_delta.seconds // 3600
        mins = (time_delta.seconds % 3600) // 60
        return f'{hours} 小时 {mins} 分钟'
    return False


def time_parse(today):
    distance_big_year = (lunar_date(today.year, 1, 1).to_datetime().date() - today).days
    distance_big_year = distance_big_year if distance_big_year > 0 else (
            lunar_date(today.year + 1, 1, 1).to_datetime().date() - today).days

    distance_5_5 = (lunar_date(today.year, 5, 5).to_datetime().date() - today).days
    distance_5_5 = distance_5_5 if distance_5_5 > 0 else (
            lunar_date(today.year + 1, 5, 5).to_datetime().date() - today).days

    distance_8_15 = (lunar_date(today.year, 8, 15).to_datetime().date() - today).days
    distance_8_15 = distance_8_15 if distance_8_15 > 0 else (
            lunar_date(today.year + 1, 8, 15).to_datetime().date() - today).days

    distance_year = (datetime.datetime.strptime(f"{today.year}-01-01", "%Y-%m-%d").date() - today).days
    distance_year = distance_year if distance_year > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-01-01", "%Y-%m-%d").date() - today).days

    distance_4_5 = (datetime.datetime.strptime(f"{today.year}-04-05", "%Y-%m-%d").date() - today).days
    distance_4_5 = distance_4_5 if distance_4_5 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-04-05", "%Y-%m-%d").date() - today).days

    distance_5_1 = (datetime.datetime.strptime(f"{today.year}-05-01", "%Y-%m-%d").date() - today).days
    distance_5_1 = distance_5_1 if distance_5_1 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-05-01", "%Y-%m-%d").date() - today).days

    distance_10_1 = (datetime.datetime.strptime(f"{today.year}-10-01", "%Y-%m-%d").date() - today).days
    distance_10_1 = distance_10_1 if distance_10_1 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-10-01", "%Y-%m-%d").date() - today).days

    distance_week_ = 5 - 1 - today.weekday()

    time_ = [
        {"v_": distance_week_ if distance_week_ > 0 else 0, "title": "周末"},  # 距离周末
        {"v_": distance_year, "title": "元旦"},  # 距离元旦
        {"v_": distance_big_year, "title": "过年"},  # 距离过年
        {"v_": distance_4_5, "title": "清明节"},  # 距离清明
        {"v_": distance_5_1, "title": "劳动节"},  # 距离劳动
        {"v_": distance_5_5, "title": "端午节"},  # 距离端午
        {"v_": distance_8_15, "title": "中秋节"},  # 距离中秋
        {"v_": distance_10_1, "title": "国庆节"},  # 距离国庆
    ]

    time_ = sorted(time_, key=lambda x: x['v_'], reverse=False)
    return time_

def set_rush_hour(config, config_path):
    time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):([0-5]?[0-9])$')
    
    def validate_time_input(prompt, default):
        while True:
            user_input = click.prompt(prompt, default=default)
            if time_pattern.match(user_input):
                return user_input
            else:
                print('时间格式不正确，请重新输入。')

    rush_hour = validate_time_input('请输入下班时间(格式为HH:MM)', '18:00')
    rush_hour_friday = validate_time_input('请输入周五下班时间，若相同可直接按回车(格式为HH:MM)', rush_hour)

    config.set('DEFAULT', 'rush_hour', rush_hour)
    config.set('DEFAULT', 'rush_hour_friday', rush_hour_friday)
    
    with open(f'{config_path}', 'w') as configfile:
        config.write(configfile)
    
    print(f'下班时间已保存在 {config_path} 中。')


@click.command()
def cli():
    """你好，摸鱼人，工作再累，一定不要忘记摸鱼哦 !"""
    cache_folder = get_cache_folder()
    config = configparser.ConfigParser()
    config_path = os.path.join(cache_folder, 'config.ini')
    config.read(config_path)
    rush_hour = config.get('DEFAULT', 'rush_hour', fallback=None)
    rush_hour_friday = config.get('DEFAULT', 'rush_hour_friday', fallback=None)

    if rush_hour is None:
        set_rush_hour(config, config_path)
        rush_hour = config.get('DEFAULT', 'rush_hour', fallback=None)
        rush_hour_friday = config.get('DEFAULT', 'rush_hour_friday', fallback=None)


    init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
    print()
    today = datetime.date.today()
    now_ = f"{today.year}年{today.month}月{today.day}日"
    week_day_ = get_week_day(today)
    print(f'{Fore.CYAN}{now_} {week_day_}')
    str_ = '''
你好，摸鱼人，工作再累，一定不要忘记摸鱼哦 ! 
有事没事起身去茶水间去廊道去天台走走，别老在工位上坐着。
多喝点水，钱是老板的，但命是自己的 !
'''
    print(f'{Fore.WHITE}{str_}')

    time_ = time_parse(today)
    for t_ in time_:
        print(f'{Fore.WHITE}距离{t_.get("title")}还有: {t_.get("v_")}天')

    if today.weekday() in range(5):
        if get_rush_hour(rush_hour, rush_hour_friday):
            print(f'\n{Fore.YELLOW}此时距离下班时间还有 {get_rush_hour(rush_hour, rush_hour_friday)}。')
            print(f'{Fore.WHITE}请提前整理好自己的桌面, 到点下班。')
        else:
            print(f'{Fore.YELLOW}现在不是上班时间，好好休息吧')

    tips_ = '''
[友情提示] 三甲医院 ICU 躺一天平均费用大概一万块。
你晚一天进 ICU，就等于为你的家庭多赚一万块。少上班，多摸鱼。
'''
    print(f'{Fore.WHITE}{tips_}')
    print(f'{Fore.GREEN}<°))))>< 摸鱼办')


if __name__ == '__main__':
    cli()