import typing
import cherrypy

from .base_model import BaseModel
from .book import book
from .utils import response_success


@cherrypy.tools.allow(methods=["POST"])
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Ant:

    @classmethod
    def bulk_register(cls, models: typing.List[BaseModel]):
        for m in models:
            book.set(m.__qualname__, m)

    @staticmethod
    def find_model(name: str) -> BaseModel:
        return book.get(name)

    @cherrypy.expose
    def model_data(self):
        data = cherrypy.request.json
        model = self.find_model(data.get("model"))
        results = model.admin_select(
            data.get("page", 1),
            data.get("size", 20),
            data.get("cond", []),
        )
        return response_success(results)

    @cherrypy.expose
    def model_create(self):
        data = cherrypy.request.json
        model = self.find_model(data.get("model"))
        obj = model.admin_create(data.get("data"))
        return response_success(obj.as_dict())

    @cherrypy.expose
    def model_update(self):
        data = cherrypy.request.json
        model = self.find_model(data.get("model"))
        model.admin_update(data.get("data"))
        return response_success(True)

    @cherrypy.expose
    def model_delete(self):
        data = cherrypy.request.json
        model = self.find_model(data.get("model"))
        model.admin_delete(data.get("pks"))
        return response_success(True)

    @cherrypy.expose
    def model_action(self):
        data = cherrypy.request.json
        model = self.find_model(data.get("model"))
        action = f"action_{data['action']}"
        data = data["data"]

        # todo: has_perm
        action_func = getattr(model, action)
        if not action_func:
            raise ValueError(f"{model} lack of action: {action}")
        ret = action_func(data)
        return response_success(ret)




