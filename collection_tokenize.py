from pymystem3 import Mystem
import nltk
from nltk.corpus import stopwords
import string
import xlrd
import xlsxwriter

list_stop_words = ['фильм', 'сезон', 'сериал', 'смотреть', 'кино', 'жизнь', 'будущее',
                   'чтиво', 'братья', 'гоблин', 'императрица', 'ци', 'властелин', 'кольцо',
                   'король', 'прикобчение', 'шерлок', 'холмс', 'доктор', 'ватсон', 'собака',
                   'баскервилей', 'хилер', 'гладиатор', 'интерстеллар', 'декалог', 'бесстыдники',
                   'мама', 'братство', 'гнездо', 'кукушка', 'игра', 'дживс', 'вустер', 'лодка',
                   'крестный', 'карта', 'деньги', 'ствол', 'куш', 'рука', 'престиж', 'джентельмен',
                   'город', 'мужчина', 'твин', 'пикс', 'рыцарь', 'стул', 'зеркало', 'остров',
                   'матрица', 'запах', 'клубника', 'джаз', 'жизнь', 'женщина', 'кавказ', 'пленница',
                   'шурик', 'королевство', 'энн', 'пробуждение', 'легенда', 'аватар', 'аанга', 'побег',
                   'шоушенк', 'дом', 'мальчик', 'девочка', 'невеста', 'фарго', 'потомок', 'ликвидация',
                   'больница', 'симпсоны', 'никербокер', 'вир', 'зара', 'борода', 'ветер', 'повелитель',
                   'москва', 'слеза', 'охота', 'охотник', 'судьба', 'агры', 'север', 'юг', 'слышать',
                   'мэш', 'капитан', 'хатико', 'ван', 'гог', 'винсент', 'завтра', 'человек', 'пираты',
                   'кариба', 'карибского', 'море', 'рождество', 'ягнят', 'паддингтона', 'балто',
                   'книга', 'аббат', 'даунтон', 'бригада', 'зверополис', 'терминатор', 'валли', 'суд',
                   'физика', 'джейн', 'эйр', 'декстер', 'мюнхгаузен', 'спартак', 'хоббит', 'хористы',
                   'лагуна', 'дневник', 'путь', 'бруклин', 'век', 'трумана', 'хилтон', 'карпов',
                   'пиноккио', 'саймон', 'магазин', 'блэк', 'ромео', 'джульетта', 'босс']

# искать подстроку Названиефильма в строке ,для удаления
#удалить смиволы код которых не равен буквенным и пробельным символам
def Process(text):
    stop_words = stopwords.words('russian')
    mystem = Mystem()
    doc = nltk.word_tokenize(text)  # токенизация (разбиение на слова и знаки препинание) предложений
    new_doc = [word for word in doc if word not in string.punctuation]  # удаление пунктуационных символов
    new_doc = [i for i in new_doc if (i not in stop_words)]  # удаление стоп-слов (с помощью stop_words.extend([]) можно расширить словарь стоп-слов
    lemmas = mystem.lemmatize(' '.join(new_doc))
    return(''.join(lemmas))

rb = xlrd.open_workbook('CommentAllStyleDelNegative.xlsx')

wb = xlsxwriter.Workbook('CommentTokenize7.xlsx')
#ws_positive = wb.add_worksheet('Positive')
#ws_neutral = wb.add_worksheet('Neutral')
ws_negative = wb.add_worksheet('Negative')

#sheet_positive = rb.sheet_by_index(0)
#sheet_neutral = rb.sheet_by_index(1)
sheet_negative = rb.sheet_by_index(1)

for i in range(0,1500):#range(sheet_positive.nrows): #ориентир по количеству negative
    #positive = Process(sheet_positive.row_values(i)[0])
    #neutral = Process(sheet_neutral.row_values(i)[1])
    negative = Process(sheet_negative.row_values(i)[0])
    #ws_positive.write(i, 0, positive)
    #ws_neutral.write(i, 0, neutral)
    ws_negative.write(i, 0, negative)
wb.close()
