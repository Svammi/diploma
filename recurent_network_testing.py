import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM, SpatialDropout1D
from keras.datasets import imdb
import xlwt
import xlrd
import collections
#создает частотный словарь, упорядачивает его по частоте встречаемости слова и (если необходимо) обрезает словарь до указанного значения num_words
# аргументы: список текстов, представленных как список слов; длина частотного словаря
def select_dict(corpus,num_words=None):
    frequency_dict={}
    for text in corpus:
        for word in text:
            if frequency_dict.get(word)==None:
                frequency_dict.update({word: 1})
            else:
                frequency_dict[word] = frequency_dict.get(word) + 1

    if num_words!=None:
        i=0
        sort_frequency_dict={}
        for w in sorted(frequency_dict, key=frequency_dict.get, reverse=True): #упорядочиваем словарб по частоте встречаемости слов
            if i<num_words:
                sort_frequency_dict.update({w:frequency_dict[w]})
            i+=1
        return sort_frequency_dict
    return frequency_dict

#векторное представление текста на основе частотного словаря
def vector_model_text(corpus,dict):
    for index_text,text in enumerate(corpus):
        for index_word,word in enumerate(text):
            corpus[index_text][index_word] = dict[word]
    return corpus

# Устанавливаем seed для повторяемости результатов
np.random.seed(42)
# Максимальное количество слов (по частоте использования)
max_features = 5000
# Максимальная длина рецензии в словах
maxlen = 80

rd=xlrd.open_workbook("CommentTokenize.xlsx")
sheet_0 = rd.sheet_by_index(0)
#sheet_1 = rd.sheet_by_index(1)
sheet_2 = rd.sheet_by_index(1)
#считываем каждый класс рецензий
array_positive = [sheet_0.row_values(rownum) for rownum in range(3800)]
#array_neutral = [sheet_1.row_values(rownum) for rownum in range(450)]
array_negative = [sheet_2.row_values(rownum) for rownum in range(3800)]
#создаем обучающую коллекцию данных, где каждый текст представлен в виде набора слов (ДЛЯ ПОЗИТИВНЫХ И НЕГАТИВНЫХ ОТЗЫВОВ)
array_text_train=[] # массив обучающих текстов
y_train=[]# массив классов ассоциированных с обучающими текстами
array_text_test=[]
y_test=[]
for i in range(3000):
    array_text_train.append(array_positive[i][0].split(' ')) #представление текстов как список слов
    y_train.append(1) #класс с позитивными рецензиями определяется как 1
for i in range(3000):
    array_text_train.append(array_negative[i][0].split(' '))
    y_train.append(0)#класс с негативными рецензиями определяется как 0

for i in range(800):
    array_text_test.append(array_positive[3000+i][0].split(' '))
    y_test.append(1)
for i in range(800):
    array_text_test.append(array_negative[3000+i][0].split(' '))
    y_test.append(0)

frequency_dict = select_dict(np.concatenate((array_text_train,array_text_test),axis=0), max_features) #урезанный частотный словарь
#P.S. при усечении словаря возникает ошибка,что текст не возможно представить в векторном виде из-за отсутствия слов в словаре
X_train = vector_model_text(array_text_train,frequency_dict) #векторное представление текста
X_test = vector_model_text(array_text_test,frequency_dict)

X_train = sequence.pad_sequences(X_train, maxlen=maxlen)#обрезаем рецензии до длины maxlen
X_test = sequence.pad_sequences(X_test, maxlen=maxlen)

y_train = np.ndarray(shape=(len(y_train)),buffer=np.array(y_train),dtype=int) #преобразование типа
y_test = np.ndarray(shape=(len(y_test)),buffer=np.array(y_test),dtype=int)

# Создаем сеть
model = Sequential()
# Слой для векторного представления слов
model.add(Embedding(max_features, 32))
model.add(SpatialDropout1D(0.2))
# Слой долго-краткосрочной памяти
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
# Полносвязный слой
model.add(Dense(1, activation="sigmoid"))

# Копмилируем модель
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Обучаем модель
model.fit(X_train, y_train, batch_size=64,validation_data=(X_test, y_test),epochs=7, verbose=2)
# Проверяем качество обучения на тестовых данных
scores = model.evaluate(X_test, y_test,
                        batch_size=64)
print("Точность на тестовых данных: %.2f%%" % (scores[1] * 100))

