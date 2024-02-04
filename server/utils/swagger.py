DESC_UNAUTH = "Unauthorized User"
DESC_INVUI = "Invalid User Input"
DESC_UNEXP = "Unexpected Server Error"


def desc_get(modelname: str) -> str:
    return f"{modelname} by ID"


def desc_list(modelname: str) -> str:
    return f"List of {modelname}s"


def desc_added(modelname: str) -> str:
    return f"{modelname} added"


def desc_update(modelname: str) -> str:
    return f"{modelname} updated"


def desc_delete(modelname: str) -> str:
    return f"{modelname} deleted"


def desc_conflict(modelname: str) -> str:
    return f"{modelname} already existing"


def desc_notfound(modelname: str) -> str:
    return f"{modelname} not found"
