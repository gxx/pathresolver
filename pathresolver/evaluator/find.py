from pathresolver.exceptions import NoMatchError, UnableToResolve
from pathresolver.resolver import basic_multi_resolver
from pathresolver.resolver import match_all_resolver
from .base import EvaluatorBase
from .base import NO_DEFAULT  # TODO: need to handle default error raising from base


IGNORE_VALUE = object()


class Finder(EvaluatorBase):
    def __init__(self, resolver=basic_multi_resolver, match_all_resolver=match_all_resolver):
        self.resolver = resolver
        self.match_all_resolver = match_all_resolver

    def resolve(self, current_key, next_key, value, default=NO_DEFAULT):
        # Attempt to do a match-all first
        try:
            iterable = self.match_all_resolver.resolve(current_key, value)
        except UnableToResolve:
            next_value = self.resolver.resolve(current_key, value)
            evaluated_value = self.evaluate(next_value, next_key, default=default)
        else:
            evaluated_value = (self.evaluate(next_value, next_key, default=IGNORE_VALUE) for next_value in iterable)
            evaluated_value = [value for value in evaluated_value if value is not IGNORE_VALUE]

            if not evaluated_value:
                if default is NO_DEFAULT:
                    # TODO: error message
                    raise UnableToResolve()

                evaluated_value = default

        return evaluated_value

    def evaluate(self, value, path, default=NO_DEFAULT):
        # Base case
        if not path:
            return value

        # Get the current and next keys in the recursion
        try:
            current_key, next_key = path.split('.', 1)
        except ValueError:
            current_key = path
            next_key = None

        try:
            evaluated_value = self.resolve(current_key, next_key, value, default=default)
        except (NoMatchError, UnableToResolve) as error:
            if default is NO_DEFAULT:
                if isinstance(error, NoMatchError):
                    # We are not the root of this issue, pass along the message (and increase the index)
                    root = error.root
                    index = error.index + 1
                else:
                    # We are the root of this error
                    root = current_key
                    index = 0

                raise NoMatchError('Unable to find {} in {}'.format(path, value), root, index)

            evaluated_value = default

        return evaluated_value
