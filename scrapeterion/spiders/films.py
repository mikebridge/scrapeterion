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
    # start_urls = ['https://films.criterionchannel.com/']
    geo='US'

    def __init__(self, geo='US', **kwargs):
        if geo.upper() == 'CA':
            self.geo = 'CA'
            self.start_urls = [f'https://films.criterionchannel.com/?geo_availability=CA']
        else:
            self.geo = 'US'
            self.start_urls = [f'https://films.criterionchannel.com/']
        super().__init__(**kwargs)

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
                'slug': self.get_slug(movie),
                'geo': self.geo or 'US'
            }

    def get_title(self, movie):
        return self.select_text(
            movie, selector='.criterion-channel__td--title a::text')

    def get_url(self, movie):
        return self.select_text(
            movie, selector=':scope::attr(data-href)')

    def get_img(self, movie):
        url = self.select_text(
            movie, selector='.criterion-channel__film-img::attr(src)')

        return remove_query_string(url)

    def get_director(self, movie):
        return self.select_text(
            movie, selector='td.criterion-channel__td--director::text')

    def get_year(self, movie):
        return self.select_text(
            movie, selector='td.criterion-channel__td--year::text')

    def get_country(self, movie):
        country = movie.css(
            '.criterion-channel__td--country span::text')
        return country[0].get() if len(country) > 0 else 'Unknown'

    def get_slug(self, movie):
        url = self.get_url(movie)
        return find_slug(url)

    #def parse_film_page(self, response):
        #item = Film()
        # crawl the item and pass the item to the following request with *meta*
        #yield Request(url=item_detail_url, callback=self.parse_detail, meta=dict(item=item))

    # def parse_detail(self, response):
    #     # get the item from the previous passed meta
    #     item = response.meta['item']
    #     # keep populating the item
    #     yield item

    def select_text(self, movie, selector):
        return movie.css(selector).get().strip()
