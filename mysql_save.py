import mysql.connector
import configparser
from movie_info import Movie

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
sec = config.sections()

def info_to_data():
    return '''
    insert into minflix_db (title, synopsis, release_year, duration, maturity, genres, characteristic, actors, authors, producer, poster) 
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

class DBMySql:
    def __init__(self):
        DBMySql=[]
    def connectMysql(Movie):
        try:
            connection = mysql.connector.connect(user=config['MySQL']['USER'],
                                                passwd=config['MySQL']['PASSWORD'],
                                                host=config['MySQL']['LOCALHOST'],
                                                db=config['MySQL']['DATABASE'])
            if connection.is_connected() :
                print('연결될때')
                db_info = connection.get_server_info()
                print('MySQL server virsion : ', db_info)

                cursor = connection.cursor(prepared=True)
        
                print("=== create table if not exitsts minflix_test===")
                cursor.execute('''
                    create table if not exists minflix_db (
                        mno int(11) not null auto_increment primary key, 
                        title varchar(100) , 
                        synopsis text, 
                        release_year year(4), 
                        duration varchar(20), 
                        maturity varchar(20), 
                        genres text, 
                        characteristic text, 
                        actors text, 
                        authors varchar(300), 
                        producer varchar(100), 
                        poster varchar(400)
                    ) DEFAULT CHARSET=utf8mb4; 
                ''')
                print("===info_to_data===")
                cursor.execute(info_to_data(), (Movie.title, Movie.synopsis, Movie.year, Movie.duration, Movie.maturity, Movie.genres, Movie.characteristic, Movie.actors, Movie.authors, Movie.producer, Movie.poster))
                connection.commit()
                record = cursor.fetchone()
                print('Connected to DB : ', record)

        except Exception as e:
            print('DB Connection Error Occure : ' ,e)
        
        finally:
            cursor.close()
            connection.close()
            print('========== END MySQL Connection ==========')

