from typing import Any, Dict, List

import cherrypy
from peewee import Model
from peewee import SqliteDatabase

db = SqliteDatabase(cherrypy.config.get("db_url", "test.db"))


class AdminCrudMixin:
    # CRUD mixin
    @classmethod
    def admin_delete(cls: "BaseModel", pks: List[int]):
        sql = cls.delete().where(cls.id.in_(pks))
        sql.execute()

    @classmethod
    def admin_create(cls: "BaseModel", data: Dict[str, Any]) -> "BaseModel":
        return cls.create(**data)

    @classmethod
    def admin_update(cls: "BaseModel", data: Dict[str, Any]):
        pk = data.pop("id")
        attrs = {getattr(cls, k): v for k, v in data.items()}
        cls.update(attrs).where(cls.id == pk).execute()

    @classmethod
    def admin_select(cls: "BaseModel", page: int, size: int, conditions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        select = cls.select()
        for c in conditions:
            field = getattr(cls, c["field"])
            if "eq" in c:
                select = select.where(field == c["eq"])
            elif "gt" in c:
                select = select.where(field > c["gt"])
            elif "lt" in c:
                select = select.where(field < c["lt"])
            elif "contains" in c:
                select = select.where(field.contains(c["contains"]))
            elif "in" in c:
                select = select.where(field.in_(c["in"]))

        if page and size:
            select = select.limit(size).offset((page - 1) * size)

        res = select.dicts()
        return list(res)


class BaseModel(Model, AdminCrudMixin):
    class Meta:
        database = db

    def as_dict(self) -> Dict[str, Any]:
        return self.__data__

    def action_example(self, *_, **__):
        # just a example for action
        return {}


def db_connect():
    print("db start....")
    db.connect()


def db_close():
    print("db close....")
    if not db.is_closed():
        db.close()


cherrypy.engine.subscribe("before_request", db_connect)
cherrypy.engine.subscribe("after_request", db_close)
