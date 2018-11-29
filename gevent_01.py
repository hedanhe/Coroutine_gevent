import gevent
from gevent import monkey; monkey.patch_all()
import requests
import threading

def get_body(i):
    print("start", i)
    url = "http://cn.bing.com"
    requests.get(url)
    print("end", i)

def get_url():
    for num in range(10, 20):
        task.append(gevent.spawn(get_body, num))

func_number = [gevent.spawn(get_body, i) for i in range(10)]
task = []
t = threading.Thread(target=get_url)
t.start()
t.join()
for n in func_number:
    task.append(n)
gevent.joinall(task)
