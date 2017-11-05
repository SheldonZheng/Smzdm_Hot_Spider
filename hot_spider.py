import requests
import time
import json
from bs4 import BeautifulSoup
import re
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import hashlib
import pymysql

database_ip_and_port = '???'
database_name = '???'
database_username = 'root'
database_password = '???'

smtp_server_ip = '???'
mail_username = '???'
mail_password = '???'

target_mail_address = ['???']

sock = '???'


def send_mail(data,title):
    smtp_server = smtp_server_ip
    username = mail_username
    password = mail_password
    to_addr = target_mail_address
    msg = MIMEText(data, 'plain', 'utf-8')
    msg['From'] = 'SMZDM爬虫'
    msg['To'] = 'Target'
    msg['Subject'] = Header('SMZDM热门榜更新; ' + 'title:' + title , 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 587)
    server.set_debuglevel(1)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, [to_addr], msg.as_string())
    server.quit()

def md5(str):
    print(str)
    m = hashlib.md5()
    m.update(str.encode(encoding='utf-8'))
    return m.hexdigest()

def is_data_existed(result):
    db = pymysql.connect(database_ip_and_port, database_username, database_password, database_name)
    cursor = db.cursor()
    tempResult = sorted(result.items(), key=lambda result: result[0])
    sql = "SELECT * FROM smzdm_hot_record where md5 = '%s'" % \
          md5(str(tempResult))

    print(md5(str(tempResult)))
    try:
        cursor.execute(sql)
        print(cursor.rowcount)
        if cursor.rowcount > 0 :
            return False
        else:
            return True
    except:
        db.rollback()

    db.close()

def insert_data(result):
    db = pymysql.connect(database_ip_and_port, database_username, database_password, database_name)
    db.set_charset('utf8')
    cursor = db.cursor()
    tempResult = sorted(result.items(), key=lambda result: result[0])
    sql = "INSERT INTO smzdm_hot_record(title,price,page_url,md5) VALUES ('%s','%s','%s','%s')" % \
          (result['title'],result['price'],result['page_url'],md5(str(tempResult)))

    try:
        cursor.execute(sql)
        db.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        db.rollback()

    db.close()

def push_wechat(data,key,title):
    url = 'https://sc.ftqq.com/%s.send' % sock
    payload = {'text' : 'SMZDM_Spider,key:%s,title:%s' % (key,title),'desp':data}
    requests.post(url,data=payload,verify=False)



def get_real_time_data():
    c_time = int(time.time())
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': 'www.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    url = 'https://www.smzdm.com/top/'
    r = requests.get(url=url, headers=headers)

    data = r.text
    # print (data)
    soup = BeautifulSoup(data, 'html5lib')
    re1 = '(\'floor\':\'好价品类榜\')'  # Command Seperated Values 1
    re2 = '.*?'  # Non-greedy match on filler
    re3 = '(\'tab\')'  # Single Quote String 1
    re4 = '.*?'  # Non-greedy match on filler
    re5 = '(\'全部\')'  # Single Quote String 2

    class_result = soup.find_all(attrs={"class": "feed-hot-card"})
    # count = 0
    result_list = []
    for str in class_result:
        a = str.find_all('a')[0];
        price_span = str.find_all('span', attrs={"class": "z-highlight"})[0]
        con1 = a['onclick'];
        if re.search(re1 + re2 + re3 + re4 + re5, con1) != None:
            print(str)
            title = str.find_all(attrs={"class": "feed-hot-title"})[0].string
            href = a['href']
            price = price_span.text
            result = {
                'title' : title,
                'price' : price,
                'page_url' : href
            }
            result_list.append(result)
            # print(title)
            # print(href)
            # print(price)
    return result_list

if __name__ == '__main__':
    result_list = get_real_time_data()
    print(result_list)
    for result in result_list:
        if is_data_existed(result):
            send_mail(str(result),result['title'])
            insert_data(result)