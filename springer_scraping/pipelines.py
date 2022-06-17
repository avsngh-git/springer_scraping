# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector

class SpringerScrapingPipeline:
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline:
    def __init__(self):
        self.titles_seen = set()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.titles_seen:
            raise DropItem('Duplicate item found:{item!r}')
        else:
            self.titles_seen.add(adapter['title'])
            return item
        
        
class MySqlPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()
        
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'your_pass',
            database = 'springer_scraping'
        )
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS scrape_result""")
        self.curr.execute("""create table scrape_result(
                          title text,
                          authors text,
                          snippet text,
                          article_link text,
                          pdf_link text,
                          publication_time text)
                          """)
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        self.curr.execute("""insert into scrape_result values(%s, %s, %s, %s, %s, %s)""",
                          (item['title'],
                          item['authors'],
                          item['snippet'],
                          item['article_link'],
                          item['pdf_link'],
                          item['publication_time']
                          )
                          )
        self.conn.commit()