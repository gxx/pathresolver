from .base import ResolverBase
from pathresolver.exceptions import UnableToResolve


class KeyResolver(ResolverBase):
    def __init__(self, func, failure_exc):
        self.func = func
        self.failure_exc = failure_exc

    def resolve(self, key, value):
        try:
            return self.func(key, value)
        except self.failure_exc:
            raise UnableToResolve('Cannot find {key} in {value}'.format(key=key, value=value))
