from bottle import route, run, template, redirect, request
import db
import bayes
import scraputils


@route('/update_news')
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    upd_news = scraputils.get_news('https://www.itnews.com.au', 1)
    s = db.session()
    titles = s.query(db.News.title).filter(db.News.title.in_([d['title'] for d in upd_news])).all()
    bd_labels = []
    for title in titles:
        bd_labels.append(title[0])
    for current_new in upd_news:
        if current_new['title'] not in bd_labels:
            news = db.News(title=current_new['title'],
                           author=current_new['author'],
                           url=current_new['url'],
                           comments=current_new['comments'])
            s.add(news)
    s.commit()
    redirect('/news')


@route('/')
@route('/news')
def news_list():
    s = db.session()
    rows = s.query(db.News).filter(db.News.label == None).all()
    return template('news_template', rows=rows)


@route('/add_label/')
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    s = db.session()
    news_label = request.query.label
    news_id = request.query.id
    rows = s.query(db.News).filter(db.News.id == news_id)
    rows[0].label = news_label
    s.commit()
    redirect('/news')


@route('/getrecommendations')
def get_recommendations():
    s = db.session()
    rows = s.query(db.News).filter(db.News.label != None).all()
    x = []
    y = []
    for row in rows:
        x.append(row.title)
        y.append(row.label)
    bayesclassifier = bayes.NaiveBayesClassifier()
    bayesclassifier.fit(x, y)
    rows = s.query(db.News).filter(db.News.label == None).all()
    X = [row.title for row in rows]
    y = bayesclassifier.predict(X)
    for i, row in enumerate(rows):
            row.label = y[i]
    good, maybe, never = [], [], []
    for row in rows:
        if row.label == 'good':
            good.append(row)
        elif row.label == 'maybe':
            maybe.append(row)
        elif row.label == 'never':
            never.append(row)
    return template('news_recommendations', good=good, maybe=maybe, never=never)


if __name__ == '__main__':
    run(host='localhost', port=8080)


def add_db():  # Добавление 1000 новостей
    news_list_ = scraputils.get_news('https://www.itnews.com.au', 50)
    q = 0
    for k in news_list_:
        s = db.session()
        news_ = db.News(title=k.get('title'),
                        author=k.get('author'),
                        url=k.get('url'),
                        comments=k.get('comments')
                    )
        s.add(news_)
        s.commit()
        q += 1
        print("added news ", q)


def clean_label():  # Вспомогательная функция
    s = db.session()
    rows = s.query(db.News).filter(db.News.label != None).all()
    for row in rows:
        row.label = None
    s.commit()
