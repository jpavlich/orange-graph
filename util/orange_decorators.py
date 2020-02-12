from typing import List, Union

# https://stackoverflow.com/a/3611134
def orange_meta(*args, **kwargs):
    def _orange(fun):
        fun.params = args
        return fun

    return _orange


def orange_types(*args, **kwargs):
    def _orange(fun):
        fun.params = args
        return fun

    return _orange
