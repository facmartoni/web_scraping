import scrapy
from scrapy.crawler import CrawlerProcess


class Spider12(scrapy.Spider):

    name = 'spider12'
    allowed_domains = ['pagina12.com.ar']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'resultados_scrapy.json',
        'DEPTH_LIMIT': 2,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    start_urls = [
        'https://www.pagina12.com.ar/secciones/el-pais',
        'https://www.pagina12.com.ar/secciones/economia',
        'https://www.pagina12.com.ar/secciones/sociedad',
        'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
        'https://www.pagina12.com.ar/secciones/ciencia',
        'https://www.pagina12.com.ar/secciones/el-mundo',
        'https://www.pagina12.com.ar/secciones/deportes',
        'https://www.pagina12.com.ar/secciones/contratapa',
    ]

    def parse(self, response):

        # Artículo promocionado
        nota_promocionada = response.xpath(
            '//div[@class="featured-article__container"]/h2/a/@href').get()
        if nota_promocionada is not None:
            yield response.follow(nota_promocionada, callback=self.parse_nota)

        # Listado de notas
        notas = response.xpath(
            '//ul[@class="article-list"]//li//a/@href').getall()
        for nota in notas:
            yield response.follow(nota, callback=self.parse_nota)

        # Link a la siguiente página
        next_page = response.xpath('//a[@class="pagination-btn-next"]/@href')
        if next_page:
            yield(response.follow(next_page, callback=self.parse))

    def parse_nota(self, response):

        # Parseo de la nota
        title = response.xpath('//div[@class="article-title"]/text()').get()
        date = response.xpath('//span[@pubdate="pubdate"]/@datetime').get()
        summary = response.xpath(
            '//div[@class="article-summary"]/text()').get()
        prefix = response.xpath('//div[@class="article-prefix"]/text()').get()
        body = "\n\n".join(
            response.xpath(
                '//div[@class="article-body"]//@div[@class="article-text"//p/text()]').getall()
        )
        author = response.xpath(
            '//div[@class="article-author"]//span//a/text()').get()

        yield {
            'url': response.url,
            'title': title,
            'date': date,
            'summary': summary,
            'prefix': prefix,
            'body': body,
            'author': author,
        }


process = CrawlerProcess()
process.crawl(Spider12)
process.start()
