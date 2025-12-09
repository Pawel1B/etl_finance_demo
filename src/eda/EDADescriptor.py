import inspect
from functools import wraps
import json

class EDADescriptor:
    def __init__(self):
        self.history = []
        with open("metric_descriptions.json", "r") as f:
            self.descriptions = json.load(f)

        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith("__"):
                continue
            setattr(self, name, self._wrap(method))

    def _wrap(self, method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            if method.__name__ in self.descriptions:
                doc = self.descriptions[method.__name__]
                self.history.append({
                    "method": method.__name__,
                    "description": doc
                })
            return result
        return wrapper