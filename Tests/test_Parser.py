#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@author: d00ms(--)
@file: test_Parser.py
@time: 2019-5-7 14:56
@desc: Test Core.Parser Module
'''

from Core.Parser import are_they_similar,sanitize_urls
from Http.Url import Url
import unittest
from urllib.parse import urlencode


class TestIt(unittest.TestCase):
    def testSimilarity(self,urla,urlb):
        result = are_they_similar(urla,urlb)
        try:
            self.assertEqual(result, -1)
        except Exception as ext:
            print(ext)

    def testSanitization(self, dirty_urls):
        return sanitize_urls(dirty_urls)



if __name__ == '__main__':
    base = 'www.bat.com/index.php'
    t = TestIt()
    t.testSimilarity(Url(base+'?b=4'), Url(base+'?b=3'))
    t.testSimilarity(Url(base+"?a=3"), Url(base+"?a=2&b=4"))
    t.testSimilarity(Url(base), Url(base))
    t.testSimilarity(Url(base), Url(base+"?a=2"))


    dirty_urls = [Url(base),Url(base+'?a=1'),Url(base+'?a=2'),Url(base+'?b=1'),Url(base+'?b=4&a=3'),Url(base+'?b=4&c=2')]
    clean_urls = t.testSanitization(dirty_urls)
    print("dirty urls:")
    print([x.canonical_url for x in dirty_urls])
    print([x.canonical_url for x in clean_urls])

    cleanUrls = t.testSanitization([Url('http://www.bandao.cn/2013css/ipadicon.png')])
    print(len(cleanUrls))
