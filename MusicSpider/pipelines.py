# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

class MusicspiderPipeline(object):
    def process_item(self, item, spider):
        print("已接收到数据，正在存储......")
        myPath = "E:\LearnLife\Python\Spider\Music"
        if not os.path.exists(myPath):
            os.mkdir(myPath)
        for i in range(len(item['musicName']) - 1):
            print(item['musicName'][i])
            fileName = myPath + os.path.sep + str(item['musicName'][i]) + '.txt'
            print(fileName)
            with open(fileName, "a+",encoding='utf-8') as f:
                for it in item:
                    if len(item[it][i]) == 0:
                        f.write("空值" + '\n')
                        print("写入成功！！")
                    else:
                        f.write(str(item[it][i]) + "\n")
                        print("写入成功！！")
        return item
