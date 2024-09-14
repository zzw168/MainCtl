import os

import yaml


def save_host():
    global host_list
    global d_time
    table = ui.tableWidget
    num = table.rowCount()
    colnum = table.columnCount()
    if num == 0:
        return
    host_list = []
    host = []
    d_time = []
    ischecked = []
    for i in range(0, num):
        host.append('rewriteDataList')
        d_time.append(table.item(i, 10).text())
        if table.cellWidget(i, 0).isChecked():
            ischecked.append("1")
        else:
            ischecked.append("0")
        for j in range(1, colnum - 1):
            # host.append(table.item(i, j).text())
            host.append("0" if table.item(i, j).text() == "" else table.item(i, j).text())

        h = {'dsID': 'HCRemoteMonitor', 'cmdType': 'command', 'cmdData': host}
        host_list.append(h)
        host = []
    print(host_list)

    file = "./Robot.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        robot_conf = yaml.safe_load(f)
        f.close()
        if ui.radioButton_2.isChecked():
            robot_conf['Tasks2'] = host_list
            robot_conf['d_time2'] = d_time
            robot_conf['ischecked2'] = ischecked
        elif ui.radioButton_3.isChecked():
            robot_conf['Tasks3'] = host_list
            robot_conf['d_time3'] = d_time
            robot_conf['ischecked3'] = ischecked
        else:
            robot_conf['Tasks'] = host_list
            robot_conf['d_time'] = d_time
            robot_conf['ischecked'] = ischecked
        print(robot_conf)

        with open(file, "w", encoding="utf-8") as f:
            yaml.dump(robot_conf, f, allow_unicode=True)
            ui.textBrowser_msg.setText("保存服务器完成")