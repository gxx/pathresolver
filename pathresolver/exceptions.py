class PathResolverError(Exception):
    pass


class UnableToResolve(PathResolverError):
    pass


class NoMatchError(PathResolverError):
    def __init__(self, arg, root, index=0):
        self.root = root
        self.index = index
        super(NoMatchError, self).__init__(arg)
