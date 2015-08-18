class ADSBibtexBaseException(Exception):
    pass


class ADSBibtexConfigError(ADSBibtexBaseException):
    pass


class ADSBibtexBibcodeNotFound(ADSBibtexBaseException):
    pass