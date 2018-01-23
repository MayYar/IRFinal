__author__ = 'Administrator'
import pymysql
try:

    conn= pymysql.connect(host='localhost', port=3306, user='root', passwd='root1234',charset='UTF8')
    # conn=pymysql.connect(host='localhost',user='root',passwd='root1234',db='bookdb')
    cur=conn.cursor()                              #獲取一個游標對象
    # cur.execute("CREATE DATABASE test15")          #執行對應的SQL語句
    cur.execute("USE test")   #創建資料庫
    # cur.execute("CREATE TABLE users (id INT, name VARCHAR(18))")#創建表
    # cur.execute("INSERT INTO users VALUES(1, 'blog'),(2, 'csdn'),(3, 'net'),(4, 'a359680405')")#插入數據

    cur.execute("SELECT * FROM all_word")
    data=cur.fetchall()

    for row in data:
        col0 = row[0]
        col1 = row[1]
        print('%s\t%s' %(col0, col1))



    cur.close()                                    #關閉游標
    conn.commit()                                  #向資料庫中提交任何未解決的事務，對不支持事務的資料庫不進行任何操作
    conn.close()                                   #關閉到資料庫的連接，釋放資料庫資源
except Exception :print("發生異常")