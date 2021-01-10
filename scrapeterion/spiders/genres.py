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

        genres = [{'key': key, 'name': name} for [key, name] in zip(genre_keys, genre_names)]
        directors = [{'key': key, 'name': name} for [key, name] in zip(director_keys, director_names)]
        yield {
            'genres': genres,
            'directors': directors
        }
