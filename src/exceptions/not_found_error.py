class NotFoundError(Exception):
    """Base class for every "not found" error '404' error """

    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(f"{entity_name} with id {entity_id} was not found")
        self.entity_name = entity_name
        self.entity_id = entity_id
