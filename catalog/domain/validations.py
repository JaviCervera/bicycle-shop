def validate_id(id_, field: str) -> None:
    if not isinstance(id_, int) or not id_ > 0:
        raise ValueError(f'{field} must be a positive integer, '
                         f'got {type(id_).__name__}')


def validate_iterable(v, elem_type, field: str) -> None:
    if v is None or not hasattr(v, '__iter__'):
        raise ValueError(f'{field} must be iterable, got {type(v).__name__}')
    for i, e in enumerate(v):
        validate_type(e, elem_type, f'{field} elem at index {i}')


def validate_type(v, type_, field: str) -> None:
    if not isinstance(v, type_):
        raise ValueError(f'{field} must be a {type_.__name__}, '
                         f'got {type(v).__name__}')
