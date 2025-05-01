"""Custom Exceptions."""


class GlucoseAPICustomError(Exception):
    pass


class NoDataFoundError(GlucoseAPICustomError):
    pass


class ParsingError(GlucoseAPICustomError):
    pass
