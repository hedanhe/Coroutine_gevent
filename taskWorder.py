
# import gevent
# from gevent import monkey; monkey.patch_all()
#monkey.patch_all()与BaseManager冲突了
from multiprocessing import Pool
from multiprocessing.managers import BaseManager
import time, re, os
import requests
from bs4 import BeautifulSoup

#分布式进程
class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

server_addr = '127.0.0.1'
print('Connent to')

def download(i):
    while not task.empty():
    # get_queue = task.get(True, timeout=10)
        txt_url = task.get(True, timeout=10)
        if  txt_url == None:
            break
        url = txt_url["href"]
        box_title = txt_url["box_title"]
        print("开始下载：{}".format(box_title))
        if "/" in box_title:
            box_title = box_title.replace("/", "")

        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36"
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding  # 正确解码
        html_str = response.text
        soup = BeautifulSoup(html_str, 'lxml', from_encoding='utf-8')
        aaa = soup.find(class_="content")
        bbb = re.search(r"</ins>([\s\S]*?)<!--广告位置-->", str(aaa))
        ccc = re.findall(r"<p>([\s\S]*?)</p>", str(bbb.group()))

        dmbj_txt = ""
        for i in ccc:
            ddd = i.replace("\u3000\u3000", "\n\r\r")
            dmbj_txt += ddd
        save_dir = "盗墓笔记全本/"
        if os.path.exists(save_dir) is False:
            os.makedirs(save_dir)

        with open(save_dir + box_title + ".txt", "w", encoding="utf-8") as f:
            f.write(dmbj_txt)
        print("下载完成：{}".format(box_title))

if __name__ == "__main__":
    start_time = time.time()
    m = QueueManager(address=(server_addr, 8002), authkey=b'abc')
    m.connect()
    print('Connent ok')
    task = m.get_task_queue()
    result = m.get_result_queue()

    groups = [x for x in range(0, 4)]
    pool = Pool()
    pool.map(download, groups)

    result.put("ok")
    print(time.time()-start_time)
    print('worker exit')