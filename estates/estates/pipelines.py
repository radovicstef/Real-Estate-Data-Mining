# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector

class EstatesPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()


    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='admin',
            database='estates'
        )
        self.curr = self.conn.cursor()


    def create_table(self):
        self.curr.execute(
            """CREATE TABLE tbl_estates(
                link longtext,
                cena float,
                kategorija text,
                transakcija text,
                grad text,
                opstina text,
                kvadratura float,
                godinaizgradnje int,
                stanjenekretnine text,
                povrsinazemljista float,
                ukupanbrojspratova float,
                spratnost text,
                uknjizeno tinyint,
                tipgrejanja text,
                brsoba float,
                brkupatila float,
                parking tinyint,
                lift tinyint,
                terasa tinyint,
                lodja tinyint,
                balkon tinyint,
                sigurnost int
            )"""
        )

    def process_item(self, item, spider):
        self.store_db(item)
        return item


    def store_db(self, item):
        self.curr.execute(
            """INSERT INTO tbl_estates VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""",
            (
                item['link'],
                item['cena'],
                item['kategorija'],
                item['transakcija'],
                item['grad'],
                item['opstina'],
                item['kvadratura'],
                item['godinaizgradnje'],
                item['stanjenekretnine'],
                item['povrsinazemljista'],
                item['ukupanbrojspratova'],
                item['spratnost'],
                item['uknjizeno'],
                item['tipgrejanja'],
                item['brsoba'],
                item['brkupatila'],
                item['parking'],
                item['lift'],
                item['terasa'],
                item['lodja'],
                item['balkon'],
                item['sigurnost']
            )
        )
        self.conn.commit()
