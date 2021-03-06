class AuthorizationError(Exception):
    pass


class UserNotFoundError(AuthorizationError):
    pass


class UrrTeacherError(AuthorizationError):
    pass


class LoginAlreadyExists(AuthorizationError):
    pass


class NotEnoughData(AuthorizationError):
    pass
