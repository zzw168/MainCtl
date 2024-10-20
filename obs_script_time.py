import obspython as obs  # 安装包 pip install obspy
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import urllib.parse

from datetime import datetime, timezone

source_name = ""
start_time = 0
end_time = 0
running = False
server = None


# HTTP Request Handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global running, start_time, end_time
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            path = parsed_path.path
            print("path1", path, type(query_params))
            if path == '/start':
                start_time = obs.os_gettime_ns() // 1000000
                print("start_time", start_time)
                running = True
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Timer started")
            elif path == '/stop':
                running = False
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response_text = f"End Time: {end_time}"
                # Handle request parameters
                if 'time' in query_params:
                    param_value = int(query_params['time'][0])
                    stop_timer(param_value)

                self.wfile.write(response_text.encode('utf-8'))
            elif path == '/reset':
                running = False
                restart_time()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Timer reset")
            elif path == '/period':

                running = False
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response_text = f"End Time: {end_time}"
                # Handle request parameters
                term = ' '
                if 'term' in query_params:
                    term = str(query_params['term'][0])
                update_period_text(term)
                self.wfile.write(b"Send Term")
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Not Found")
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_message = f"Internal Server Error: {str(e)}"
            self.wfile.write(error_message.encode('utf-8'))
            import traceback
            traceback.print_exc()

    def log_message(self, format, *args):
        pass  # Override to disable logging


# Start HTTP Server in a separate thread
def start_http_server():
    global server
    try:
        server = HTTPServer(('localhost', 8899), RequestHandler)
        print("HTTP server started at port 8899")
        server.serve_forever()
    except Exception as e:
        print(f"Error starting server: {e}")


def stop_http_server():
    global server
    if server:
        server.shutdown()
        server.server_close()
        server = None


# OBS script description
def script_description():
    return "一个简单的毫秒计时器脚本，通过HTTP请求控制计时器的开始和停止。"


# OBS script properties
def script_properties():
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(props, "source_name", "选择文本源", obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in ["text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)
        obs.source_list_release(sources)
    return props


# OBS script update
def script_update(settings):
    global source_name
    source_name = obs.obs_data_get_string(settings, "source_name")
    # scene = obs.obs_frontend_get_scene_by_name(scene_name)
    # obs.obs_frontend_set_current_scene(scene)
    # obs.obs_source_release(scene)


# OBS script load
def script_load(settings):
    print("setting", settings)
    script_update(settings)
    obs.timer_add(update_timer, 10)  # 每100毫秒更新一次

    obs.timer_add(update_gmt_text, 1000)

    # update_timer()
    threading.Thread(target=start_http_server, daemon=True).start()


def script_unload():
    obs.timer_remove(update_timer)
    stop_http_server()
    obs.timer_remove(update_gmt_text)


def update_timer():
    global running, start_time, source_name, end_time
    try:
        if running:
            elapsed = obs.os_gettime_ns() // 1000000 - start_time
            end_time = elapsed
            seconds = elapsed // 1000
            milliseconds = (elapsed % 1000) // 10  # 将毫秒限制为两位
            if seconds > 999:
                seconds = 999
                milliseconds = 99

            timer_text = f"{seconds:02d}’{milliseconds:02d}"

            source = obs.obs_get_source_by_name(source_name)
            if source:
                settings = obs.obs_data_create()
                obs.obs_data_set_string(settings, "text", timer_text)
                obs.obs_source_update(source, settings)
                obs.obs_data_release(settings)
                obs.obs_source_release(source)
    except Exception as e:
        print(f"Error in update_timer: {e}")
        import traceback
        traceback.print_exc()


def stop_timer(timenow):
    global source_name
    try:
        elapsed = timenow
        seconds = elapsed // 1000
        milliseconds = (elapsed % 1000) // 10  # 将毫秒限制为两位
        if seconds > 99:
            seconds = 99
            milliseconds = 99
        print(f"Error in update_timer: {seconds}")
        timer_text = f"{seconds:02d}’{milliseconds:02d}"

        source = obs.obs_get_source_by_name(source_name)
        if source:
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", timer_text)
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)
            obs.obs_source_release(source)
    except Exception as e:
        print(f"Error in update_timer: {e}")
        import traceback
        traceback.print_exc()


def reset_time():
    global source_name
    timer_text = "00’00"
    source = obs.obs_get_source_by_name(source_name)
    if source:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", timer_text)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)


def script_defaults(settings):
    pass


def script_save(settings):
    pass


# 更新文本来源的函数
def update_gmt_text():
    source_name = "GMT"  # 这里是你的文本来源名称

    # 获取该来源
    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        # 获取当前的 GMT 时间
        gmt_time = datetime.now(timezone.utc).strftime("GMT %H:%M:%S")

        # 获取该来源的当前设置
        settings = obs.obs_source_get_settings(source)

        # 修改文本内容为 GMT 时间
        obs.obs_data_set_string(settings, "text", gmt_time)

        # 应用新的设置
        obs.obs_source_update(source, settings)

        # 释放资源
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
    else:
        print(f"来源 {source_name} 未找到")


# 修改文本来源的函数
def update_period_text(new_text):
    source_name = "period"  # 这里是你创建的来源名称

    # 获取该来源
    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        # 获取该来源的当前设置
        settings = obs.obs_source_get_settings(source)

        # 修改文本内容
        obs.obs_data_set_string(settings, "text", new_text)

        # 应用新的设置
        obs.obs_source_update(source, settings)

        # 释放资源
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
    else:
        print(f"来源 {source_name} 未找到")
