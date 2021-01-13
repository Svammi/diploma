import requests
import xlsxwriter
from bs4 import BeautifulSoup
import time
from multiprocessing import Manager
from multiprocessing import Process

def comment_text(url):
    time.sleep(5)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    #'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    comment_block = []
    while (len(comment_block) == 0):
        r = requests.get(url, headers=headers) #requests.get(url, timeout=(10, 0.01))
        soup = BeautifulSoup(r.text, 'lxml')
        comment_block = soup.find_all('div', class_='review__content')

    list_text_tag_p = []
    list_comment = []
    for block in comment_block:
        teg_p = block.find('div', class_='review__text').find_all('p')
        for i in teg_p:
            list_text_tag_p.append(i.text)
        comment = ' '.join(list_text_tag_p)
        list_text_tag_p = []
        list_comment.append(comment)
    return list_comment

def search_positiv_comment(positive_link, positive):
    for link in positive_link:
        list_ = comment_text(link)
        for text in list_:
            positive.append(text)

def search_negative_comment(negative_link, negative):
    for link in negative_link:
        list_ = comment_text(link)
        for text in list_:
            negative.append(text)

def search_neutral_comment(neutral_link,comment):#, ws_neutral):
    for link in neutral_link:
        list_ = comment_text(link)
        for text in list_:
            comment.append(text)

if __name__ == "__main__":
    url = 'https://plus.kinopoisk.ru/catalogue/?page=125'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    list_film = []
    while (len(list_film) == 0):
        #time.sleep(5)
        r = requests.get(url, headers = headers) #получаем html страницу
        soup = BeautifulSoup(r.text, 'lxml')
        list_film = soup.find_all('div', class_='film-snippet')
        print('Connect...')

    print("Connect is succssesful!")
    
    list_link = []
    list_name_film = []
    for film in list_film:
        link = film.find('header', class_='film-snippet__content-header').find('a').get('href')
        name = film.find('header', class_='film-snippet__content-header').find_all('span', class_='film-snippet__title')
        list_link.append(link)            #список ссылок на фильм не отформаттированный
        for title in name:
            list_name_film.append(title.text)

    name = 'details/reviews/'
    positive_link = []
    #neutral_link = []
    negative_link = []

    for link in list_link:
        positive_link.append(link + name + 'positive/')
       # neutral_link.append(link + name + 'neutral/')
        negative_link.append(link + name + 'negative/')

    wb = xlsxwriter.Workbook('Comment125.xlsx')
    #ws_positive = wb.add_worksheet('Positive')
    #ws_neutral = wb.add_worksheet('Neutral')
    ws_negative = wb.add_worksheet('Negative')
    ws_name = wb.add_worksheet('Name_Film')

    for i in range(len(list_name_film)-1):
        ws_name.write(i, 0, list_name_film[i])

    m = Manager()
    #neutral = m.list()
    negative = m.list()
    positive = m.list()

    #proc_neutral = Process(target=search_neutral_comment, args=(neutral_link,neutral,))
    proc_negative = Process(target=search_negative_comment, args=(negative_link, negative,))
    proc_positive = Process(target=search_positiv_comment, args=(positive_link, positive,))

    proc_negative.start()
    #proc_neutral.start()
    proc_positive.start()

    proc_negative.join()
    #proc_neutral.join()
    proc_positive.join()

    k=0
    for i in range(len(negative) - 1):
        if negative[i] not in positive:
        #ws_negative.write(i, 0, i)
            ws_negative.write(k, 0, negative[i])
            k+=1

    wb.close()
    print('Connect the end')
'''
    for i in range(len(neutral)-1):
        ws_neutral.write(i,0,i)
        ws_neutral.write(i, 1, neutral[i])

    

    for i in range(len(positive)-1):
        ws_positive.write(i, 0, i)
        ws_positive.write(i, 1, positive[i])
'''


