# coding: utf-8

from leancloud import LeanCloudError
from leancloud import Query
from leancloud import Object

from .tieba import TiebaPost

class Tian(Object):
    pass


def updatePage(start_page):
    """爬取 http://tieba.baidu.com/p/2674337275 的日记贴，从start_page开始爬取。     

    Args:
        start_page (INTEGER, optional): 从start_page页开始爬取，若为-n，代表更新最后n页

    """
    t = TiebaPost('http://tieba.baidu.com/p/2674337275')
    max_page = t.max_page
    if start_page < 0:
        start_page = start_page + max_page + 1
    for i in xrange(start_page, max_page + 1):
        for post in t.find_page(i):
            try:
                # 如果回复贴已存入数据库，则跳过
                if Query(Tian).equal_to('post_no', post['post_no']).find():
                    continue
            except LeanCloudError as e:
                if e.code == 101:
                    pass
            Tian(**post).save()
            print post['user_name'], post['post_no']
            print '-' * 50
