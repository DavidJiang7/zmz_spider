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
    
class ResourceLink(scrapy.Item):
    Id = scrapy.Field()
    ResourceId = scrapy.Field()
    LinkId = scrapy.Field()
    Title = scrapy.Field()
    MagnetUrl = scrapy.Field()
    Ed2kUrl = scrapy.Field()
    
class ResourceBase(scrapy.Item):
    Id = scrapy.Field()
    Code = scrapy.Field()
    PCApi = scrapy.Field()
    MApi = scrapy.Field()
    NameCN = scrapy.Field()
    NameEN = scrapy.Field()
    OtherName = scrapy.Field()
    Channel = scrapy.Field()
    ChannelCN = scrapy.Field()
    Area = scrapy.Field()
    ShowType = scrapy.Field()
    Views = scrapy.Field()