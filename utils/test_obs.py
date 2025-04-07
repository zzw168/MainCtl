import time

import requests
import obsws_python as obs

# obs_script_addr = "http://127.0.0.1:8899"  # OBS 脚本网址
# res = requests.get(url="%s/start" % obs_script_addr)
    #  res = requests.get(url="http://127.0.0.1:8899/stop")
    # res = requests.get(url="http://127.0.0.1:8899/reset")
# res = requests.get(url='http://127.0.0.1:8899/period?period=12.23"')
# res = requests.get(url="http://127.0.0.1:8899/term?term=1223")

# cl_request = obs.ReqClient(host='127.0.0.1', port=4455, password="")
# resp = cl_request.get_source_screenshot('终点1', "jpg", 1920, 1080, 100)
# print(resp.image_data[:22])
cl_request = obs.ReqClient()
print(cl_request)
cl_request.disconnect()
print(cl_request)
for i in range(5):
    try:
        resp = cl_request.get_source_screenshot('终点1', "jpg", 1920, 1080, 100)
        print(resp.image_data[:22])
        break
    except:
        if i < 3:
            # cl_request = obs.ReqClient(host='127.0.0.1', port=4455, password="")
            cl_request = obs.ReqClient()
            print('重连OBS~~~~~~~~~~~~')
            time.sleep(0.5)
            continue
        else:
            print('失败~~~~~~~~~~~')