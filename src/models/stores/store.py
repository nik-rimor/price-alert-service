import uuid
import re

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors

class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)


    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(collection=StoreConstants.COLLECTION, query={"_id": id}))

    def save_to_mongo(self):
        # Insert json representation
        Database.update(collection= StoreConstants.COLLECTION, query={"_id": self._id} ,data=self.json())


    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(collection=StoreConstants.COLLECTION, query= {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        store_data = Database.find_one(collection=StoreConstants.COLLECTION, query= {"url_prefix": url_prefix})
        if store_data is not None:
            return cls(**store_data)
        else:
            raise StoreErrors.StoreNotFoundError("No shop with the specified URL: {} found.".format(url_prefix))

    @classmethod
    def find_by_url(cls, url):
        """Fetch the Store for a specified URL.
        :param url: The store's URL.
        :returns: The corresponding Store.
        :raises: A StoreNotFoundException if no matching store is found.
        """
        pattern = re.compile(r'^(?P<url_prefix>[^:]*://[^/]+)')
        match = pattern.match(url)
        if match:
            try:
                return cls.get_by_url_prefix(match.group('url_prefix'))
            except StoreErrors.StoreNotFoundError as e:
                return e.message

        raise StoreErrors.URLMalformedError("The url format is not valid")

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(collection=StoreConstants.COLLECTION, query={})]


    def delete(self):
        Database.remove(collection=StoreConstants.COLLECTION, query={"_id": self._id})
