import scrapy
from itemloaders import ItemLoader

from ..items import PeriodicElementItem
from scrapy_playwright.page import PageMethod


# no longer necessary since the pipeline takes care of it (run: scrapy crawl periodic_elements -O elements.json)
# run: scrapy crawl periodic_elements

class PeriodicElementsSpider(scrapy.Spider):
    name = "periodic_elements"
    allowed_domains = ["nih.gov"]

    # don't need: start_urls = ["/"] since we're just working with 1 url

    def start_requests(self):
        # override start_requests to use scrapy-playwright
        yield scrapy.Request('https://pubchem.ncbi.nlm.nih.gov/ptable/',
                             meta=dict(
                                 playwright=True,
                                 playwright_page_methods=[
                                     PageMethod("wait_for_selector", "div.ptable")
                                 ]
                             ))

    # "async" since we're waiting for the "div.ptable" selector above
    async def parse(self, response):
        for element in response.css("div.ptable div.element"):
            i = ItemLoader(item=PeriodicElementItem(), selector=element)

            # [] attribute selector
            i.add_css("symbol", '[data-tooltip="Symbol"]')
            i.add_css("name", '[data-tooltip="Name"]')
            i.add_css("atomic_number", '[data-tooltip="Atomic Number"]')
            i.add_css("atomic_mass", '[data-tooltip*="Atomic Mass"]')
            i.add_css("chemical_group", '[data-tooltip="Chemical Group Block"]')

            yield i.load_item()
