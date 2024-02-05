import json
import os
import re
import requests
from pycqBot import *


class MovieSearch(Plugin):
    def __init__(self, bot: cqBot, cqapi: cqHttpApi, plugin_config):
        super().__init__(bot, cqapi, plugin_config)
        # 添加指令
        bot.command(self.search, "影视搜索", {
            "type": "all"
        }).command(self.choose_res, "搜索结果", {
            "type": "all"
        }).command(self.choose_series, "选集", {
            "type": "all"
        }).command(self.change_page, "换页", {
            "type": "all"
        })

    def search(self, content, message):
        qq = message.user_id
        url = "http://www.ffzy.tv/api.php/provide/vod/"
        params = {
            "ac": "detail",
            "wd": content[0],
            "pg": 1
        }
        response = requests.get(url, params=params)
        response.encoding = "utf-8"
        if response.status_code != 200:
            message.reply("影视搜索接口失效！联系机器人管理员更换！")
        else:
            os.makedirs(f"./plugin/MovieSearch/data/{qq}", exist_ok=True)
            with open(f"./plugin/MovieSearch/data/{qq}/name.txt", "wb") as file:
                file.write(content[0].encode('utf-8'))
            with open(f"./plugin/MovieSearch/data/{qq}/pg1.txt", "wb") as file:
                file.write(response.content)
            data = json.loads(response.text)
            page_total = data["pagecount"]
            result_total = data["total"]
            now_page = data["page"]
            msg = f"搜索到{result_total}条结果\n当前是第{now_page}页\n共{page_total}页\n"
            num = 1
            for i in data["list"]:
                msg = msg + f"{num}.{i['vod_name']}\n"
                num += 1
            msg = msg + "输入 #换页 页码 来换页\n输入 #搜索结果 页码 序号 来选择"
            message.reply(msg)

    def choose_res(self, data, message: Message):
        choose_page = int(data[0])
        choose_res = int(data[1])
        file_path = f"./plugin/MOvieSearch/data/{message.user_id}/pg{choose_page}.txt"
        if os.path.exists(file_path):
            with open(f"./plugin/MovieSearch/data/{message.user_id}/pg{choose_page}.txt", "r",encoding="utf-8") as file:
                json_data = json.loads(file.read())
            num = 0
            for i in json_data["list"]:
                if num == choose_res - 1:
                    all_series = i["vod_play_url"]
                    all_series = re.search(r"(.*?)\$\$\$", all_series)
                    all_series_list = all_series.group(1).split("#")
                    series = 0
                    for i in all_series_list:
                        series += 1
                    message.reply(f"共有{series}集，请输入：\n#选集 页数 序号 集数\n来选择集数")
                num += 1
        else:
            message.reply("所选页码不存在！")

    def choose_series(self, data, message:Message):
        choose_page = int(data[0])
        choose_res = int(data[1])
        choose_series = int(data[2])
        file_path = f"./plugin/MOvieSearch/data/{message.user_id}/pg{choose_page}.txt"
        if os.path.exists(file_path):
            with open(f"./plugin/MovieSearch/data/{message.user_id}/pg{choose_page}.txt", "r",encoding="utf-8") as file:
                json_data = json.loads(file.read())
            num = 0
            for i in json_data["list"]:
                if num == choose_res - 1:
                    all_series = i["vod_play_url"]
                    all_series = re.search(r"(.*?)\$\$\$", all_series)
                    all_series_list = all_series.group(1).split("#")
                    series = 0
                    for i in all_series_list:
                        series += 1
                    if choose_series > series:
                        message.reply("所选集数不存在！")
                    else:
                        n = 1
                        for i in all_series_list:
                            if choose_series == n:
                                list_se = i.split("$")
                                message.reply(f"{list_se[0]} 播放地址\n{list_se[1]}\n注：请在系统浏览器打开")
                            n += 1
                num += 1
        else:
            message.reply("所选页码不存在！")

    def change_page(self, data, message:Message):
        page = int(data[0])
        qq = message.user_id
        name_path = f"./plugin/MOvieSearch/data/{message.user_id}/name.txt"
        if os.path.exists(name_path):
            with open(name_path, "r", encoding="utf-8") as file:
                content = file.read()
            url = "http://www.ffzy.tv/api.php/provide/vod/"
            params = {
                "ac": "detail",
                "wd": content,
                "pg": page
            }
            response = requests.get(url, params=params)
            response.encoding = "utf-8"
            if response.status_code != 200:
                message.reply("影视搜索接口失效！联系机器人管理员更换！")
            else:
                os.makedirs(f"./plugin/MovieSearch/data/{qq}", exist_ok=True)
                with open(f"./plugin/MovieSearch/data/{qq}/pg{page}.txt", "wb") as file:
                    file.write(response.content)
                data = json.loads(response.text)
                page_total = data["pagecount"]
                result_total = data["total"]
                now_page = data["page"]
                msg = f"搜索到{result_total}条结果\n当前是第{now_page}页\n共{page_total}页\n"
                num = 1
                for i in data["list"]:
                    msg = msg + f"{num}.{i['vod_name']}\n"
                    num += 1
                msg = msg + "输入 #换页 页码 来换页\n输入 #搜索结果 页码 序号 来选择"
                message.reply(msg)
        else:
            message.reply("你都没有搜索，换什么页面？")