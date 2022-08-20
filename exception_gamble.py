

class StudentDataNotUnique(Exception):
    pass

class StudentDataNotFound(Exception):
    pass

class DataHasError(Exception):
    def __init__(self, arg):
        self.args = arg

class EmptyDataException(Exception):
    pass

class ExecuteOverErrorLimitException(Exception):
    pass
