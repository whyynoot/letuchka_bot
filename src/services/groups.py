from pymongo import database

from typing import Any, Union, cast

from config import GROUP_COLLECTION_NAME

from ..models.group import RawGroup, Group


class GroupsTable():

    def __init__(self,
            db: database.Database) -> None:
        self.__collection = db[GROUP_COLLECTION_NAME]

    def create(self, source: RawGroup) -> Group:
        doc = { 'name': source.name, 'open': source.open}
        insert_result = self.__collection.insert_one(doc)
        found = self.__collection.find_one({ '_id': insert_result.inserted_id })
        return self.__from_document(cast(dict, found))
    
    def delete_group(self, property: str, value: Any) -> bool:
        result = self.__collection.delete_one({ property: value })
        return result.deleted_count > 0
    
    def update_group(self, property: str, value: Any, update_property: str, new_value: Any) -> bool:
        result = self.__collection.update_one({ property: value }, {'$set': {update_property: new_value}})
        return result.modified_count > 0

    def get_all(self) -> list[Group]:
        found = self.__collection.find()
        return list(map(lambda doc: self.__from_document(doc), found))

    def get(self, property: str, value: Any) -> Union[Group, None]:
        found = self.__collection.find_one({ property: value })
        if found is None: return
        return self.__from_document(found)
    
    def get_open(self) -> Union[Group, None]:
        found = self.__collection.find({'open': True})
        if found is None: return
        return list(map(lambda doc: self.__from_document(doc), found))
    
    def is_open(self, property: str, value: Any) -> bool:
        found = self.__collection.find_one({ property: value })
        if found is None: return
        return found['open']

    def remove_all(self) -> None:
        self.__collection.delete_many({})

    def __from_document(self, doc: dict) -> Group:
        return Group(name=doc['name'], id=doc['_id'], open=doc['open'])
    

    
