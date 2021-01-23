import scrapy
from urllib.parse import urlsplit, urlunsplit


# work in progress
def remove_query_string(url: str) -> str:
    return urlunsplit(urlsplit(url)._replace(query="", fragment=""))


def find_slug(url: str) -> str:
    path = urlsplit(url).path
    return path.strip('/').split('/')[-1]


class FilmsByGenreSpider(scrapy.Spider):
    name = 'films_by_genre'
    allowed_domains = ['films.criterionchannel.com']
    start_urls = ['https://films.criterionchannel.com/']

    def parse(self, response, **kwargs):
        genre_keys = response.css("input[name=genre]::attr(value)").getall()
        genre_names = response.css("label[for^=filter-genre]::text").getall()
        director_keys = response.css("input[name=director]::attr(value)").getall()
        director_names = response.css("label[for^=filter-director]::text").getall()

#        genres = [{'key': key, 'name': name} for [key, name] in zip(genre_keys, genre_names)]
#        directors = [{'key': key, 'name': name} for [key, name] in zip(director_keys, director_names)]
        for genre in genre_keys:
        # for genre in ['drama']:
            genre_url = f'{response.request.url}?genre={genre}'
            yield scrapy.Request(url=genre_url, callback=self.parse_by_genre, meta={'genre': genre})

        # yield {
        #     'genres': genres,
        #     'directors': directors
        # }

    def parse_by_genre(self, response, **kwargs):
        genre = response.meta.get('genre')
        movies = response.css('tr.criterion-channel__tr')
        for movie in movies:
            yield {
                'title': self.get_title(movie),
                'url': self.get_url(movie),
                'img': self.get_img(movie),
                'country': self.get_country(movie),
                'year': self.get_year(movie),
                'director': self.get_director(movie),
                'slug': self.get_slug(movie),
                'genre': genre
            }

    def get_title(self, movie):
        return self.select_text(
            movie, selector='.criterion-channel__td--title a::text')

    def get_url(self, movie):
        return self.select_text(
            movie, selector=':scope::attr(data-href)')

    def get_img(self, movie):
        url=self.select_text(
            movie, selector='.criterion-channel__film-img::attr(src)')

        return remove_query_string(url)

    def get_director(self, movie):
        return self.select_text(
            movie, selector='td.criterion-channel__td--director::text')

    def get_year(self, movie):
        return self.select_text(
            movie, selector='td.criterion-channel__td--year::text')

    def get_country(self, movie):
        return movie.css(
            '.criterion-channel__td--country span::text')[0].get()

    def get_slug(self, movie):
        url = self.get_url(movie)
        return find_slug(url)

    def select_text(self, movie, selector):
        return movie.css(selector).get().strip()
