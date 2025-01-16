from config.constants import Constants


def remove_mongo_id(data):
    """Remove MongoDB ObjectId from messages for JSON serialization"""
    if isinstance(data, list):
        return [remove_mongo_id(item) for item in data]
    if isinstance(data, dict):
        data_cleaned = data.copy()
        if Constants.ID_FIELD in data_cleaned:
            del data_cleaned[Constants.ID_FIELD]
        return data_cleaned
    return data