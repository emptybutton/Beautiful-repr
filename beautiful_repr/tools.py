def parse_length(object_: object, attribute_name: str):
    """
    Simple getter function for the Field model that returns the length of an
    attribute by its name.
    """
    
    return len(getattr(object_, attribute_name))
