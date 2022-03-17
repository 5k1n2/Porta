class DeviceInfo(dict):
    
    
    def __init__(self, model) -> None:
        super().__init__()
        
        self.model = model
        
        self["name"] = ""
        self["fancyName"] = ""
        self["description"] = ""
        
        
    def update(self, new_dict, current_layer = None):
        
        
        if current_layer is None:
            current_layer = self
        


        for entry in new_dict:
            if isinstance(new_dict[entry], dict):
                if(entry in current_layer):
                    self.update(new_dict[entry], current_layer[entry])
                    continue
                else: current_layer[entry] = new_dict[entry]
            current_layer[entry] = new_dict[entry]

        print(self)

    def update_dict(self, new_dict, current_layer = None):

        self.model.updateElement.emit(new_dict)

        self.update(new_dict, current_layer)
        
