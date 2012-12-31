#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib2 import urlopen, quote
import json
import gobject

class QueryYoudao:
    def __init__(self, api_key, key_from):
        self.api_key = api_key
        self.key_from = key_from
        self.resultsCache = {}

        
    def query(self, word):
        word = word.strip().split()
        if len(word) > 1:
            for i,w in enumerate(word):
                word[i] = quote(word[i])
            word = '+'.join(word)
        else:
            word = quote(word[0])

        if self.resultsCache.has_key(word):
            results = self.resultsCache[word]
        else:
            req = urlopen('http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=%s'%(self.key_from, self.api_key, word))
            results = json.loads(req.read())
            self.resultsCache[word] = results

        return results

    
    def update_buffer(self, buffer, text):
        buffer.set_text(text)
        return False

        
    def getBrief(self, word, queue, buffer):
        results = self.query(word)
        
        text = '未找到匹配的词'
        
        if results.has_key('basic'):
            basic = results['basic']
            text = word + '\n'
        else:
            gobject.idle_add(self.update_buffer, buffer, text)
            return
            
        if basic.has_key('phonetic'):
            phonetic = basic['phonetic']
            text = '[' + phonetic + ']\n\n'
        else:
            phonetic = None
                
        if basic.has_key('explains'):
            explains = ''
            for w in basic['explains']:
                explains = explains + w + '\n'
                text = text + explains + '\n'
        else:
            explains = None

        gobject.idle_add(self.update_buffer, buffer, text)

    
    def getDetail(self, word):
        results = self.query(word)

        text = '没有更多内容'

        if results.has_key('web'):
            text = '网络释义\n\n'
            for r in results['web']:
                text = text + r['key'] + '\n'
                for val in r['value']:
                    text = text + val + '\n'

        return text
