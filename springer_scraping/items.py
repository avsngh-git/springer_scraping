# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import Field
import scrapy


class SpringerScrapingItem(scrapy.Item):
    title = Field()
    article_link = Field()
    snippet = Field()
    authors = Field()
    pdf_link = Field()
    publication_time = Field()
