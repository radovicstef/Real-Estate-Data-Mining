import scrapy
from ..items import EstatesItem


def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


class EstatesSpider(scrapy.Spider):
    name = "estates"
    start_urls = [
        'https://www.nekretnine.rs/stambeni-objekti/lista/po-stranici/10/'
    ]

    amenities_main_dict = {}
    amenities_additional = []
    amenities_security = 0
    amenities_other = {}

    def parse(self, response):
        self.parse_ad(response)
        estate_links_page = response.css("div.row.offer a").xpath("@href")

        next_page = response.css("a.next-article-button").xpath("@href")

        for page in estate_links_page:
            yield response.follow(page.get(), callback=self.parse_ad)

        if estate_links_page:
            yield response.follow(next_page.get(), callback=self.parse)



    def parse_ad(self, response):
        self.amenities_main_dict = {}
        self.amenities_additional = []
        self.amenities_security = 0
        self.amenities_other = {}  # Reset global dictionaries and arrays

        price = response.css("div.stickyBox__price-size h4.stickyBox__price::text").extract()[0]
        price = float("".join((price.strip(" EUR")).split()))
        location = response.css("h3.stickyBox__Location::text").extract()[0].strip()
        city = location.split(",")[0].strip()
        community = location.split(",")[1].strip() if len(location.split(",")) >= 2 else ""

        self.amenities_main_dict['Cena'] = price
        self.amenities_main_dict['Grad'] = city
        self.amenities_main_dict['Opstina'] = community

        amenities_sections = response.css("div.property__amenities")
        for amenities_section in amenities_sections:
            title = amenities_section.css("h3::text").extract()[0]
            if title == "Podaci o nekretnini":
                self.parse_amenities_main(amenities_section)
                print(self.amenities_main_dict)
            if title == "Dodatna opremljenost":
                self.parse_amenities_additional(amenities_section)
                print(self.amenities_additional)
            if title == "Sigurnosna oprema":
                self.amenities_security = self.parse_ammenities_security(amenities_section)
                print(self.amenities_security)
            if title == "Ostalo":
                self.parse_amenities_other(amenities_section)
                print(self.amenities_other)

        items = self.store_to_items(response)
        yield items





    def parse_amenities_main(self, amenities_section):  # parse 'Podaci o nekretnini' section
        amenities = amenities_section.css("ul li")
        for amenity in amenities:
            key = amenity.css("li::text").extract()[0].strip()  # remove white spaces
            if key[-1] == ':':  # and last ':' character
                key = key[:-1]
            value = amenity.css("strong::text").extract()[0].strip()
            if "kategorija" in key.lower():  # general categorization - house/apartment
                if "stan" in value.lower() or "garsonjera" in value.lower():
                    value = "Stan"
                elif "kuća" in value.lower():
                    value = "Kuca"
                else:
                    continue
            if "kvadratura" in key.lower():  # remove m^2 from value
                value = value.split()[0]
            if "ukupan" in key.lower() and "spratova" in key.lower():  # had some problems with this text, probably some special characters
                key = "Ukupan broj spratova"
            if "površina zemljišta" in key.lower():
                value = value.split()[0]
            if is_number(value) and "spratnost" not in key.lower():  # spratnost can have values such as 'Prizemlje'
                value = float(value)
            if isinstance(value, str) and value.lower() == "da":
                value = True
            elif isinstance(value, str) and value.lower() == "ne":
                value = False
            self.amenities_main_dict[key] = value


    def parse_amenities_additional(self, amenities_section):  # Parse 'Dodatna opremljenost' section
        amenities = amenities_section.css("ul li")
        for amenity in amenities:
            self.amenities_additional.append(amenity.css("li::text").extract()[0].strip())


    def parse_ammenities_security(self, amenities_section):  # Parse 'Sigurnosna oprema' section
        amenities = amenities_section.css("div.property__amenities ul li::text").extract()
        return len(amenities)


    def parse_amenities_other(self, amenities_section):  # Parse 'Ostalo' section
        amenities = amenities_section.css("ul li::text").extract()
        for amenity in amenities:
            key = amenity.strip().split(":")[0].strip()
            value = amenity.strip().split(":")[1].strip()
            self.amenities_other[key] = value


    def store_to_items(self, response):
        items = EstatesItem()
        items["kategorija"] = self.amenities_main_dict["Kategorija"] if "Kategorija" in self.amenities_main_dict else None
        items["transakcija"] = self.amenities_main_dict["Transakcija"] if "Transakcija" in self.amenities_main_dict else None
        items["grad"] = self.amenities_main_dict["Grad"] if "Grad" in self.amenities_main_dict else None
        items["opstina"] = self.amenities_main_dict["Opstina"] if "Opstina" in self.amenities_main_dict else None
        items["kvadratura"] = self.amenities_main_dict["Kvadratura"] if "Kvadratura" in self.amenities_main_dict else None
        items["godinaizgradnje"] = self.amenities_main_dict["Godina izgradnje"] if "Godina izgradnje" in self.amenities_main_dict else None
        items["povrsinazemljista"] = self.amenities_main_dict["Površina zemljišta"] if "Površina zemljišta" in self.amenities_main_dict else None
        items["spratnost"] = self.amenities_main_dict["Spratnost"] if "Spratnost" in self.amenities_main_dict else None
        items["ukupanbrojspratova"] = self.amenities_main_dict["Ukupan broj spratova"] if "Ukupan broj spratova" in self.amenities_main_dict else None
        items["uknjizeno"] = self.amenities_main_dict["Uknjiženo"] if "Uknjiženo" in self.amenities_main_dict else False
        items["brsoba"] = self.amenities_main_dict["Ukupan broj soba"] if "Ukupan broj soba" in self.amenities_main_dict else None
        items["brkupatila"] = self.amenities_main_dict["Broj kupatila"] if "Broj kupatila" in self.amenities_main_dict else None
        items["stanjenekretnine"] = self.amenities_main_dict["Stanje nekretnine"] if "Stanje nekretnine" in self.amenities_main_dict else None

        items["cena"] = self.amenities_main_dict["Cena"] if "Cena" in self.amenities_main_dict else None

        if any("parking" in amenity.lower() for amenity in self.amenities_additional):
            items["parking"] = True
        elif any("garaž" in amenity.lower() for amenity in self.amenities_additional):
            items["parking"] = True
        else:
            items["parking"] = False

        if any("lift" in amenity.lower() for amenity in self.amenities_additional):
            items["lift"] = True
        else:
            items["lift"] = False

        if any("terasa" in amenity.lower() for amenity in self.amenities_additional):
            items["terasa"] = True
        else:
            items["terasa"] = False

        if any("balkon" in amenity.lower() for amenity in self.amenities_additional):
            items["balkon"] = True
        else:
            items["balkon"] = False

        if any("lođa" in amenity.lower() for amenity in self.amenities_additional):
            items["lodja"] = True
        else:
            items["lodja"] = False

        if any("grejanje" in amenity.lower() for amenity in self.amenities_other):
            items["tipgrejanja"] = self.amenities_other["Grejanje"]
        else:
            items["tipgrejanja"] = None

        items["sigurnost"] = self.amenities_security

        items["link"] = response.request.url
        return items

