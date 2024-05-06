import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None

QUESTIONS = [
    ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
    ('Каким станет зелёный утёс, если упадёт в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
    ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
    ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
    ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
    ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')
]
victotine = [
    ("Природа",),("Жизнь",),("Геометрия",)
]
content = [
    (1,1),(2,1),(3,2),(5,2),(4,3),(6,3)
]

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def do_many(query, db):
    cursor.executemany(query, db)
    conn.commit()

def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

def f_q():
    open()
    do_many('''
INSERT INTO question (question,true_answer,false_answer_1,
false_answer_2,false_answer_3) VALUES (?,?,?,?,?)
''', QUESTIONS)
    close()

def f_quiz():
    open()
    do_many('''
INSERT INTO quiz (quiz) VALUES (?)
''', victotine )
    close()

def f_c():
    open()
    do_many('''
INSERT INTO quiz_content (question_id, quiz_id) VALUES (?,?)
''',  content)
    close()

def g_q():
        open()
        do(
        '''SELECT question.question,question.true_answer,question.false_answer_1,
        question.false_answer_2,
        question.false_answer_3
        FROM quiz_content, question
        WHERE quiz_content.question_id == question.id
        AND quiz_content.quiz_id == 3'''
    )
        print(cursor.fetchall())
        close()
    
def create():
    open()
    do('''CREATE TABLE IF NOT EXISTS question(
       id INTEGER PRIMARY KEY,
       question TEXT,
       true_answer TEXT,
       false_answer_1 TEXT,
       false_answer_2 TEXT,
       false_answer_3 TEXT
    )''')
    do('''CREATE TABLE IF NOT EXISTS quiz(
       id INTEGER PRIMARY KEY,
       quiz TEXT
    )''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content(
       id INTEGER PRIMARY KEY,
       question_id INTEGER,
       quiz_id INTEGER,
       FOREIGN KEY (quiz_id) REFERENCES quiz (id),
       FOREIGN KEY (question_id) REFERENCES question (id)
    )''')
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    f_q()
    f_quiz()
    f_c()
    g_q()
    #show_tables()

if __name__ == "__main__":
    main()
