# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

class TextspiderPipeline(object):
    def process_item(self, item, spider):
        myPath = "E:\LearnLife\Python\Spider\Stories"
        tempPath = str(item['bookName'])
        targetPath = myPath + os.path.sep + tempPath
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)
        fileNamePath = myPath + os.path.sep + tempPath + os.path.sep + tempPath + '.txt'
        with open(fileNamePath, 'w', encoding='utf-8') as f:
            f.write(item['chapterContent'])
        return item