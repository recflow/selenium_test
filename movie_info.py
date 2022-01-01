class Movie:
    def __init__(self, title, synopsis, year, duration, maturity, genres, characteristic, actors, authors, producer, poster):
        self.title=title
        self.synopsis=synopsis
        self.year=year
        self.duration = duration
        self.maturity = maturity
        self.genres = genres
        self.characteristic = characteristic
        self.actors = actors
        self.authors = authors
        self.producer = producer
        self.poster = poster
        self.data=[]

    def printMovieInfo(self):
        print("제목: ", self.title)
        print("줄거리: ",self.synopsis)
        print("개봉연도: ", self.year)
        print("런닝 타임: " , self.duration)
        print("관람 연령: ", self.maturity)
        print("장르: ", self.genres)
        print("영화 특징: ", self.characteristic)
        print("배우: ", self.actors)
        print("각본: ", self.authors)
        print("감독: ", self.producer)
        print(self.poster)
