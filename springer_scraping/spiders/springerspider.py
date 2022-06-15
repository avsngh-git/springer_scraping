from time import time
import scrapy


def get_main_tag_selector(response):
    """get main tag as a selector because it contains all the info we need to scrape
    and we can use it to further make calls to tags inside it. 
    If we directly call li tags then many more are also brought in which do not have the info we need"""
    main_tag = response.css('main')
    return main_tag

def get_li_tag_selector(main):
    """ get a list of li tags out from main as selectors again because 
    we need to scrape info inside other tags residing in these tags"""
    li = main.css('li') #will be a list
    return li

def get_title(li_tag):
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
    time = li_tag.css('.year::attr(title)').get()
    return time
    
    

class SpringerspiderSpider(scrapy.Spider):
    name = 'springerspider'
    allowed_domains = ['link.springer.com']
    start_urls = ['https://link.springer.com/search/page/1?facet-journal-id=10994&package=openaccessarticles&search-within=Journal&query=']
    

    def parse(self, response):
        pass
