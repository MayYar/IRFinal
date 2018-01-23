__author__ = 'Administrator'
import sys
import ijson
import jieba
import jieba.posseg as pseg
import time
import pymysql
# ["B", "A", "C", "B", "A", "C", "A", "A", "B", "B", "B", "C", "C", "A", "A", "B", "B", "B", "B", "B"]
try:
	conn= pymysql.connect(host='localhost', port=3306, user='root', passwd='root1234',charset='UTF8')
	cur=conn.cursor()                              #獲取一個游標對象
	cur.execute("USE test")   #創建資料庫
	# cur.execute("SELECT * FROM all_word")
	# data=cur.fetchall()

	# for row in data:
	#     col0 = row[0]
	#     col1 = row[1]
	#     print('%s\t%s' %(col0, col1))

	f = open('question_easy.json', 'rb')

	print("loading json")
	objects = ijson.items(f, 'item')
	print("loading done")
	num = 0
	start = time.strftime("%Y/%m/%d %H:%M")

	for question in objects:
			num += 1
			print('question'+str(num)+':')
			query = question['Question']
			words = pseg.cut(query)
			# word_list = []
			sumA = 0
			sumB = 0
			sumC = 0
			#先將每題ABC選項的list找出來
			sqlA = "SELECT docs FROM all_word where word = '%s'" % (str(question['A']))
			cur.execute(sqlA)
			data=cur.fetchall()
			for rowA in data:
				spA = set(rowA[0].split(","))

			sqlB = "SELECT docs FROM all_word where word = '%s'" % (str(question['B']))
			cur.execute(sqlB)
			data=cur.fetchall()
			for rowB in data:
				spB = set(rowB[0].split(","))

			sqlC = "SELECT docs FROM all_word where word = '%s'" % (str(question['C']))
			cur.execute(sqlC)
			data=cur.fetchall()
			for rowC in data:
				spC = set(rowC[0].split(","))

			#比對每個斷出詞彙跟各選項的docs交集
			for word in words:

				if str(word.flag)[0] == 'n':
					# word_list.append(str(word.word))
					# print(str(word.word) + "\\" + str(word.flag) + '\n', end=' ')
					sql = "SELECT docs FROM all_word where word = '%s'" % (str(word.word))
					cur.execute(sql)
					data=cur.fetchall()
					for rowW in data:
						sp = set(rowW[0].split(","))
						
					# print(len(set(sp) & set(sp1)))
					sumA += len(sp.intersection(spA))
					sumB += len(sp.intersection(spB))
					sumC += len(sp.intersection(spC))
			# print(question['A'] + ': %d' % sumA)
			# print(question['B'] + ': %d' % sumB)
			# print(question['C'] + ': %d' % sumC)
			print('\n')
			
			# wiki = open('question.json', 'rb')
			# documents = ijson.items(wiki, 'item')
			# for doc in objects:
				# if question['A'] == doc['title']:
				# 	count += 1
				# 	content = doc['content']
				# 	words = pseg.cut(content)
				# 	for word in words:
				# 		if str(word.flag)[0]=='n' and str(word.word) in word_list:
				# 			a += 1
				# elif question['B'] == doc['title']:
				# 	count += 1
				# 	content = doc['content']
				# 	words = pseg.cut(content)
				# 	for word in words:
				# 		if str(word.flag)[0]=='n' and str(word.word) in word_list:
				# 			b += 1
				# elif question['C'] == doc['title']:
				# 	count += 1
				# 	content = doc['content']
				# 	words = pseg.cut(content)
				# 	for word in words:
				# 		if str(word.flag)[0]=='n' and str(word.word) in word_list:
				# 			c += 1
				# elif count == 3:
				# 	break;
			#比大小
			list_ans = [sumA,sumB,sumC]
			print(list_ans.index(max(list_ans)), end=', ')
			# print(max(list_ans))
			end = time.strftime("%Y/%m/%d %H:%M")
			# print('start = '+start+' end = '+end)
			print('\n')
			# wiki.close()
	f.close()

	cur.close()                                    #關閉游標
	conn.commit()                                  #向資料庫中提交任何未解決的事務，對不支持事務的資料庫不進行任何操作
	conn.close()                                   #關閉到資料庫的連接，釋放資料庫資源
except Exception :print("發生異常")