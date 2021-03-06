# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from typing import Dict, List, Tuple

from crawling.data import data

'''
1. 각 class 구동시 필요한 import 구문은 class 안에 있어야 함.
 (scrapy에서 class만 갖고 crawling 하기 때문에 class 밖에 적어 놓으면 인식 불가.)
2. 비고(reference)가 없는 게시판이라면 xpath를 None으로 지정할 것.
3. set_args() 함수의 id 인자는 각 게시판에서 게시물을 구별할때 사용되는 키 값.
 (ex cse 게시판은 BID 사용, main 게시판은 nttNo 사용)
'''

class DefaultSpider(scrapy.Spider):

    handle_httpstatus_list = [404]

    # 데이터 검증
    def _data_verification(self, item: Dict[str, List]):
        from crawling import models
        when = f'While crawling {self.name}'
        id_len = len(item['ids'])

        # model check
        eval(f"models.{item['model']}")
        if id_len == 0:
            # empty check. 크롤링은 시도했으나 아무 데이터를 가져오지 못한 경우.
            raise Exception(f'{when}, Crawled item is empty! Check the xpaths or base url.')
        for key, value in item.items():
            if key != 'model':
                if len(value) != id_len:
                    # size check. 크롤링된 데이터들이 길이가 다른 경우
                    print("#"*80)
                    print(key)
                    print(item['links'])
                    print(item['ids'])
                    print(item['titles'])
                    raise Exception(f"{when}, {key} size is not same with id. ({key} size: {len(value)}, id size: {id_len})")
            if key != 'references':
                # valid check. 크롤링된 데이터의 유효성 검증.
                if value[0] is None:
                    raise Exception(f'{when}, {key} is None.')
                if value[0] == '':
                    raise Exception(f'{when}, {key} is empty. ("")')

    # 객체 인스턴스에서 사용되는 변수 등록
    def set_args(self, args: Dict):
        self.model = args['model']
        self.id = args['id']
        self.url_xpath = args['url_xpath']
        self.titles_xpath = args['titles_xpath']
        self.dates_xpath = args['dates_xpath']
        self.authors_xpath = args['authors_xpath']
        self.references_xpath = args['references_xpath']

    # 공백 제거. 가장 선행되어야 하는 전처리
    def remove_whitespace(self, items: List[str]) -> List[str]:
        ret = []
        for item in items:
            x = item.strip()
            if x != '':
                ret.append(x)
        return ret

    # Link 객체에서 url과 id 추출
    def split_id_and_link(self, links: List[str]) -> Tuple[List[str],List[str]]:
        urls = []
        ids = []
        for link in links:
            urls.append(link.url+'&')
        for url in urls:
            idx = url.find(self.id)+len(self.id)+1
            for i in range(idx, len(url)):
                if url[i] == "&":
                    break
            ids.append(f'{self.name}-{url[idx:i]}')
        return ids, urls

    # date 형식에 맞게 조정
    # ex 2020.05.19 > 2020-05-19
    def date_cleanse(self, dates: List[str]) -> List[str]:
        return [date.replace('.','-') for date in dates]

    # Override parse()
    def parse(self, response) -> Dict:
        if response.status == 404:
            raise Exception('404 Page not foud! Check the base url.')

        url_forms = LinkExtractor(restrict_xpaths=self.url_xpath,attrs='href',unique=False)
        
        links: List[str] = url_forms.extract_links(response)

        titles: List[str] = self.remove_whitespace(
            response.xpath(self.titles_xpath).getall())

        dates: List[str] = self.remove_whitespace(
            response.xpath(self.dates_xpath).getall())

        authors: List[str] = self.remove_whitespace(
            response.xpath(self.authors_xpath).getall())

        if self.references_xpath:
            references: List[str] = self.remove_whitespace(
                response.xpath(self.references_xpath).getall())
        else:
            references: List[None] = [None for _ in range(len(links))]

        # Data cleansing
        ids, links = self.split_id_and_link(links)  # id, link 추출
        dates = self.date_cleanse(dates)            # date 형식에 맞게 조정

        self._data_verification({
            'model':self.model,
            'ids':ids, 
            'titles':titles, 
            'links':links, 
            'dates':dates, 
            'authors':authors, 
            'references':references,
        })

        for id, title, link, date, author, reference in zip(
            ids, titles, links, dates, authors, references):
            scrapyed_info = {
                'model' : self.model,
                'id' : id,
                'title' : title,
                'link' : link,
                'date' : date,
                'author' : author,
                'reference' : reference,
            }
            yield scrapyed_info

'''
class MainSpider(DefaultSpider):
    def __init__(self):
        from crawling.data import data 
        args = data['main']
        self.name = args['name']
        self.start_urls = args['start_urls']
        super().__init__()
        super().set_args(args)
'''
# 위와 같은 형식의 Spider Class 자동 생성
for key, item in data.items():
    if key.find('test') == -1:
        txt = f"""
class {key.capitalize()}Spider(DefaultSpider):
    def __init__(self):
        from crawling.data import data 
        args = data['{key}']
        self.name = args['name']
        self.start_urls = args['start_urls']
        super().__init__()
        super().set_args(args)
"""
        exec(compile(txt,"<string>","exec"))
