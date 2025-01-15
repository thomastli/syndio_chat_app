from config.constants import Constants


def clean_mongo_id(data):
    """Convert MongoDB ObjectId to string for JSON serialization"""
    if isinstance(data, list):
        return [clean_mongo_id(item) for item in data]
    if isinstance(data, dict):
        data_cleaned = data.copy()
        if Constants.ID_FIELD in data_cleaned:
            data_cleaned[Constants.ID_FIELD] = str(data_cleaned[Constants.ID_FIELD])
        return data_cleaned
    return data