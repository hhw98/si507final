import requests
import json
from bs4 import BeautifulSoup
import sqlite3

def get_movie_info(url):
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.find('h2').text
    #print(title)
    year = soup.find(class_='release_date').text
    #year = year_1.strip('(').strip(')')
    #print(year.strip('(').strip(')'))
    score = soup.find('div', class_='user_score_chart')['data-percent']
    if score == '0.0':
        score = '-'
    #print(score)
    #print(type(score))
    try:
        overview = soup.find('div', class_='overview').find('p').text
    except:
        overview = soup.find('div', class_='overview').find('li').text
        #print(title)
    #print(overview)
    people = soup.find('ol',class_='people no_image').find_all('li')
    director_list = []
    for a in people:
        #print(a.find('p').text)
        if a.find('p').text == "We don't have any crew added to this movie. You can help by adding some!":
            director_info = {'Director': '-', 'Known For':'-', 'Gender':'-', 'Known Credits':'-',
                            'Birthday':'-', 'Place of Birth':'-'}
            director_list.append(director_info)
            break
        p = a.find_all('p')
        if 'Director' in p[1].text:
            #Director = p[0].text
            end_url = p[0].find('a').get('href')
            people_url = base_url+end_url
            people_text = requests.get(people_url).text
            people_soup = BeautifulSoup(people_text, 'html.parser')
            Director = people_soup.find('h2').text
            #print('Director: '+Director)
            #bio = people_soup.find(class_='biography false')
            #print('biography', bio)
            people_info = people_soup.find(class_='grey_column').find_all('strong')
            for pi in people_info:
                if pi.text == 'Known For':
                    KnownFor = pi.parent.contents[1]
                    #print('Known For',pi.parent.contents[1])
                if pi.text == 'Gender':
                    Gender = pi.parent.contents[1]
                    #print('Gender',pi.parent.contents[1])
                if pi.text == 'Known Credits':
                    KnownCredits = pi.parent.contents[1]
                    #print('Known Credits',pi.parent.contents[1])
                if pi.text == 'Birthday':
                    Birthday = pi.parent.contents[1]
                    #print('Birthday',pi.parent.contents[1])
                if pi.text == 'Place of Birth':
                    PlaceofBirth = pi.parent.contents[1]
                    #print('Place of Birth',pi.parent.contents[1])
            director_info = {'Director': Director, 'Known For':KnownFor, 'Gender':Gender, 'Known Credits':KnownCredits,
                            'Birthday':Birthday, 'Place of Birth':PlaceofBirth}
            director_list.append(director_info)
    info = soup.find('section',class_='facts left_column').find_all('strong')
    for i in info:
        if i.text == 'Original Language':
            Language = i.parent.contents[1]
            #print('language',Language)
        if i.text == 'Runtime':
            duration = i.parent.contents[1]
            #print('Runtime',duration)
        if i.text == 'Budget':
            Budget = i.parent.contents[1]
            #print('Budget',i.Budget)
        if i.text == 'Revenue':
            Revenue = i.parent.contents[1]
            #print('Revenue',Revenue)
    genres = soup.find('section',class_='genres right_column').find_all('li')
    genre_list = []
    for g in genres:
        #if g not in find_genre:
            #find_genre.append(g.text)
        genre_list.append(g.text)
        #print('genre',g.text)
    genre = ','.join(genre_list)
    keywords = soup.find('section',class_='keywords right_column').find_all('li')
    keyword_list = []
    for k in keywords:
        #if k not in find_keyword:
            #find_keyword.append(k.text)
        keyword_list.append(k.text)
        #print('keyword',k.text)
    keyword = ','.join(keyword_list)
    movie_info = {'MovieTitle': title, 'Year':year, 'Score':score, 'overview':overview, 'Original Language':Language,
                'duration':duration, 'Budget':Budget, 'Revenue':Revenue,'genres':genre,'keyword':keyword, 'director_info':director_list}
    #print()
    CSV_Dict[url] = movie_info
    dumped_json_cache = json.dumps(CSV_Dict,indent = 4,separators=(',', ':'))
    with open('movieinfo.json', 'w') as f:
        f.write(dumped_json_cache)
        return CSV_Dict[url]
