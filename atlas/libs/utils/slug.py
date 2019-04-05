def slugify(value):
    """
    slugify user name to username
    the format name.names
    """
    names = value.lower().split(' ')[:2]
    return '.'.join(names)