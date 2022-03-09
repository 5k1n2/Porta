class DeviceInfo(object):
    
    def __init__(self, name: str, fancyName: str = "Empty", description: str = "Empty", title: str = "Empty" ) -> None:
        self.name = name
        self.fancyName = fancyName
        self.description = description
        self.title = title
        self.file = None