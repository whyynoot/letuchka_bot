from typing import Any, Union, cast
from pymongo import database

import uuid

from config import USER_COLLECTION_NAME

from ..models.user import User, Student, RawStudent


class UsersTable():

    def __init__(self,
            db: database.Database) -> None:
        self.__collection = db[USER_COLLECTION_NAME]


    # region Tutor

    def has_tutor(self) -> bool:
        found = self.__collection.find_one({ 'is_tutor': True })
        return found is not None

    def create_tutor(self, id: int) -> User:
        doc = { 'telegram_id': id, 'is_tutor': True }
        insert_result = self.__collection.insert_one(doc)
        found = self.__collection.find_one({ '_id': insert_result.inserted_id })
        return self.__user_from_document(cast(dict, found))

    def __user_from_document(self, doc: dict) -> User:
        return User(doc['telegram_id'], doc['is_tutor'])

    def remove_tutor(self) -> None:
        self.__collection.delete_one({ '$eq': { 'is_tutor': True } })

    # endregion


    # region Student

    def create_student(self, source: RawStudent) -> Student:
        doc = { 'telegram_id': source.id, 'is_tutor': False, 'name': source.name, 'group_id': source.group_id }
        insert_result = self.__collection.insert_one(doc)
        found = self.__collection.find_one({ '_id': insert_result.inserted_id })
        return self.__student_from_document(cast(dict, found))

    def get_students(self, group_id: uuid.UUID) -> list[Student]:
        found = self.__collection.find({ 'is_tutor': False, 'group_id': group_id })
        return list(map(lambda doc: self.__student_from_document(doc), found))
    
    def get_all_students(self) -> list[Student]:
        found = self.__collection.find({ 'is_tutor': False})
        return list(map(lambda doc: self.__student_from_document(doc), found))
    
    def delete_student_by_tg_id(self, telegram_id: int) -> bool:
        result = self.__collection.delete_one({'telegram_id': telegram_id})
        return result.deleted_count > 0

    def get_student(self, property: str, value: Any) -> Union[Student, None]:
        found = self.__collection.find_one({property: value})
        if found is None: return
        return self.__student_from_document(found)

    def __student_from_document(self, doc: dict) -> Student:
        return Student(id=doc['telegram_id'], is_tutor=doc['is_tutor'], name=doc['name'], group_id=doc['group_id'])

    def remove_students(self) -> None:
        self.__collection.delete_many({ '$eq': { 'is_tutor': False } })

    # endregion


    # region User

    def get_user(self, id: int) -> Union[User, None]:
        found = self.__collection.find_one({ 'telegram_id': id })
        if found is None: return
        return self.__user_from_document(found)

    def get_users(self) -> list[User]:
        found = self.__collection.find()
        return list(map(lambda doc: self.__user_from_document(doc), found))

    def remove_users(self) -> None:
        self.__collection.delete_many({})

    # endregion
