import sys


class ClassProperty(property):
    """ Property value at class level, instead of instance level """

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class MetaWrapper(type):
    LOCALS = {k: v for k, v in globals().iteritems() if k.isupper()}

    def __getattr__(self, name):
        """ defines __getattr__ at class level for all subclasses of this meta class """
        try:
            return self.LOCALS[name]
        except KeyError:
            raise AttributeError()


class Wrapper:
    """ Turns import-time defined global variables into properties retreived at run-time"""

    __metaclass__ = MetaWrapper

    def OVERRIDDEN_CONFIG_getter(self):
        """ Retreive value at run-time """
        # do something here.
        return

    @property
    def OVERRIDDEN_CONFIG(self):
        """ Returns class level property that calls getter at access time """
        return ClassProperty(self.OVERRIDDEN_CONFIG_getter)


# Replace this module with the created wrapper
sys.modules[__name__] = Wrapper
