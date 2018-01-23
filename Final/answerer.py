import sys
import json
import getpass
import jieba
import jieba.posseg as pseg
import time
import pymysql
import math

pswd = getpass.getpass('enter password:')
database = input('enter database:')
quest_file = input('enter json file:')
try:
        db = pymysql.connect(host='localhost', user='root', passwd=pswd, db=database, charset='utf8')
        cursor = db.cursor()
except:
        print('wrong password or wrong database')

try:
        with open(quest_file, 'r', encoding='utf8') as f:
                questions = json.load(f)
except:
        print("file does not exist.")

num = 0
answer = []
start = time.strftime("%H:%M:%S")
jieba.set_dictionary('dict.txt')
ans_str = ["A", "B", "C"]
docNum = 873045

for question in questions:
        num += 1
        query = question['Question']
        words = pseg.cut(query)
        word_tf = {}
        word_set = {}
        word_weight = {}
        count = 0

        print('question'+str(num)+':')
        for word in words:
            word_str = word.word
            if str(word.flag)[0] == 'n' and word_str not in word_tf:
                if cursor.execute("select docs from inverted_table where word='%s'" % (word_str)):
                    count += 1
                    word_tf[word_str] = 1

                    row = cursor.fetchone()[0]
                    docList = row.split(';')
                    word_docs = set()
                    for doc in docList:
                        if len(doc) > 1:
                            word_docs.add(doc.split(':')[0])
                    word_set[word_str] = word_docs
            elif word_str in word_tf:
                count += 1
                word_tf[word_str] += 1

        for word in iter(word_tf):
            tf = word_tf[word] / count
            idf = math.log10(docNum / len(word_set[word]))
            word_weight[word] = tf*idf

        ans_score = [0, 0, 0]
        ans_list = [question['A'], question['B'], question['C']]

        for i in range(3):
            docs = set()
            doc_ansNum = {}
            if cursor.execute("select docs from inverted_table where word='%s'" % (ans_list[i])):
                data = cursor.fetchone()[0]
                temp = data.split(';')
                for word in temp:
                    if len(word) > 1:
                        term = word.split(':')
                        docs.add(term[0])
                        doc_ansNum[term[0]] = int(term[1])
            '''else:
                ans_words = pseg.cut(ans_list[i])
                for word in ans_words:
                    print(str(word))
                    if cursor.execute("select docs from inverted_table where word='%s'" % (str(word.word))):
                        data = cursor.fetchone()[0]
                        temp = set(data.split(';'))
                        for word in temp:
                            docs.add(word.split(':')[0])'''
            for word in iter(word_weight):
                if len(word_set[word]) < 30000:
                    docAmount = len(docs)
                    matchDoc = docs & word_set[word]
                    for doc in matchDoc:
                        cursor.execute('select amount from wordnums where docID=' + doc)
                        docWordNum = int(cursor.fetchone()[0])
                        tf = doc_ansNum[doc] / docWordNum
                        idf = math.log10(docNum / docAmount)
                        ans_score[i] += word_weight[word] * tf * idf


        print (ans_score)
        temp_ans = ans_str[ans_score.index(max(ans_score))]
        answer.append(temp_ans)
        print ('\n')

json_ans = json.dumps(answer)
print(json_ans)

print('start = ' + start + '\tend = ' + time.strftime("%H:%M:%S"))
f.close()
db.close()

input('press enter to exit...')
