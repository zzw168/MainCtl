import json
import time

import requests

url = 'https://marble-api.kaj789.com'

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Authorization': 'Bearer L8yUwg1wljco3j57u59XdkGKalrK0NtTMX1ok8fSCSYBVj5Vdu',
}


def test_server(Track_number='I'):
    GET_term_url = '/forecast/%s' % Track_number  # 取得期号，开始时间，结束时间，运行时长
    response = requests.get('%s%s' % (url, GET_term_url), headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        return True
    else:
        return False


def get_term(Track_number='I'):  # 取期号
    GET_term_url = '/v2/forecast/%s' % Track_number  # 取得期号，开始时间，结束时间，运行时长
    response = requests.get('%s%s' % (url, GET_term_url), headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print('获取期号失败！')
        return None


def post_start(term, betting_start_time, Track_number='I'):  # 开始比赛
    POST_start_url = '/start'  # 比赛开始信号
    POST_start_data = {"raceTrackID": Track_number, "term": str(term), "actualStartTime": betting_start_time}
    print(POST_start_data)
    response = requests.post('%s%s' % (url, POST_start_url), headers=headers, json=POST_start_data)
    print('start:', response.content)
    return response.content


def post_end(term, betting_end_time, status=1, Track_number='I'):  # 结束比赛
    POST_end_url = '/end'
    POST_end_data = {"raceTrackID": Track_number, "term": str(term), "actualEndTime": betting_end_time,
                     "status": status}  # 1: 正常, 0: 不正常
    print(POST_end_data)
    response = requests.post('%s%s' % (url, POST_end_url), headers=headers, json=POST_end_data)
    print('end:', response.content)
    return response.content


def post_result(term, betting_end_time, result_data='', Track_number='I'):  # 发送赛果
    POST_result_url = '/result'
    if result_data != '':
        POST_result_data = result_data
    else:
        POST_result_data = {"raceTrackID": Track_number, "term": str(term), "actualResultOpeningTime": betting_end_time,
                            "result": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                            "timings": json.dumps([
                                {"pm": 1, "id": 1, "time": 120.11},
                                {"pm": 2, "id": 2, "time": 122.73},
                                {"pm": 3, "id": 3, "time": 123.24},
                                {"pm": 4, "id": 4, "time": 125.89},
                                {"pm": 5, "id": 5, "time": 126.01},
                                {"pm": 6, "id": 6, "time": 128.27},
                                {"pm": 7, "id": 7, "time": 129.35},
                                {"pm": 8, "id": 8, "time": 130.98},
                                {"pm": 9, "id": 9, "time": 130.99},
                                {"pm": 10, "id": 10, "time": 131.22}])}
    response = requests.post('%s%s' % (url, POST_result_url), headers=headers, json=POST_result_data)
    print(POST_result_data)
    print('result:', response.text)
    return response.text


def post_upload(term, img_path, Track_number='I'):  # 上传图片
    # upload_url = 'https://marble-api.hyypgs.com'
    POST_upload_url = '/upload/%s/%s' % (Track_number, term)
    with open(img_path, 'rb') as f:
        files = {'file': ('image.jpg', f, 'image/jpeg')}  # 创建上传文件对象
        response = requests.post('%s%s' % (url, POST_upload_url), files=files, headers=headers)
    print('upload:', response.text)
    return response.text


def post_marble_results(term, comments='Invalid Term', Track_number='I'):  # 比赛异常，上传这个结果取消比赛
    control_headers = {
        'Authorization': 'Bearer e8baaf8c-d6c2-4287-afbe-a95ae1eed235',
    }
    # comments = [Out Ball, Trap Ball,'Invalid Term']
    post_marble_results_url = 'https://control.kaj789.com/marbleResults'
    marble_results_data = {
        "raceTrackID": Track_number,
        "term": str(term),
        "comments": comments
    }
    response = requests.post(post_marble_results_url, headers=control_headers, json=marble_results_data)
    print(marble_results_data)
    print('marble_results:', response.text)
    return response.text


def get_marble_settings():  # 取得当前整体开盘情况
    GET_marble_settings_url = 'https://control.kaj789.com/marbleSettings'
    response = requests.get(GET_marble_settings_url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print('获取期号失败！')
        return None


def post_aiupload(term, ai_img_path, Track_number='I'):
    POST_aiupload_url = '/aiupload/%s/%s' % (Track_number, term)
    with open(ai_img_path, 'rb') as f:
        files = {'file': ('image.jpg', f, 'image/jpeg')}  # 创建上传文件对象
        response = requests.post('%s%s' % (url, POST_aiupload_url), headers=headers, files=files)
    print(response.text)
    return response.text


def get_stream(Track_number='I'):
    global stream_url
    GET_stream_url = '/stream/%s' % Track_number
    response = requests.get('%s%s' % (url, GET_stream_url), headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        stream_url = response.text
        print(stream_url)
        return stream_url
    else:
        print('获取流失败！')
        return False


def post_status(status=True, Track_number='I'):  # 发送开盘封盘状态，开盘了才能正常进行操作
    POST_status_url = '/status/%s' % Track_number
    POST_status_data = {"status": status}  # true: 正常, false: 不正常
    response = requests.post('%s%s' % (url, POST_status_url), headers=headers, json=POST_status_data)
    print(response.text)
    return response.text


if __name__ == '__main__':
    # get_marble_settings()
    # get_stream()
    # test_server()
    # post_status(True)
    get_term()
    # post_start(9613162, 1730369317)
    post_marble_results(9613183)
    # time.sleep(5)9613162
    # post_end(9613161, 1730369497)
    # post_upload('./1.png')
    # post_result(9613161, 1730369497)
    # post_status(False)
