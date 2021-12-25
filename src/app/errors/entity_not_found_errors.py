from app.errors.service_error import ServiceError


class EntityNotFound(ServiceError):
    http_code = 404

    def __init__(self, message: str):
        super(EntityNotFound, self).__init__(message=message)
