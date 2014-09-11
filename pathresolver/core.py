#!/usr/bin/env python
# encoding=utf-8
IGNORE_VALUE = object()

NO_DEFAULT = object()

MATCH_ALL = '*'


class PathResolverError(Exception):
    pass


class NoMatchError(PathResolverError):
    pass


class BadValueError(PathResolverError):
    pass


def resolve(value, path, default=NO_DEFAULT):
    # If no path, return the current value
    if not path:
        return value

    # Get the current and next keys in the recursion
    try:
        current_key, next_key = path.split('.', 1)
    except ValueError:
        current_key = path
        next_key = None

    if current_key == MATCH_ALL:
        # Apply all paths, if any, on every item on list
        if isinstance(value, dict):
            # If the value is a dictionary, we simply continue matching for each element of the values
            evaluated_value = (
                [resolve(item, next_key, default=IGNORE_VALUE) for item in value.values()]
            )
        elif hasattr(value, '__iter__') or hasattr(value, '__getitem__'):
            # If the
            evaluated_value = (
                [resolve(item, next_key, default=IGNORE_VALUE) for item in value]
            )
        else:
            raise BadValueError(
                'Cannot match all within value, bad type "{klass_type}" with value "{value}"'.format(
                    klass_type=type(value).__name__,
                    value=repr(value)
                )
            )

        evaluated_value = [value for value in evaluated_value if value is not IGNORE_VALUE]
        if not evaluated_value and default is NO_DEFAULT:
            raise ValueError('Unable to find {} in {}'.format(path, value))
    else:
        try:
            try:
                current_value = getattr(value, current_key)
            except AttributeError:
                try:
                    current_value = value[current_key]
                except TypeError:
                    current_value = value[int(current_key)]
        except (TypeError, ValueError, KeyError, AttributeError):
            if default is NO_DEFAULT:
                raise ValueError('Unable to find {} in {}'.format(path, value))
            else:
                evaluated_value = default
        else:
            evaluated_value = resolve(current_value, next_key, default=default)

    return evaluated_value
