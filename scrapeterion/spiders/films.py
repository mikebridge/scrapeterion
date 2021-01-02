import scrapy

class FilmsSpider(scrapy.Spider):
    # from w3lib.html import replace_escape_chars
    # yourloader.default_input_processor = MapCompose(relace_escape_chars)
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
                'year': self.get_year(movie)
            }

    def get_title(self, movie):
        return self.select_text(movie, selector='.criterion-channel__td--title a::text')

    def get_url(self, movie):
        return self.select_text(movie, selector=':scope::attr(data-href)')

    def get_img(self, movie):
        return self.select_text(movie, selector='.criterion-channel__film-img::attr(src)')

    def get_directory(self, movie):
        return self.select_text(movie, selector='td.criterion-channel__td--director::text')

    def get_year(self, movie):
        return self.select_text(movie, selector='td.criterion-channel__td--year::text')

    def get_country(self, movie):
        return movie.css('.criterion-channel__td--country span::text')[0].get()

    def select_text(self, movie, selector):
        return movie.css(selector).get().strip()

