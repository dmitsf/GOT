class EastException(Exception):
    """
    """
    msg_fmt = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except KeyError as e:
                message = self.msg_fmt

        super().__init__(message)

    def format_message(self):
        if self.__class__.__name__.endswith('_Remote'):
            return self.args[0]
        else:
            return self


class NotFoundException(EastException):
    msg_fmt = "Not found."


class NoSuchASTAlgorithm(NotFoundException):
    msg_fmt = "There is no AST construction algorithm with name `%(name)s`."


class EmptyStringsCollectionException(EastException):
    msg_fmt = "The input strings collection is empty."