def main():
    DBNAME = 'movie_info.db'
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        DROP TABLE IF EXISTS 'Movies';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Directors';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Movie_Genres';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Movie_Keywords';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Movie_Director';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Movie_Genre';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Movie_Keyword';
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Movies'(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'MovieTitle' TEXT NOT NULL,
        'Overview' TEXT NOT NULL,
        'Score' REAL NOT NULL,
        'Language' TEXT NOT NULL,
        'Duration' TEXT NOT NULL,
        'Year' TEXT NOT NULL,
        'Budget' REAL NOT NULL,
        'Revenue' REAL NOT NULL
        );
        '''
#        'DirectorId' INTEGER NOT NULL,
#        'GenreId' INTEGER NOT NULL,
#        'KeywordId' INTEGER NOT NULL
    cur.execute(statement)

    statement = '''
    CREATE TABLE 'Directors'(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'DirectorName' TEXT NOT NULL,
        'KnownFor' TEXT NOT NULL,
        'Gender' INTEGER NOT NULL,
        'KnownCredits' TEXT NOT NULL,
        'Birthday' TEXT NOT NULL,
        'PlaceOfBirth' TEXT NOT NULL
    );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Movie_Genres'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'GenreName' TEXT NOT NULL
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Movie_Keywords'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'KeywordName' TEXT NOT NULL
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Movie_Director'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'MovieId' INTEGER NOT NULL,
            'DirectorId' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Movie_Genre'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'MovieId' INTEGER NOT NULL,
            'GenreId' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Movie_Keyword'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'MovieId' INTEGER NOT NULL,
            'KeywordId' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)

        #print(people)

    for i in range(50):
        i = i+1
        #print('page',i)
        end_url = '/movie?page='+ str(i)
        base_url = 'https://www.themoviedb.org'
        page_text = requests.get(base_url + end_url).text
        page_soup = BeautifulSoup(page_text, 'html.parser')
        titles = page_soup.find_all(class_='title result')
        for a in titles:
            #print(type(a.text))
            #movietitle = (a.text,)
            #s = '''SELECT COUNT(*) FROM Movies WHERE MovieTitle = ?'''
            #cur.execute(s, movietitle)
            #for row in cur:
                #if int(row[0]) == 0:
            end_url = a.get('href')
            url = base_url + end_url
            try:
                with open('movieinfo.json', encoding='utf-8') as f:
                    CSV_contents = f.read()
                    CSV_Dict = json.loads(CSV_contents)
            except:
                CSV_Dict = {}
            #find_genre = []
            #find_keyword = []
            if url in CSV_Dict:
                #print("Getting cached data...")
                content = CSV_Dict.get(url)
            else:
                #print('request online...')
                content = get_movie_info(url)
            #insert data into database
            try:
                score = float(content['Score'])
                budget = float(content['Budget'].strip(' $').replace(",",""))
                revenue = float(content['Revenue'].strip(' $').replace(",",""))
            except:
                continue
            for ele in content['director_info']:
                statement = '''SELECT COUNT(*) FROM Directors WHERE DirectorName = ?'''
                cur.execute(statement, (ele['Director'],))
                for row in cur:
                    if row[0] == 0:
                        D = []
                        statement = '''INSERT INTO Directors (DirectorName, KnownFor, Gender, KnownCredits, Birthday, PlaceOfBirth)'''
                        statement += '''VALUES(?,?,?,?,?,?) '''
                        D = [ele['Director'],ele['Known For'],ele['Gender'],ele['Known Credits'],ele['Birthday'], ele['Place of Birth']]
                        cur.execute(statement,D)
            M = []
            statement = '''INSERT INTO Movies (MovieTitle, Overview, Score, Language,Duration,Year, Budget, Revenue)'''
            statement += '''VALUES(?,?,?,?,?,?,?,?) '''
            try:
                score = float(content['Score'])
                budget = float(content['Budget'].strip(' $').replace(",",""))
                revenue = float(content['Revenue'].strip(' $').replace(",",""))
            except:
                continue
            M = [content['MovieTitle'],content['overview'],score,content['Original Language'],content['duration'],content['Year'].strip('(').strip(')'),budget,revenue]
            cur.execute(statement,M)
            statement = '''SELECT Id FROM Movies WHERE MovieTitle = ?'''
            cur.execute(statement, (content['MovieTitle'],))
            result = cur.fetchall()
            for row in result:
                movieid = row[0]
            #print(MovieId)
            statement = '''SELECT Id FROM Directors WHERE DirectorName = ?'''
            directorid = []
            for ele in content['director_info']:
                cur.execute(statement, (ele['Director'],))
                result = cur.fetchall()
                for row in result:
                    directorid.append(row[0])
            #print(results)
            for ele in directorid:
                mdR = []
                statement = '''INSERT INTO Movie_Director (MovieId, DirectorId)'''
                statement += '''VALUES(?,?) '''
                mdR = [movieid,ele]
                cur.execute(statement,mdR)
            #insert genres table
            if content['genres'] == '':
                pass
            else:
                genre_list = content['genres'].split(',')
                for ele in genre_list:
                    statement = '''SELECT COUNT(*) FROM Movie_genres WHERE GenreName = ?'''
                    cur.execute(statement, (ele,))
                    for row in cur:
                        if row[0] == 0:
                            #insert into Genres table
                            G = []
                            statement = '''INSERT INTO Movie_Genres(GenreName)'''
                            statement +='''VALUES(?)'''
                            G = [ele]
                            cur.execute(statement, G)
                        else:
                            pass
            #insert keywords table
            if content['keyword'] == '':
                pass
            else:
                keyword_list = content['keyword'].split(',')
                for ele in keyword_list:
                    statement = '''SELECT COUNT(*) FROM Movie_Keywords WHERE KeywordName = ?'''
                    cur.execute(statement, (ele,))
                    for row in cur:
                        if row[0] == 0:
                            #insert into keywords table
                            K = []
                            statement = '''INSERT INTO Movie_Keywords(KeywordName)'''
                            statement +='''VALUES(?)'''
                            K = [ele]
                            cur.execute(statement, K)
                        else:
                            pass
            #insert into Movie_Genre relationship
            statement = '''SELECT Id FROM Movie_Genres WHERE GenreName = ?'''
            genreid = []
            for ele in genre_list:
                cur.execute(statement, (ele,))
                result = cur.fetchall()
                for row in result:
                    genreid.append(row[0])
            #print(genreid)
            for ele in genreid:
                mgR = []
                statement = '''INSERT INTO Movie_Genre (MovieId, GenreId)'''
                statement += '''VALUES(?,?) '''
                mgR = [movieid,ele]
                cur.execute(statement,mgR)
            #insert into Movie_Keyword relationship
            statement = '''SELECT Id FROM Movie_Keywords WHERE KeywordName = ?'''
            keywordid = []
            for ele in keyword_list:
                cur.execute(statement, (ele,))
                result = cur.fetchall()
                for row in result:
                    keywordid.append(row[0])
            #print(genreid)
            for ele in keywordid:
                mkR = []
                statement = '''INSERT INTO Movie_Keyword (MovieId, KeywordId)'''
                statement += '''VALUES(?,?) '''
                mkR = [movieid,ele]
                cur.execute(statement,mkR)
    conn.commit()
    conn.close()
            #for ele in content:
            #print(content['MovieTitle'])
if __name__ == '__main__':
    main()
#test
#SELECT * FROM Movies
#LEFT JOIN Movie_Director ON Movies.Id = Movie_Director.MovieId
#LEFT JOIN Directors ON Movie_Director.DirectorId = Directors.Id
#LEFT JOIN Movie_Genre ON Movies.Id = Movie_Genre.MovieId
#LEFT JOIN Movie_Genres ON Movie_Genre.GenreId = Movie_Genres.Id
#LEFT JOIN Movie_Keyword ON Movies.Id = Movie_Keyword.MovieId
#LEFT JOIN Movie_Keywords ON Movie_Keyword.KeywordId = Movie_Keywords.Id
#WHERE Movies.Id = 4
