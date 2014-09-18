import abc


NO_DEFAULT = object()


class EvaluatorBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, value, path, default=NO_DEFAULT):
        raise NotImplementedError()

    def __call__(self, value, path, default=NO_DEFAULT):
        return self.evaluate(value, path, default=default)
