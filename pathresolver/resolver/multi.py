from .key import KeyResolver
from pathresolver.exceptions import UnableToResolve


class MultiKeyResolver(KeyResolver):
    def __init__(self, *resolvers):
        self.resolvers = resolvers
        super(MultiKeyResolver, self).__init__(self.resolve_multi, UnableToResolve)

    def resolve_multi(self, key, value):
        for resolver in self.resolvers:
            try:
                return resolver.resolve(key, value)
            except UnableToResolve:
                pass

        # If we've reached this point, none of the resolvers matched
        raise UnableToResolve('Cannot find {key} in {value}'.format(key=key, value=value))
