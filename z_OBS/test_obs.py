import requests

obs_script_addr = "http://127.0.0.1:8899"  # OBS 脚本网址
# requests.get(url="%s/start" % obs_script_addr)  # 开始OBS的python脚本计时
requests.get(url="%s/period?term=666" % obs_script_addr)  # 开始OBS的python脚本计时