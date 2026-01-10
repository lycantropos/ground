import importlib.machinery
import inspect
import pkgutil
from collections.abc import Iterable
from types import ModuleType

from hypothesis import given, strategies as st

import ground


def _iter_package_api_modules(
    parent_module: ModuleType, /, *, private_name_prefix: str = '_'
) -> Iterable[ModuleType]:
    assert (
        len(
            private_name_parts := [
                name_part
                for name_part in parent_module.__name__.split('.')
                if name_part.startswith(private_name_prefix)
            ]
        )
        == 0
    ), (parent_module.__name__, private_name_parts)
    yield parent_module
    for submodule_info in pkgutil.iter_modules(parent_module.__path__):
        if submodule_info.name.startswith(private_name_prefix):
            continue
        submodule = importlib.import_module(
            '.' + submodule_info.name, parent_module.__name__
        )
        if submodule_info.ispkg:
            yield from _iter_package_api_modules(submodule)
        else:
            yield submodule


module_strategy = st.sampled_from([*_iter_package_api_modules(ground)])


@given(module_strategy)
def test_functions(module: ModuleType) -> None:
    function_signatures = {
        member_name: inspect.signature(member_value)
        for member_name, member_value in vars(module).items()
        if (
            inspect.isfunction(member_value)
            and member_value.__module__ == module.__name__
        )
    }

    assert (
        len(
            invalid_function_signatures := _to_invalid_callable_signatures(
                function_signatures
            )
        )
        == 0
    ), invalid_function_signatures


@given(module_strategy)
def test_class_method_signatures(module: ModuleType) -> None:
    class_own_method_signatures = {
        member_name: {
            field_name: inspect.signature(field_callable)
            for field_name, field_value in vars(member_value).items()
            if (
                (
                    (
                        field_callable := (
                            field_value
                            if inspect.isfunction(field_value)
                            else (
                                field_value.__func__
                                if isinstance(
                                    field_value, (classmethod, staticmethod)
                                )
                                else (
                                    field_value.fget
                                    if isinstance(field_value, property)
                                    else None
                                )
                            )
                        )
                    )
                    is not None
                )
                and (
                    (
                        (field_module := inspect.getmodule(field_callable))
                        is not None
                    )
                    and (
                        field_module.__name__.startswith(ground.__name__ + '.')
                        or field_module.__name__ == ground.__name__
                    )
                )
            )
        }
        for member_name, member_value in vars(module).items()
        if (
            inspect.isclass(member_value)
            and member_value.__module__ == module.__name__
        )
    }

    assert (
        len(
            invalid_class_method_signatures := {
                cls_name: invalid_method_signatures
                for cls_name, cls_method_signatures in (
                    class_own_method_signatures.items()
                )
                if len(
                    invalid_method_signatures := (
                        _to_invalid_callable_signatures(cls_method_signatures)
                    )
                )
                > 0
            }
        )
        == 0
    ), invalid_class_method_signatures


def _to_invalid_callable_signatures(
    callable_signatures: dict[str, inspect.Signature], /
) -> dict[str, inspect.Signature]:
    return {
        name: signature
        for name, signature in callable_signatures.items()
        if not all(
            (
                parameter.kind
                in {
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.KEYWORD_ONLY,
                }
            )
            for parameter in signature.parameters.values()
        )
    }
