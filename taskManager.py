import queue
import requests
import re, json, time
from bs4 import BeautifulSoup
from multiprocessing.managers import BaseManager
#分布式进程
task_queue = queue.Queue()
result_queue = queue.Queue()

class Queuemanager(BaseManager):
    pass

def get_url():
    url = "http://seputu.com/"

    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36"
    headers = {'User-Agent': user_agent}

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')
    # content = []
    for mulu in soup.find_all(class_="mulu"):
        h2 = mulu.find("h2")
        if h2 != None:
            h2_title = h2.string
            if "盗墓笔记" in h2_title:
                list = []
                for a in mulu.find(class_="box").find_all("a"):
                    href = a.get("href")
                    print(a.get("title"))
                    aa = re.search("\[.*?\]", a.get("title")).group()
                    # print(aa)
                    box_title = a.get("title").replace(aa, "")
                    list.append({"href": href, "box_title": box_title})
                    task.put({"href": href, "box_title": box_title})
                    print("put url ok {}".format(url))
                    time.sleep(0.1)
                # content.append({"title": h2_title, "content": list})

if __name__ == "__main__":
    #windows下绑定调用接口不能用lambda，智能先定义函数再绑定
    Queuemanager.register('get_task_queue', callable= lambda :task_queue)
    Queuemanager.register('get_result_queue', callable= lambda :result_queue)

    manager = Queuemanager(address=('127.0.0.1', 8002), authkey=b'abc')
    manager.start()


    task = manager.get_task_queue()
    result = manager.get_result_queue()
    get_url()

    while result.empty():
        print("等待下载完成……")
        time.sleep(5)
    print("全本下载完成")
    manager.shutdown()
