import abc


class ResolverBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def resolve(self, key, value):
        raise NotImplementedError()

    def __call__(self, key, value):
        return self.resolve(key, value)
