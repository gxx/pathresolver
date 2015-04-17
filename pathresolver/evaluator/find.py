from pathresolver.exceptions import NoMatchError, UnableToResolve
from pathresolver.resolver import basic_multi_resolver
from pathresolver.resolver import match_all_resolver as _match_all_resolver
from .base import EvaluatorBase
from .base import NO_DEFAULT  # TODO: need to handle default error raising from base


IGNORE_VALUE = object()


class Finder(EvaluatorBase):
    def __init__(self, resolver=basic_multi_resolver, match_all_resolver=_match_all_resolver):
        self.resolver = resolver
        self.match_all_resolver = match_all_resolver

    def resolve(self, current_key, next_key, value, default=NO_DEFAULT):
        call_as_func = False

        # TODO: add functionality to call with index values or some such i.e. 'a.b($0)' or values 'a.b("c")
        if current_key.endswith('()'):
            current_key = current_key[:-2]
            call_as_func = True

        # Attempt to do a match-all first
        try:
            iterable = self.match_all_resolver.resolve(current_key, value)
        except UnableToResolve:
            next_value = self.resolver.resolve(current_key, value)

            if call_as_func:
                next_value = next_value()

            evaluated_value = self.evaluate(next_value, next_key, default=default)
        else:
            # TODO: add in ability to call all items on an iterable as funcs
            if call_as_func:
                raise NotImplementedError()

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
            # Wrap the call and if it cannot be resolved, check if we can alternatively evaluate the value of a
            # function while back-tracking here. If not, simply re-raise the error
            try:
                evaluated_value = self.resolve(current_key, next_key, value, default=default)
            except (NoMatchError, UnableToResolve):
                if not callable(value):
                    raise

                value = value()
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

                raise NoMatchError('Unable to find {} in {} at index'.format(path, value, index), root, index)

            evaluated_value = default

        return evaluated_value
