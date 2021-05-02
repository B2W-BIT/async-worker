class EmptyQueueException(Exception):
    """ No message to get """


class MessageError(ValueError):
    """ Base for all message exceptions """


class UndecodableMessageException(MessageError):
    """ Can't decode as JSON """


class InvalidMessageSizeException(MessageError):
    def __init__(self, message=None):
        """ Message size if bigger than it should be """
        self.message = message
