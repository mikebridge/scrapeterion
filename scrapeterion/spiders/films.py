import scrapy
from urllib.parse import urlsplit, urlunsplit


def remove_query_string(url: str) -> str:
    return urlunsplit(urlsplit(url)._replace(query="", fragment=""))


def find_slug(url: str) -> str:
    path = urlsplit(url).path
    return path.strip('/').split('/')[-1]


class FilmsSpider(scrapy.Spider):
    name = 'films'
    allowed_domains = ['films.criterionchannel.com']
    start_urls = ['https://films.criterionchannel.com/']

    def parse(self, response, **kwargs):
        movies = response.css('tr.criterion-channel__tr')
        for movie in movies:
            yield {
                'title': self.get_title(movie),
                'url': self.get_url(movie),
                'img': self.get_img(movie),
                'country': self.get_country(movie),
                'year': self.get_year(movie),
                'director': self.get_director(movie),
                'slug': self.get_slug(movie)
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
