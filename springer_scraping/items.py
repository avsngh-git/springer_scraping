# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SpringerScrapingItem(Item):
    title = Field()
    article_link = Field()
    snippet = Field()
    authors = Field()
    pdf_link = Field()
    publication_time = Field()
