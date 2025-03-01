import requests

obs_script_addr = "http://127.0.0.1:8899"  # OBS 脚本网址
# res = requests.get(url="%s/start" % obs_script_addr)
    #  res = requests.get(url="http://127.0.0.1:8899/stop")
    # res = requests.get(url="http://127.0.0.1:8899/reset")
res = requests.get(url='http://127.0.0.1:8899/period?period=12.23"')
# res = requests.get(url="http://127.0.0.1:8899/term?term=1223")