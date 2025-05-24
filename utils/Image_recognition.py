import copy
import threading
import time

max_area_count = 68
balls_count = 8
max_lap_count = 2
ranking_time_start = 0
Track_number = 'I'
term = 8000

ball_sort_lock = threading.Lock()
ranking_lock = threading.Lock()

def deal_rank(integration_qiu_array):
    global ranking_array, ball_sort, lapTimes, lapTimes_thread, ranking_check

    area_limit = max_area_count / int(ui.lineEdit_area_limit.text())

    # 深拷贝全局状态以操作
    ranking_temp = copy.deepcopy(ranking_array)
    ball_sort_temp = copy.deepcopy(ball_sort)

    # 更新圈数、位置
    for r_index, ball in enumerate(ranking_temp):
        updated = False
        for q_item in integration_qiu_array:
            if ball[5] != q_item[5]:
                continue

            if handle_lap(ball, q_item, r_index, area_limit):
                pass  # 圈数更新逻辑封装

            if is_valid_update(ball, q_item, area_limit):
                if check_position_conflict(ranking_temp, q_item) or ball[6] != 1:
                    apply_position_update(ball, q_item)
                    ball[10] = 1
                else:
                    ball[10] = 0

            if r_index > 0 and q_item[6] <= max_area_count - balls_count:
                if abs(q_item[6] - ranking_temp[0][6]) < area_limit / 2:
                    if ranking_check[q_item[5]] == [-1, -1]:
                        ranking_check[q_item[5]] = [q_item[6], ball[9]]
                    if ball[6] != max_area_count - balls_count and ball[6] <= q_item[6]:
                        ball[9] = ranking_temp[0][9]
                    ball[10] = 1
            updated = True
            break

        if not updated:
            ball[10] = 1 if map_label_big.map_action >= len(map_label_big.path_points[0]) - 20 else 0

    # 将区域内排位寄存器更新
    for ball in ranking_temp:
        if len(ball_sort_temp) <= ball[6]:
            continue
        if ball[5] not in ball_sort_temp[ball[6]][ball[9]]:
            ball_sort_temp[ball[6]][ball[9]].append(ball[5])

    # 排序：圈数 > 区域 > 自定义方向 > 寄存器顺序
    def sort_key(ball):
        lap, area, direction = ball[9], ball[6], ball[7]
        try:
            reg_order = ball_sort_temp[area][lap].index(ball[5])
        except ValueError:
            reg_order = 999
        pos_score = ball[0] if direction in (0, 1) else ball[1]
        pos_score *= -1 if direction in (0, 11) else 1
        return (-lap, -area, pos_score, reg_order)

    ranking_temp_sorted = sorted(ranking_temp, key=sort_key)

    # 最终写回全局
    with ball_sort_lock:
        ball_sort = copy.deepcopy(ball_sort_temp)
    with ranking_lock:
        ranking_array = copy.deepcopy(ranking_temp_sorted)

def handle_lap(ball, q_item, r_index, area_limit):
    if ball[6] >= max_area_count - balls_count and ball[9] >= max_lap_count - 1 and r_index == 0:
        for b in ranking_array:
            if b[6] != max_area_count - balls_count:
                b[9] = max_lap_count - 1

    lap_condition = (
        (not ui.checkBox_end_2.isChecked() and q_item[6] < ball[6] < max_area_count - balls_count + 1)
        or (ui.checkBox_end_2.isChecked() and ball[9] < max_lap_count - 1 and q_item[6] < ball[6] < max_area_count + 1)
    )

    if lap_condition:
        passed_area = ball[6] - q_item[6]
        if passed_area >= max_area_count - area_limit - balls_count:
            if ball[9] == 0 and lapTimes[r_index] == 0:
                lapTimes[r_index] = round(time.time() - ranking_time_start, 2)
                thread = threading.Thread(
                    target=post_lapTime,
                    args=(term, r_index + 1, lapTimes[r_index], Track_number),
                    daemon=True
                )
                lapTimes_thread[r_index] = thread
                thread.start()
            if r_index == 0:
                for b in ranking_array:
                    ranking_check[b[5]] = [-1, -1]
            ball[6] = 0
            ball[9] += 1
            if ball[9] >= max_lap_count:
                ball[9] = max_lap_count - 1
        return True
    return False

def is_valid_update(old_ball, new_ball, area_limit):
    new_area = new_ball[6]
    old_area = old_ball[6]
    lap = old_ball[9]
    valid_basic = (
        old_area == 0 and new_area < area_limit or
        (max_area_count - balls_count >= new_area >= old_area and 0 <= new_area - old_area <= area_limit) or
        (
            ranking_check[new_ball[5]][0] != -1 and
            ranking_check[new_ball[5]][1] == lap and
            0 < new_area - ranking_check[new_ball[5]][0] < area_limit
            and ui.checkBox_First_Check.isChecked()
        )
    )
    valid_end = (
        new_area >= old_area >= max_area_count - area_limit - balls_count and
        new_area - old_area <= area_limit + balls_count and
        lap == max_lap_count - 1
    )
    return (valid_basic or valid_end) and new_area <= max_area_count

def check_position_conflict(ranking_temp, q_item):
    for b in ranking_temp:
        if abs(q_item[0] - b[0]) <= 7 and abs(q_item[1] - b[1]) <= 7:
            return False
    return True

def apply_position_update(ball, q_item):
    for idx in range(len(q_item)):
        ball[idx] = copy.deepcopy(q_item[idx])

def post_lapTime():
    pass