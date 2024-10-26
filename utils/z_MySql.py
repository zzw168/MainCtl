import pymysql


def create_connection(host, user, password, database):
    """创建数据库连接。"""
    try:
        connection = pymysql.connect(
            host=host,  # 数据库主机地址
            user=user,  # 数据库用户名
            password=password,  # 数据库密码
            database=database,  # 数据库名称
            port=3306,  # 如非默认端口，可更改
            charset="utf8mb4"
        )
        print("数据库连接成功！")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


def execute_query(connection, query, params=None):
    """执行插入、更新或删除的 SQL 语句。"""
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query executed successfully")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")


def fetch_query(connection, query, params=None):
    """执行 SELECT 查询并获取结果。"""
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None

# if __name__ == "__main__":
#     # 创建数据库连接
#     conn = create_connection("192.168.0.80", "root", "root", "dataini")
#
#     if conn:
#         local_ip = tool_unit.check_network_with_ip()
#
#         # 查询配置表的 SQL 语句
#         user_value = local_ip[1]  # 网卡号
#         key_value = "电压输出%"  # 读取字段
#         key_value2 = "网络摄像机%"  # 读取字段
#         key_value3 = "赛道名称%"  # 读取字段
#         key_value4 = "图像识别IP"  # 读取字段
#         key_value5 = "全局配置.IP%"  # 读取字段
#
#         # select_query = "SELECT * FROM config WHERE `user`=%s AND `key`=%s"
#         select_query = ("SELECT * FROM config WHERE `user`=%s "
#                         "AND (`key` LIKE %s "
#                         "OR `key` LIKE %s "
#                         "OR `key` LIKE %s "
#                         "OR `key` = %s "
#                         "OR `key` LIKE %s)")
#         res = fetch_query(conn, select_query,
#                           [user_value,
#                            key_value,
#                            key_value2,
#                            key_value3,
#                            key_value4,
#                            key_value5])
#         print("Query Results:", type(res), res)
#         for index in range(len(res)):
#             if res[index][3] != '0' and ('电压输出' in res[index][2]):
#                 print(res[index][2], res[index][3])
#             elif '网络摄像机' in res[index][2]:
#                 print(res[index][2], res[index][3])
#             elif '赛道名称' in res[index][2]:
#                 print(res[index][2], res[index][3])
#             elif '图像识别IP' in res[index][2]:
#                 print(res[index][2], res[index][3])
#             elif '全局配置.IP' in res[index][2]:
#                 print(res[index][2], res[index][3])
#
#         # # 示例：执行 INSERT 操作
#         # insert_query = "INSERT INTO users (name, age) VALUES (%s, %s)"
#         # execute_query(conn, insert_query, ("Alice", 30))
#         #
#         # # 示例：执行 UPDATE 操作
#         # update_query = "UPDATE users SET age = %s WHERE name = %s"
#         # execute_query(conn, update_query, (35, "Alice"))
#         #
#         # # 示例：执行 DELETE 操作
#         # delete_query = "DELETE FROM users WHERE name = %s"
#         # execute_query(conn, delete_query, ("Alice",))
#
#         # 关闭连接
#         conn.close()
