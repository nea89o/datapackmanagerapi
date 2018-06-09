import typing

from flask import jsonify, request
from peewee import Model, ModelSelect

from api.v1.db import DataPack, Tag, TagRelation

_V = typing.TypeVar('_V', bound=Model)


def model_paginator(model: typing.Type[_V], mapping: typing.Callable[[_V], dict]):
    return query_paginator(model.select(), mapping)


class ConstrainFailed(Exception):
    def __init__(self, description: str, parameter: str, reason: str):
        self.reason = reason
        self.parameter = parameter
        self.description = description


def try_or_fail_contrain(func: typing.Callable, parameter: str, value=None, default=None):
    if value is None:
        value = request.args.get(parameter, default)
    try:
        return func(value)
    except BaseException as e:
        func = func.__name__
        raise ConstrainFailed(f"{func}({parameter}) failed with an exception", parameter,
                              f"{func} raised {type(e).__name__}")


def max_constrain(max: int, parameter: str, value=None, default=None):
    value = try_or_fail_contrain(int, parameter, value, default)
    if value > max:
        raise ConstrainFailed(f"requested {parameter} too big", parameter, f'> {max}')
    return value


def min_constrain(min: int, parameter: str, value=None, default=None):
    value = try_or_fail_contrain(int, parameter, value, default)
    if value < min:
        raise ConstrainFailed(f"requested {parameter} too big", parameter, f'< {min}')
    return value


def query_paginator(query: ModelSelect, mapping: typing.Callable[[_V], dict]):
    size = try_or_fail_contrain(int, 'size', default='50')
    max_constrain(50, 'size', size)
    min_constrain(2, 'size', size)
    offset = try_or_fail_contrain(int, 'offset', default='0')
    min_constrain(0, 'offset', offset)
    res = []
    for obj in query.limit(size + 1).offset(offset):
        res.append(mapping(obj))
    more = len(res) > size
    if more:
        res[-1:] = []
    return jsonify({
        'more': more,
        'next': offset + size if more else None,
        'results': res,
    })


def get_tags_for_datapack(datapack: DataPack):
    return [tag.name for tag in
            Tag.select().join(TagRelation).join(DataPack).where(TagRelation.pack.id == int(datapack.id))]
