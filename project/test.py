import unittest
from part1 import *
from part2 import *

class TestDatabase(unittest.TestCase):

    def test_movies_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT MovieTitle FROM Movies'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Incredibles 2',), result_list)
        self.assertEqual(len(result_list), 734)

        sql = '''
            SELECT MovieTitle, Score, Language FROM Movies
            WHERE Year="2000"
            ORDER BY Overview DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 6)
        self.assertEqual(result_list[2][0],"The Emperor's New Groove")

        conn.close()
    def test_director_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT DirectorName
            FROM Directors
            WHERE KnownFor=" Directing"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Michael Sucsy',), result_list)
        self.assertEqual(len(result_list), 293)

        sql = '''
            SELECT COUNT(*)
            FROM Directors
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertTrue(count == 463)

        conn.close()
    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
        SELECT MovieTitle, DirectorName FROM Movies
        LEFT JOIN Movie_Director ON Movies.Id = Movie_Director.MovieId
        LEFT JOIN Directors ON Movie_Director.DirectorId = Directors.Id
        WHERE MovieTitle = 'John Wick'
        ORDER BY DirectorName DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        for row in result_list:
            self.assertEqual(len(result_list), 2)
            self.assertEqual(result_list[1][1], 'Chad Stahelski')
        sql = '''
        SELECT MovieTitle, GenreName FROM Movies
        LEFT JOIN Movie_Genre ON Movies.Id = Movie_Genre.MovieId
        LEFT JOIN Movie_Genres ON Movie_Genre.GenreId = Movie_Genres.Id
        WHERE MovieTitle = 'John Wick'
        ORDER BY GenreName ASC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        for row in result_list:
            self.assertEqual(len(result_list), 2)
            self.assertEqual(result_list[0][1], 'Action')
        sql = '''
        SELECT MovieTitle, KeywordName FROM Movies
        LEFT JOIN Movie_Keyword ON Movies.Id = Movie_Keyword.MovieId
        LEFT JOIN Movie_Keywords ON Movie_Keyword.KeywordId = Movie_Keywords.Id
        WHERE MovieTitle = 'John Wick'
        ORDER BY KeywordName ASC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        for row in result_list:
            self.assertEqual(len(result_list), 11)
            self.assertEqual(result_list[10][1], 'widower')
        #self.assertIn(('US',), result_list)
        conn.close()
class TestMovieSearch(unittest.TestCase):

    def test_movie_search(self):
        response = 'list;movietitle=Maze Runner: The Death Cure'
        year_info=[]
        genre_info=[]
        results = interactive_prompt(response,year_info,genre_info)
        self.assertEqual(results[1], 'Wes Ball')
        self.assertEqual(results[0], 'Maze Runner: The Death Cure')
        self.assertEqual(results[3], '2018')
        self.assertIn('Action', results[4])

class TestDirectorSearch(unittest.TestCase):

    def test_director_search(self):
        response = 'list;director=J.J. Abrams'
        year_info=[]
        genre_info=[]
        results = interactive_prompt(response,year_info,genre_info)
        self.assertEqual(results[3].strip(), '1966-06-27')
        result_list = results[5].split('\n')
        self.assertEqual(len(result_list), 3)
        self.assertIn('Mission: Impossible III', results[5])
        self.assertIn('Star Trek Into Darkness', results[5])
        self.assertIn('Star Trek', results[5])

class TestGenreSearch(unittest.TestCase):

    def test_genre_search(self):
        #response = 'plot;genre=Action'
        #test plot
        #interactive_prompt(response)
        response = 'list;genre=Action'
        year_info=[]
        genre_info=[]
        results = interactive_prompt(response,year_info,genre_info)
        self.assertEqual(results, True)
        response = 'plot;genre=Action'
        #test plot
        results = interactive_prompt(response,year_info,genre_info)
        response = 'list;year=1997'
        items = interactive_prompt(response,results.get('genre'),genre_info)
        #print(items)
        self.assertEqual(len(items), 5)
        self.assertIn('The Fifth Element', items)

class TestYearSearch(unittest.TestCase):

    def test_year_search(self):
        response = 'list;year=2001'
        year_info=[]
        genre_info=[]
        results = interactive_prompt(response,year_info,genre_info)
        self.assertEqual(results, True)

        response = 'plot;year=2008'
        #test plot
        results = interactive_prompt(response,year_info,genre_info)
        response = 'list;genre=Action'
        items = interactive_prompt(response,year_info,results.get('year'))
        #print(items)
        self.assertEqual(len(items), 9)
        self.assertIn('Indiana Jones and the Kingdom of the Crystal Skull', items)

unittest.main()
