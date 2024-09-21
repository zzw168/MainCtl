def deal_rank(integration_qiu_array, max_region_count, max_lap_count, ranking_array_, ball_sort_):
    for r_index in range(0, len(ranking_array_)):
        replaced = False
        for q_item in integration_qiu_array:
            if ranking_array_[r_index][5] == q_item[5]:  # 更新 ranking_array
                if q_item[6] < ranking_array_[r_index][6]:  # 处理圈数（上一次位置，和当前位置的差值大于等于12为一圈）
                    result_count = ranking_array_[r_index][6] - q_item[6]
                    if result_count >= max_region_count - 6:
                        ranking_array_[r_index][8] += 1
                        if ranking_array_[r_index][8] > max_lap_count - 1:
                            ranking_array_[r_index][8] = 0
                if ((ranking_array_[r_index][6] == 0)  # 等于0 刚初始化，未检测区域
                        or (q_item[6] >= ranking_array_[r_index][6] and  # 新位置要大于旧位置
                            (q_item[6] - ranking_array_[r_index][6] <= 3  # 新位置相差旧位置三个区域以内
                             or ranking_array_[0][6] - ranking_array_[r_index][
                                 6] > 5))  # 当新位置与旧位置超过3个区域，则旧位置与头名要超过5个区域才统计
                        or (q_item[6] < 8 and ranking_array_[r_index][6] >= max_region_count - 8)):  # 跨圈情况
                    for r_i in range(0, len(q_item)):
                        ranking_array_[r_index][r_i] = q_item[r_i]  # 更新 ranking_array
                    ranking_array_[r_index][9] = 1
                replaced = True
                break
        if not replaced:
            ranking_array_[r_index][9] = 0
    sort_ranking(ranking_array_, ball_sort_)


def sort_ranking(ranking_array_, ball_sort_):
    # 1.排序区域
    for i in range(0, len(ranking_array_)):  # 冒泡排序
        for j in range(0, len(ranking_array_) - i - 1):
            if ranking_array_[j][6] < ranking_array_[j + 1][6]:
                ranking_array_[j], ranking_array_[j + 1] = ranking_array_[j + 1], ranking_array_[j]
    # 2.区域内排序
    for i in range(0, len(ranking_array_)):  # 冒泡排序
        for j in range(0, len(ranking_array_) - i - 1):
            if ranking_array_[j][6] == ranking_array_[j + 1][6]:
                if ranking_array_[j][7] == 0:  # (左后->右前)
                    if ranking_array_[j][0] < ranking_array_[j + 1][0]:
                        ranking_array_[j], ranking_array_[j + 1] = ranking_array_[j + 1], ranking_array_[j]
                if ranking_array_[j][7] == 1:  # (左前<-右后)
                    if ranking_array_[j][0] > ranking_array_[j + 1][0]:
                        ranking_array_[j], ranking_array_[j + 1] = ranking_array_[j + 1], ranking_array_[j]
                if ranking_array_[j][7] == 10:  # (上前 ↑ 下后)
                    if ranking_array_[j][1] > ranking_array_[j + 1][1]:
                        ranking_array_[j], ranking_array_[j + 1] = ranking_array_[j + 1], ranking_array_[j]
                if ranking_array_[j][7] == 11:  # (上后 ↓ 下前)
                    if ranking_array_[j][1] < ranking_array_[j + 1][1]:
                        ranking_array_[j], ranking_array_[j + 1] = ranking_array_[j + 1], ranking_array_[j]
    # 3.圈数排序
    for i in range(0, len(ranking_array_)):  # 冒泡排序
        for j in range(0, len(ranking_array_) - i - 1):
            if ranking_array_[j][8] < ranking_array_[j + 1][8]:
                ranking_array_[j], ranking_array_[j + 1] = ranking_array_[j + 1], ranking_array_[j]
    # 4.寄存器保存固定每个区域的最新排位（因为ranking_array 变量会因实时动态变动，需要寄存器辅助固定每个区域排位）
    for i in range(0, len(ranking_array_)):
        if not (ranking_array_[i][5] in ball_sort_[ranking_array_[i][6]][ranking_array_[i][8]]):
            ball_sort_[ranking_array_[i][6]][ranking_array_[i][8]].append(ranking_array_[i][5])  # 添加寄存器球排序
            # if ranking_array[i][6] == 35 and ranking_array[i][8] == 1:
            #     print(ball_sort[ranking_array[i][6]][ranking_array[i][8]])
    # 5.按照寄存器位置，重新排序排名同圈数同区域内的球
    for i in range(0, len(ranking_array_)):
        for j in range(0, len(ranking_array_) - i - 1):
            if (ranking_array_[j][6] == ranking_array_[j + 1][6]) and (
                    ranking_array_[j][8] == ranking_array_[j + 1][8]):
                m = 0
                n = 0
                for k in range(0, len(ball_sort_[ranking_array_[j][6]][ranking_array_[j][8]])):
                    if ranking_array_[j][5] == ball_sort_[ranking_array_[j][6]][ranking_array_[j][8]][k]:
                        n = k
                    elif ranking_array_[j + 1][5] == ball_sort_[ranking_array_[j][6]][ranking_array_[j][8]][k]:
                        m = k
                if n > m:  # 把区域排位索引最小的球（即排名最前的球）放前面
                    ranking_array_[j], ranking_array_[j + 1] = ranking_array_[j + 1], ranking_array_[j]
    return ranking_array_, ball_sort_


def reset_ranking_array(init_array, max_lap_count, max_region_count, ):
    """
    重置排名数组
    # 前0~3是坐标↖↘,4=置信度，5=名称,6=赛道区域，7=方向排名,8=圈数,9=0不可见 1可见.
    """
    ranking_array_ = []  # 排名数组
    for i in range(0, len(init_array)):
        ranking_array_.append([])
        for j in range(0, len(init_array[i])):
            ranking_array_[i].append(init_array[i][j])
    ball_sort_ = []  # 位置寄存器
    for i in range(0, max_region_count + 1):
        ball_sort_.append([])
        for j in range(0, max_lap_count):
            ball_sort_[i].append([])
    con_data_ = []  # 排名数组
    for i in range(0, len(init_array)):
        con_data_.append([])
        for j in range(0, 5):
            con_data_[i].append([])
            if j == 0:
                con_data_[i][j] = init_array[i][5]  # con_data 数据表数组
            else:
                con_data_[i][j] = 0
    return ranking_array_, ball_sort_, con_data_


def to_num(res, init_array, z_response):
    arr_res = []
    for r in res:
        for i in range(0, len(init_array)):
            if r[0] == init_array[i][5]:
                arr_res.append(i + 1)
    for i in range(0, len(arr_res)):
        for j in range(0, len(z_response)):
            if arr_res[i] == z_response[j]:
                z_response[i], z_response[j] = z_response[j], z_response[i]
    return z_response
