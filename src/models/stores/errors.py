
class StoreError(Exception):
    def __init__(self, message):
        self.message =message

class StoreNotFoundError(StoreError):
    pass

class URLMalformedError(StoreError):
    pass

class SavingToDatabseError(StoreError):
    pass

