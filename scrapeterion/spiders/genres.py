import scrapy


class GenresSpider(scrapy.Spider):
    name = 'genres'
    allowed_domains = ['films.criterionchannel.com']
    start_urls = ['https://films.criterionchannel.com/']

    def parse(self, response, **kwargs):
        genre_keys = response.css("input[name=genre]::attr(value)").getall()
        genre_names = response.css("label[for^=filter-genre]::text").getall()
        director_keys = response.css("input[name=director]::attr(value)").getall()
        director_names = response.css("label[for^=filter-director]::text").getall()

        genres = [{'slug': key, 'name': name} for [key, name] in zip(genre_keys, genre_names)]
        directors = [{'slug': key, 'name': name} for [key, name] in zip(director_keys, director_names)]
        for genre in genres:
            yield genre
        #yield {
        #    'genres': genres,
        #    'directors': directors
        #}
