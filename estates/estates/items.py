# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EstatesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kategorija = scrapy.Field()  # house/apartment
    transakcija = scrapy.Field()  # for sale/rent
    grad = scrapy.Field()  # city
    opstina = scrapy.Field()  # community
    kvadratura = scrapy.Field()  # square footage in m^2
    godinaizgradnje = scrapy.Field()  # the year of construction
    povrsinazemljista = scrapy.Field()  # land area in ares
    ukupanbrojspratova = scrapy.Field()  # storeys
    spratnost = scrapy.Field()  # story
    uknjizeno = scrapy.Field()  # registration
    tipgrejanja = scrapy.Field()  # heating
    brsoba = scrapy.Field()  # number of rooms
    brkupatila = scrapy.Field()  # number of bathrooms
    parking = scrapy.Field()  # parking lot or garage
    lift = scrapy.Field()  # elevator
    terasa = scrapy.Field()  # terrace (terasa, vrt)
    lodja = scrapy.Field()  # loggia
    balkon = scrapy.Field()  # balcony
    sigurnost = scrapy.Field()  # quantitative representation based on number of listed items
