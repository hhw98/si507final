import sqlite3 as sqlite
from prettytable import PrettyTable
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import secret

FLICKR_KEY = secret.FLICKR_KEY
MAPBOX_TOKEN = secret.MAPBOX_TOKEN
PLOTLY_USERNAME = secret.PLOTLY_USERNAME
PLOTLY_API_KEY = secret.PLOTLY_API_KEY

plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)

DBNAME = 'movie_info.db'
def drawtable(table):
    output = ''
    for item in table[0]:
        output += '|'+str(item)+' '
    output += "\n---------------------------------------------------------"
    for item in table[1:]:
        print('\n')
        print(item)
def get_movie_info(movie_name):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT MovieTitle, DirectorName, Score, Year, GenreName, KeywordName FROM Movies '
    statement += 'LEFT JOIN Movie_Director ON Movies.Id = Movie_Director.MovieId '
    statement += 'LEFT JOIN Directors ON Movie_Director.DirectorId = Directors.Id '
    statement += 'LEFT JOIN Movie_Genre ON Movies.Id = Movie_Genre.MovieId '
    statement += 'LEFT JOIN Movie_Genres ON Movie_Genre.GenreId = Movie_Genres.Id '
    statement += 'LEFT JOIN Movie_Keyword ON Movies.Id = Movie_Keyword.MovieId '
    statement += 'LEFT JOIN Movie_Keywords ON Movie_Keyword.KeywordId = Movie_Keywords.Id '
    statement += 'WHERE Movies.MovieTitle = ?'
    cur.execute(statement,(movie_name,))
    Director = []
    Genre = []
    Keyword = []
    for row in cur:
        Movietitle = row[0]
        if row[1] not in Director:
            Director.append(row[1])
        Score = row[2]
        Year = row[3]
        if row[4] not in Genre:
            Genre.append(row[4])
        if row[5] not in Keyword:
            Keyword.append(row[5])
    director = '\n'.join(Director)
    genre = '\n'.join(Genre)
    keyword = '\n'.join(Keyword)
    t = PrettyTable(['MovieTitle', 'DirectorName', 'Score', 'Year', 'GenreName', 'Keyword'])
    try:
        t.add_row([Movietitle,director,Score,Year,genre,keyword])
    except:
        pass
    print(t)
    conn.close()
    return [Movietitle,director,Score,Year,genre,keyword]
    #drawtable(output)
def get_director_info(director):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT DirectorName, KnownFor, Gender, Birthday, PlaceOfBirth, MovieTitle FROM Movies '
    statement += 'LEFT JOIN Movie_Director ON Movies.Id = Movie_Director.MovieId '
    statement += 'LEFT JOIN Directors ON Movie_Director.DirectorId = Directors.Id '
    statement += 'LEFT JOIN Movie_Genre ON Movies.Id = Movie_Genre.MovieId '
    statement += 'LEFT JOIN Movie_Genres ON Movie_Genre.GenreId = Movie_Genres.Id '
    statement += 'LEFT JOIN Movie_Keyword ON Movies.Id = Movie_Keyword.MovieId '
    statement += 'LEFT JOIN Movie_Keywords ON Movie_Keyword.KeywordId = Movie_Keywords.Id '
    statement += 'WHERE DirectorName = ?'
    cur.execute(statement,(director,))
    Title = []
    for row in cur:
        DirectorName = row[0]
        KnownFor = row[1]
        Gender = row[2]
        Birthday = row[3]
        PlaceOfBirth = row[4]
        if row[5] not in Title:
            Title.append(row[5])
    movietitle = '\n'.join(Title)
    t = PrettyTable(['DirectorName', 'KnownFor', 'Gender', 'Birthday', 'PlaceOfBirth','DirectedMovie'])
    try:
        t.add_row([DirectorName,KnownFor,Gender,Birthday,PlaceOfBirth,movietitle])
    except:
        pass
    print(t)
    conn.close()
    return [DirectorName,KnownFor,Gender,Birthday,PlaceOfBirth,movietitle]
def get_genre_info(genre):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT COUNT(*),Year, {}, {}, {} FROM Movies '.format('ROUND(AVG(Score),1)','ROUND(AVG(Budget),1)', 'ROUND(AVG(Revenue),1)')
    #statement = 'SELECT MovieTitle, Year, Score, Revenue, Budget FROM Movies '
    statement += 'LEFT JOIN Movie_Genre ON Movies.Id = Movie_Genre.MovieId '
    statement += 'LEFT JOIN Movie_Genres ON Movie_Genre.GenreId = Movie_Genres.Id '
    statement += 'WHERE GenreName = ? '
    #statement += 'AND Year = 2008 '
    statement += 'GROUP BY Year '
    statement += 'HAVING COUNT(*) > 3'

    cur.execute(statement,(genre,))
    num = []
    year = []
    ave_score = []
    ave_budget_ratio = []
    ave_budget = []
    for row in cur:
        num.append(row[0])
        year.append(row[1])
        ave_score.append(float(row[2])/100)
        ave_budget_ratio.append(float(row[3])/float(row[4]))
        #if row[4] not in ave_budget:
            #ave_score.append(row[4])
    statement = 'SELECT MovieTitle, Year FROM Movies '
    #statement = 'SELECT COUNT(*), GenreName FROM Movies '
    statement += 'LEFT JOIN Movie_Genre ON Movies.Id = Movie_Genre.MovieId '
    statement += 'LEFT JOIN Movie_Genres ON Movie_Genre.GenreId = Movie_Genres.Id '
    statement += 'WHERE GenreName = ? '
    cur.execute(statement,(genre,))
    result = cur.fetchall()
    t = PrettyTable(year)
    try:
        t.add_row(num)
    except:
        pass
    print(t)
    trace1 = go.Scatter(
        x = year,
        y = ave_score,
        name = 'ave_score',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4,
            dash = 'dot')
    )
    trace2 = go.Scatter(
        x = year,
        y = ave_budget_ratio,
        name = 'ave_budget_ratio',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4,
            dash = 'dot') # dash options include 'dash', 'dot', and 'dashdot'
    )
    data = [trace1, trace2]
    # Edit the layout
    layout = dict(title = 'Annual average score and budget ratio for {} movies'.format(genre),
                xaxis = dict(title = 'year'),
                yaxis = dict(title = 'Average score and budget ratio'),
              )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='movie-genre')
    conn.close()
    return result
