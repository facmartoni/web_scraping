import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse

URL = 'https://platzi.com'


class SpiderPlatzi(scrapy.Spider):
    name = 'platzi-spider'
    allowed_domains = ['platzi.com']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'resultados_platzi.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    start_urls = [
        URL + '/categorias/desarrollo/',
        URL + '/categorias/marketing/',
        URL + '/categorias/negocios/',
        URL + '/categorias/diseno/',
        URL + '/categorias/produccion-audiovisual/',
        URL + '/categorias/crecimiento-profesional/',
    ]

    def parse(self, response):
        carrers_items = response.xpath(
            '//a[@class="CarrersItem"]/@href').getall()
        if carrers_items:
            for carrera in carrers_items:
                yield response.follow(carrera, callback=self.parse_carrera)

    def parse_carrera(self, response):
        route_title = response.xpath(
            '//div[@class="Hero-route-title"]/h1/text()').get()
        route_items = response.xpath('//div[@class="route-item"]').getall()
        route_items_list = []
        for route_item in route_items:
            route_item_html = HtmlResponse(
                url="", body=route_item, encoding='utf-8')
            badge = route_item_html.xpath(
                '//div[@class="route-item-badge"]//img/@src').extract()[0]
            name = route_item_html.xpath(
                '//div[@class="route-item-name"]//h4/text()').extract()[0]
            course_url = route_item_html.xpath(
                '//a/@href').extract()[0]
            route_items_list.append({
                'badge': badge,
                'name': name,
                'url': URL + course_url,
            })
        yield {
            'route-title': route_title,
            'courses': route_items_list,
        }


process = CrawlerProcess()
process.crawl(SpiderPlatzi)
process.start()
