from app.errors.service_error import ServiceError


class EntityAlreadyExist(ServiceError):
    http_code = 404

    def __init__(self, message: str):
        super(EntityAlreadyExist, self).__init__(message=message)