def get_year_info(year):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    statement = 'SELECT COUNT(*), GenreName, {}, {}, {} FROM Movies '.format('ROUND(AVG(Score),1)','ROUND(AVG(Budget),1)', 'ROUND(AVG(Revenue),1)')
    #statement = 'SELECT COUNT(*), GenreName FROM Movies '
    statement += 'LEFT JOIN Movie_Genre ON Movies.Id = Movie_Genre.MovieId '
    statement += 'LEFT JOIN Movie_Genres ON Movie_Genre.GenreId = Movie_Genres.Id '
    statement += 'WHERE Year = ? '
    #statement += 'AND Year = 2008 '
    statement += 'GROUP BY GenreName '
    #statement += 'HAVING Year = 2018'

    cur.execute(statement,(year,))
    ave_score = []
    ave_budget_ratio = []
    genre = []
    num = []
    for row in cur:
        num.append(row[0])
        genre.append(row[1])
        ave_score.append(float(row[2])/100)
        ave_budget_ratio.append(float(row[3])/float(row[4]))
    statement = 'SELECT MovieTitle, GenreName FROM Movies '
    #statement = 'SELECT COUNT(*), GenreName FROM Movies '
    statement += 'LEFT JOIN Movie_Genre ON Movies.Id = Movie_Genre.MovieId '
    statement += 'LEFT JOIN Movie_Genres ON Movie_Genre.GenreId = Movie_Genres.Id '
    statement += 'WHERE Year = ? '
    cur.execute(statement,(year,))
    result = cur.fetchall()
    t = PrettyTable(genre)
    try:
        t.add_row(num)
    except:
        pass
    print(t)
    trace1 = go.Scatter(
        x = genre,
        y = ave_score,
        name = 'ave_score',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4,
            dash = 'dot')
    )
    trace2 = go.Scatter(
        x = genre,
        y = ave_budget_ratio,
        name = 'ave_budget_ratio',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4,
            dash = 'dot') # dash options include 'dash', 'dot', and 'dashdot'
    )
    data = [trace1, trace2]
    # Edit the layout
    layout = dict(title = 'Average score and budget ratio for {}'.format(year),
                xaxis = dict(title = 'genre'),
                yaxis = dict(title = 'Average score and budget ratio'),
              )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='movie-year')
    conn.close()
    return result
def load_help_TEXT():
    with open('help.txt') as f:
        return f.read()

def interactive_prompt(response):
    help_TEXT = load_help_TEXT()
    if response == 'help':
        print(help_TEXT)
        results = True
    elif len(response) == 0:
        results = True
    elif response == 'exit':
        print('bye')
        return False
    else:
        #response.split("'") list'movietitle=hello'
        command = response.split(";")
        if command[0] == 'list':
            if command[1].split('=')[0] == 'movietitle':
                results = get_movie_info(command[1].split('=')[1])
            elif command[1].split('=')[0] == 'director':
                results = get_director_info(command[1].split('=')[1])
            elif command[1].split('=')[0] == 'genre':
                try:
                    item = []
                    for ele in year_info:
                        if ele[1] == command[1].split('=')[1].capitalize():
                            item.append(ele[0])
                    g = PrettyTable([command[1].split('=')[1]])
                    for i in item:
                        try:
                            g.add_row([i])
                        except:
                            pass
                    print(g)
                except:
                    print('list year info first\n')
                #year_info = []
                #genre_info = get_genre_info(command[1].split('=')[1])
                results =item
            elif command[1].split('=')[0] == 'year':
                try:
                    item = []
                    for ele in genre_info:
                        if ele[1] == command[1].split('=')[1].capitalize():
                            item.append(ele[0])

                    y = PrettyTable([command[1].split('=')[1]])
                    for i in item:
                        try:
                            y.add_row([i])
                        except:
                            pass
                    print(y)
                    
                except:
                    print('list genre info first\n')
                genre_info = []
                results =item
            else:
                print('wrong command\n')
                results = True
        elif command[0] == 'plot':
            if command[1].split('=')[0] == 'genre':
                genre_info = get_genre_info(command[1].split('=')[1])
                results = genre_info
            elif command[1].split('=')[0] == 'year':
                year_info = get_year_info(command[1].split('=')[1])
                results = year_info
        else:
            print('wrong input\n')
            results = True
    return results
#mName = input("Enter a movie name: ")
#get_movie_info(mName)

#dName = input("Enter a movie director name: ")
#get_director_info(dName)

#genre = input("Enter a genre: ")
#genre_info = get_genre_info(genre)

#year = input("Enter a year: ")
#year_info = get_year_info(year)
#item = []
#for ele in year_info:
#    if ele[1] == 'Action':
#        item.append(ele[0])

#t = PrettyTable(['Action'])
#for i in item:
#    try:
#        t.add_row([i])
#    except:
#        pass
#print(t)

if __name__=="__main__":
    flag = True
    while flag:
        response = input('Enter a command\n ')
        flag = interactive_prompt(response)
