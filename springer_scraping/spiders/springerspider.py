from time import time
from springer_scraping.items import SpringerScrapingItem
import scrapy


def get_li_tag_selector(response):
    """get main tag as a selector because it contains all the info we need to scrape
    and we can use it to further make calls to tags inside it. 
    If we directly call li tags then many more are also brought in which do not have the info we need"""
    main_tag = response.css('main')
    
    """ get a list of li tags out from main as selectors again because 
    we need to scrape info inside other tags residing in these tags"""
    li = main_tag.css('li') #will be a list
    return li

def get_article_title(li_tag):
    """get article title from single li tag"""
    title = li_tag.css('h2').css('a::text').get()
    return title

def get_link(li_tag):
    """get article link"""
    base_url = 'https://link.springer.com'
    href = li_tag.css('h2').css('a::attr(href)').get()
    url = base_url + href
    return url

def get_snippet(li_tag):
    '''a small snippet from the article'''
    snippet = li_tag.css('.snippet::text').get().strip()
    return snippet

def get_authors(li_tag):
    """get authors from a tags in p tag with class 'authors'
    and then combine them into one string with all author names"""
    authors = li_tag.css('.authors').css('a::text').getall()
    authors_str = ', '.join(authors)
    return authors_str

def get_pdf_link(li_tag):
    '''get link for the pdf download of each article'''
    base_url = 'https://link.springer.com'
    href = li_tag.css('.pdf-link::attr(href)').get()
    download_link = base_url+href
    return download_link

def get_publication_time(li_tag):
    '''get publication month and year of the article'''
    time = li_tag.css('.year::attr(title)').get()
    return time
    

def get_nextpage(response):
    '''get the link of the next page from the pagination button'''
    href = response.css('.next::attr(href)').get()
    base_url = 'https://link.springer.com'
    next_link = base_url+href
    return next_link



class SpringerspiderSpider(scrapy.Spider):
    name = 'springerspider'
    allowed_domains = ['link.springer.com']
    start_urls = ['https://link.springer.com/search/page/1?facet-journal-id=10994&package=openaccessarticles&search-within=Journal&query=']
    

    def parse(self, response):
        li_tags = get_li_tag_selector(response)
        
        article_item = SpringerScrapingItem()
        
        for li_tag in li_tags:
            #because li_tags is a list, we have to scrape each one. 
            article_item['title'] = get_article_title(li_tag)
            article_item['article_link'] = get_link(li_tag)
            article_item['snippet'] = get_snippet(li_tag)
            article_item['authors']= get_authors(li_tag)
            article_item['pdf_link'] = get_pdf_link(li_tag)
            article_item['publication_time'] = get_publication_time(li_tag)
            yield article_item
            
        next_page = get_nextpage(response)
        
        if '10' not in next_page[:45]:
            yield response.follow(next_page, callback=self.parse)
            
            
         
            
            
            
        
