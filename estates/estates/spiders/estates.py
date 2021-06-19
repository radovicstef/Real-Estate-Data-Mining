import scrapy
from ..items import EstatesItem


class EstatesSpider(scrapy.Spider):
    name = "estates"
    start_urls = [
        'https://www.nekretnine.rs/stambeni-objekti/stanovi/alterra-una-lux-smart-home-direktna-prodaja/Nk9MpN6AZTT/'
    ]

    amenities_main_dict = {}
    amenities_additional = []
    amenities_security = 0
    amenities_other = {}

    def parse(self, response):
        price = response.css("div.stickyBox__price-size h4.stickyBox__price::text").extract()[0]
        price = int("".join((price.strip(" EUR")).split()))
        location = response.css("h3.stickyBox__Location::text").extract()[0].strip()
        city = location.split(",")[0].strip()
        community = location.split(",")[1].strip() if len(location.split(","))>=2 else ""

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

        #self.store_to_items()


    def parse_amenities_main(self, amenities_section):  # parse 'Podaci o nekretnini' section
        amenities = amenities_section.css("ul li")
        for amenity in amenities:
            key = amenity.css("li::text").extract()[0].strip()  # remove white spaces
            if key[-1] == ':':  # and last ':' character
                key = key[:-1]
            value = amenity.css("strong::text").extract()[0].strip()
            if "kategorija" in key.lower():  # general categorization - house/apartment
                if "stan" in value.lower():
                    value = "Stan"
                elif "kuća" in key.lower():
                    value = "Kuca"
                else:
                    continue
            if "kvadratura" in key.lower():  # remove m^2 from value
                value = value.split()[0]
            if value.isnumeric():
                value = int(value)
            self.amenities_main_dict[key] = value


    def parse_amenities_additional(self, amenities_section):
        amenities = amenities_section.css("ul li")
        for amenity in amenities:
            self.amenities_additional.append(amenity.css("li::text").extract()[0].strip())


    def parse_ammenities_security(self, amenities_section):
        amenities = amenities_section.css("div.property__amenities ul li::text").extract()
        return len(amenities)


    def parse_amenities_other(self, amenities_section):
        amenities = amenities_section.css("ul li::text").extract()
        for amenity in amenities:
            key = amenity.strip().split(":")[0].strip()
            value = amenity.strip().split(":")[1].strip()
            self.amenities_other[key] = value


    def store_to_items(self):
        items = EstatesItem()
        items["kategorija"] = self.amenities_main_dict["Kategorija"] if "Kategorija" in self.amenities_main_dict else ""
        items["transakcija"] = self.amenities_main_dict["Transakcija"] if "Transakcija" in self.amenities_main_dict else ""
        items["grad"] = self.amenities_main_dict["Grad"] if "Grad" in self.amenities_main_dict else ""
        items["opstina"] = self.amenities_main_dict["Opstina"] if "Opstina" in self.amenities_main_dict else ""
        items["kvadratura"] = self.amenities_main_dict["Kvadratura"] if "Kvadratura" in self.amenities_main_dict else ""
        items["godinaizgradnje"] = self.amenities_main_dict["Godina izgradnje"] if "Godina izgradnje" in self.amenities_main_dict else ""
        items["povrsinazemljista"] = self.amenities_main_dict["Povrsina zemljišta"] if "Povrsina zemljišta" in self.amenities_main_dict else ""
        items["spratnost"] = self.amenities_main_dict["Spratnost"] if "Spratnost" in self.amenities_main_dict else ""
        items["ukupanbrojspratova"] = self.amenities_main_dict["Ukupan broj spratova"] if "Ukupan broj spratova" in self.amenities_main_dict else ""
        items["uknjizeno"] = self.amenities_main_dict["Uknjiženo"] if "Uknjiženo" in self.amenities_main_dict else ""
        items["brsoba"] = self.amenities_main_dict["Ukupan broj soba"] if "Ukupan broj soba" in self.amenities_main_dict else ""
        items["brkupatila"] = self.amenities_main_dict["Broj kupatila"] if "Broj kupatila" in self.amenities_main_dict else ""

        if any("parking" in amenity.lower() for amenity in self.amenities_additional):
            items["parking"] = "Da"
        elif any("garaž" in amenity.lower() for amenity in self.amenities_additional):
            items["parking"] = "Da"
        else:
            items["parking"] = "Ne"

        if any("lift" in amenity.lower() for amenity in self.amenities_additional):
            items["lift"] = "Da"
        else:
            items["lift"] = "Ne"

        if any("terasa" in amenity.lower() for amenity in self.amenities_additional):
            items["terasa"] = "Da"
        else:
            items["terasa"] = "Ne"

        if any("balkon" in amenity.lower() for amenity in self.amenities_additional):
            items["balkon"] = "Da"
        else:
            items["balkon"] = "Ne"

        if any("lodja" in amenity.lower() for amenity in self.amenities_additional):
            items["lodja"] = "Da"
        else:
            items["lodja"] = "Ne"

        if any("grejanje" in amenity.lower() for amenity in self.amenities_other):
            items["tipgrejanja"] = self.amenities_other["Grejanje"]

        items["sigurnost"] = self.amenities_security
