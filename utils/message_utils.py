from config.constants import Constants


def remove_mongo_id(data):
    """ (Recursively) Removes MongoDB ObjectId from messages for JSON serialization

    Args:
        data: The data to be converted (message or list of messages)

    Returns:
        The message or list of messages with no _id field
    """
    if isinstance(data, list):
        return [remove_mongo_id(item) for item in data]
    if isinstance(data, dict):
        data_cleaned = data.copy()
        if Constants.ID_FIELD in data_cleaned:
            del data_cleaned[Constants.ID_FIELD]
        return data_cleaned
    return data
