import scrapy


class ChannelList(scrapy.Item):
    Id = scrapy.Field()
    Channel = scrapy.Field()
    Url = scrapy.Field()
    Status = scrapy.Field()

class Resource(scrapy.Item):
    Id = scrapy.Field()
    NameCN = scrapy.Field()
    NameEN = scrapy.Field()
    OtherName = scrapy.Field()
    PlayStatus = scrapy.Field()
    Explain = scrapy.Field()
    ImgLink = scrapy.Field()
    Level = scrapy.Field()
    Url = scrapy.Field()
    Description = scrapy.Field()
    Score = scrapy.Field()
    CreateTime = scrapy.Field()
    UpdateTime = scrapy.Field()
    Channel = scrapy.Field()
    RSSUrl = scrapy.Field()
    Status = scrapy.Field()
    
class ResourceProp(scrapy.Item):
    Id = scrapy.Field()
    ResourceId = scrapy.Field()
    PropName = scrapy.Field()
    PropValue = scrapy.Field()
    
class ResourceCharacter(scrapy.Item):
    Id = scrapy.Field()
    ResourceId = scrapy.Field()
    CharacterId = scrapy.Field()
    CharacterType = scrapy.Field()

class Character(scrapy.Item):
    Id = scrapy.Field()
    NameCN = scrapy.Field()
    NameEN = scrapy.Field()
    Url = scrapy.Field()
    
class SearchResult(scrapy.Item):
    Id = scrapy.Field()
    ResourceId = scrapy.Field()
    LinkId = scrapy.Field()
    Title = scrapy.Field()
    MagnetUrl = scrapy.Field()
    Ed2kUrl = scrapy.Field()