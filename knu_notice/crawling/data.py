from crawling import models

data = {
    'main' : {
        'api_url' : '/notice/main/',
        'name' : '강원대학교',
        'start_urls' : ['https://www.kangwon.ac.kr/www/selectBbsNttList.do?bbsNo=37'],
        'model' : models.Main,
        'bid' : 'nttNo',
        'url_xpath' : '//*[@id="board"]/table/tbody/tr/td[3]/a',
        'titles_xpath' : '//*[@id="board"]/table/tbody/tr/td[3]/a/text()',
        'dates_xpath' : '//*[@id="board"]/table/tbody/tr/td[6]/text()',
        'authors_xpath' : '//*[@id="board"]/table/tbody/tr/td[4]/text()',
        'references_xpath' : '//*[@id="board"]/table/tbody/tr/td[2]/text()',
    },
    'cse' : {
        'api_url' : '/notice/cse/',
        'name' : '컴퓨터공학과',
        'start_urls' : ['https://cse.kangwon.ac.kr/index.php?mp=5_1_1'],
        'model' : models.Cse,
        'bid' : 'BID',
        'url_xpath' : '//*[@id="bbsWrap"]/table/tbody/tr/td[2]/a',
        'titles_xpath' : '//*[@id="bbsWrap"]/table/tbody/tr/td[2]/a/text()',
        'dates_xpath' : '//*[@id="bbsWrap"]/table/tbody/tr/td[4]/text()',
        'authors_xpath' : '//*[@id="bbsWrap"]/table/tbody/tr/td[3]/text()',
        'references_xpath' : None,
    },
}