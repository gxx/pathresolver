from .key import KeyResolver
from pathresolver.exceptions import UnableToResolve
from .predicate import PredicateResolver
from .predicate import StringMatchResolver
from .multi import MultiKeyResolver


MATCH_ALL = '*'


# ---- Basic Resolvers ---- #
# Resolve by Attribute
attribute_resolver = KeyResolver(lambda k, v: getattr(v, k), (AttributeError, TypeError))

# Resolve by Key (i.e. dictionary)
key_lookup_resolver = KeyResolver(lambda k, v: v[k], (KeyError, TypeError))

# Resolve by Index (integer index lookup)
index_lookup_resolver = KeyResolver(lambda k, v: v[int(k)], (KeyError, IndexError, TypeError, ValueError))

# ---- Iterable Resolvers ---- #
# Resolve for a match-all against a dictionary
match_all_dict_resolver = PredicateResolver(
    lambda _, dct: dct.values(),
    AttributeError,
    dict,
)

# Resolve for a match-all against an iterable
match_all_iterable_resolver = PredicateResolver(
    lambda _, iterable: [i for i in iterable],
    (AttributeError, TypeError),
    lambda _, value: hasattr(value, '__iter__') or hasattr(value, '__getitem__'),
)

# ---- Multi Resolvers --- #
# Resolve for all default resolutions (by attribute, by key and by index)
basic_multi_resolver = MultiKeyResolver(attribute_resolver, key_lookup_resolver, index_lookup_resolver)

# Resolve for match-all
match_all_resolver = StringMatchResolver(
    MultiKeyResolver(match_all_dict_resolver, match_all_iterable_resolver),
    UnableToResolve,
    MATCH_ALL
)
