import xlwt
import xlrd
import collections
import math
import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM, SpatialDropout1D

from keras.preprocessing.text import Tokenizer #для предобработки текста

def select_word_for_dict(corpus_word):
    dictionary = []
    for word_one_text in corpus_word:
        for word in word_one_text:
            if word not in dictionary: #добавить проверку
                dictionary.append(word)
    return dictionary

def tf(document):
    tf_frequency = collections.Counter(document) #считает частотность терминов в документе
    for i in tf_frequency:
        tf_frequency[i] = tf_frequency[i]/float(len(document))
    return tf_frequency

def idf(words, list_of_document):
    idf_frequency = math.log2(len(list_of_document)/sum([1.0 for i in list_of_document if words in i]))
    return idf_frequency

def tf_idf(corpus): # можно пердать в аргементы еще словарь слов(по которым будет формироваться вектор текста)
    documet_list = []
    for text in corpus:
        tf_idf_dictionary = [] #{}
        computed_tf = tf(text)
        for word in computed_tf:  # а тут сделать цикл по этому словарю и тогда для слов с нулевым весовым коэффициентом будет автоматически прощитываться tf-idf
            tf_idf_dictionary.append(computed_tf[word] * idf(word,corpus))
            #tf_idf_dictionary[word] = computed_tf[word] * idf(word,corpus)
        documet_list.append(tf_idf_dictionary)
    return documet_list

rd_1=xlrd.open_workbook("D:\учеба\диплом\CommentAll.xlsx")
rd_2=xlrd.open_workbook("D:\учеба\диплом\CommentAllStyleDelNegative.xlsx")
sheet_0 = rd_1.sheet_by_index(0)
#sheet_1 = rd.sheet_by_index(1)
sheet_2 = rd_2.sheet_by_index(0)

array_0 = [sheet_0.row_values(rownum) for rownum in range(3800)]
#array_1 = [sheet_1.row_values(rownum) for rownum in range(350)]
array_2 = [sheet_2.row_values(rownum) for rownum in range(3800)]
array_text_train = [] #набор текстов двух классов
y_train=[]
for i in range(3000):
    array_text_train.append(array_0[i][0])
    y_train.append(1)
for i in range(3000):
    array_text_train.append(array_2[i][0])
    y_train.append(0)

y_test =[]
array_text_test = []

for i in range(800):
    array_text_test.append(array_0[i][0])
    y_test.append(1)
for i in range(800):
    array_text_test.append(array_2[i][0])
    y_test.append(0)

tokenizer = Tokenizer(lower=True, split=' ') # представление текста как списка слов с усечением знаковпрепинания и привееднием к нижнему регистру
tokenizer.fit_on_texts(array_text_test)
X_train = tokenizer.texts_to_matrix(mode='tfidf', texts=array_text_train)
X_test = tokenizer.texts_to_matrix(mode='tfidf', texts=array_text_test)

maxlen = 1000
X_train = sequence.pad_sequences(X_train,dtype=float,maxlen=maxlen)#обрезаем рецензии до длины maxlen
X_test = sequence.pad_sequences(X_test,dtype=float,maxlen=maxlen)
# выяснить почему pad_sequences после обработки выдает весовые коэффициенты каждого слова равным 0


y_train = np.ndarray(shape=(len(y_train)),buffer=np.array(y_train),dtype=int) #преобразование типа
y_test = np.ndarray(shape=(len(y_test)),buffer=np.array(y_test),dtype=int)

max_features = 5000
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
model.fit(X_train, y_train, batch_size=64, epochs=7, verbose=2)#,validation_data=(X_test, y_test))
# Проверяем качество обучения на тестовых данных
scores = model.evaluate(X_test, y_test,
                        batch_size=64)
print("Точность на тестовых данных: %.2f%%" % (scores[1] * 100))

