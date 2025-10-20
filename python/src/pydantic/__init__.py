from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, TypeVar, Union, get_args, get_origin, Literal

__all__ = [
    "BaseModel",
    "Field",
    "ValidationError",
    "field_validator",
]


class ValidationError(Exception):
    def __init__(self, errors: Sequence[Dict[str, Any]]):
        super().__init__("validation failed")
        self._errors = list(errors)

    def errors(self) -> List[Dict[str, Any]]:
        return list(self._errors)

    @classmethod
    def from_exception_data(
        cls, title: str, errors: Sequence[Dict[str, Any]]
    ) -> "ValidationError":  # pragma: no cover - simple helper
        processed: List[Dict[str, Any]] = []
        for error in errors:
            entry = dict(error)
            ctx = dict(entry.get("ctx", {}))
            if "model" not in ctx:
                ctx["model"] = title
            if ctx:
                entry["ctx"] = ctx
            processed.append(entry)
        return cls(processed)


class _UndefinedType:
    pass


Undefined = _UndefinedType()


@dataclass
class FieldInfo:
    default: Any = Undefined
    ge: Optional[float] = None
    le: Optional[float] = None


def Field(*, default: Any = Undefined, ge: Optional[float] = None, le: Optional[float] = None) -> FieldInfo:
    return FieldInfo(default=default, ge=ge, le=le)


def field_validator(*fields: str):
    def decorator(func):
        actual = func
        is_classmethod = False
        if isinstance(func, classmethod):  # pragma: no cover - defensive
            actual = func.__func__
            is_classmethod = True
        actual._validator_fields = fields  # type: ignore[attr-defined]
        actual._validator_is_classmethod = is_classmethod  # type: ignore[attr-defined]
        return func

    return decorator


T = TypeVar("T", bound="BaseModel")


class BaseModelMeta(type):
    def __new__(mcls, name, bases, namespace):
        annotations = namespace.get("__annotations__", {})
        field_definitions: Dict[str, Tuple[Any, FieldInfo]] = {}

        validators: Dict[str, List[Tuple[Any, bool]]] = {}
        for base in bases:
            base_validators = getattr(base, "__field_validators__", {})
            for key, funcs in base_validators.items():
                validators.setdefault(key, []).extend(funcs)

        for field_name, annotation in annotations.items():
            default = namespace.get(field_name, Undefined)
            if isinstance(default, FieldInfo):
                field_info = default
                namespace.pop(field_name)
            elif default is not Undefined:
                field_info = FieldInfo(default=default)
            else:
                field_info = FieldInfo()
            field_definitions[field_name] = (annotation, field_info)

        for attr_name, attr_value in list(namespace.items()):
            attr = attr_value
            is_classmethod = False
            if isinstance(attr_value, classmethod):
                attr = attr_value.__func__
                is_classmethod = True
            if hasattr(attr, "_validator_fields"):
                fields = getattr(attr, "_validator_fields")
                for field in fields:
                    validators.setdefault(field, []).append((attr, is_classmethod or getattr(attr, "_validator_is_classmethod", False)))

        cls = super().__new__(mcls, name, bases, dict(namespace))
        cls.__field_definitions__ = field_definitions
        cls.__field_validators__ = validators
        config = namespace.get("model_config") or {}
        if isinstance(config, dict):
            cls.__allow_extra__ = config.get("extra") == "allow"
        else:
            cls.__allow_extra__ = True
        return cls


class BaseModel(metaclass=BaseModelMeta):
    __field_definitions__: Dict[str, Tuple[Any, FieldInfo]]
    __field_validators__: Dict[str, List[Tuple[Any, bool]]]
    __allow_extra__: bool = True

    @classmethod
    def model_validate(cls: Type[T], data: Any) -> T:
        if not isinstance(data, dict):
            raise ValidationError([{ "loc": ("__root__",), "msg": "expected object", "type": "type_error" }])

        values: Dict[str, Any] = {}
        errors: List[Dict[str, Any]] = []
        for name, (annotation, field_info) in cls.__field_definitions__.items():
            if name in data:
                raw_value = data[name]
            elif field_info.default is not Undefined:
                raw_value = field_info.default
            else:
                errors.append({"loc": (name,), "msg": "Field required", "type": "missing"})
                continue
            try:
                value = _coerce_value(annotation, raw_value)
                value = _apply_constraints(name, value, field_info)
                value = _run_validators(cls, name, value)
            except ValidationError as sub:
                errors.extend(sub.errors())
                continue
            except ValueError as exc:
                errors.append({"loc": (name,), "msg": str(exc), "type": "value_error"})
                continue
            values[name] = value

        if errors:
            raise ValidationError(errors)

        extra: Dict[str, Any] = {}
        if cls.__allow_extra__:
            for key, value in data.items():
                if key not in values:
                    extra[key] = value
        elif any(key not in cls.__field_definitions__ for key in data):
            unknowns = [key for key in data if key not in cls.__field_definitions__]
            raise ValidationError([{ "loc": tuple(unknowns), "msg": "extra fields not permitted", "type": "value_error" }])

        instance = cls.__new__(cls)
        for key, value in values.items():
            setattr(instance, key, value)
        instance.__extra__ = extra
        return instance

    def model_dump(self, mode: str = "python") -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for name in self.__field_definitions__:
            value = getattr(self, name, None)
            result[name] = _dump_value(value)
        extras = getattr(self, "__extra__", {})
        for key, value in extras.items():
            result[key] = _dump_value(value)
        return result


def _run_validators(cls: Type[BaseModel], name: str, value: Any) -> Any:
    funcs = cls.__field_validators__.get(name, [])
    for func, is_classmethod in funcs:
        if is_classmethod:
            value = func(cls, value)
        else:
            value = func(value)
    return value


def _apply_constraints(name: str, value: Any, field_info: FieldInfo) -> Any:
    if isinstance(value, (int, float)):
        if field_info.ge is not None and value < field_info.ge:
            raise ValueError(f"{name} < {field_info.ge}")
        if field_info.le is not None and value > field_info.le:
            raise ValueError(f"{name} > {field_info.le}")
    return value


def _coerce_value(annotation: Any, value: Any) -> Any:
    if annotation is Any:
        return value
    origin = get_origin(annotation)
    if origin is Union:
        errors: List[Dict[str, Any]] = []
        for arg in get_args(annotation):
            try:
                return _coerce_value(arg, value)
            except ValidationError as err:
                errors.extend(err.errors())
            except ValueError:
                continue
        if errors:
            raise ValidationError(errors)
        raise ValueError("value does not match any type in Union")
    if origin in (list, List):
        if not isinstance(value, list):
            raise ValueError("expected list")
        item_type = get_args(annotation)[0] if get_args(annotation) else Any
        return [_coerce_value(item_type, item) for item in value]
    if origin in (dict, Dict):
        if not isinstance(value, dict):
            raise ValueError("expected dict")
        key_type, val_type = get_args(annotation) if get_args(annotation) else (Any, Any)
        return {
            _coerce_value(key_type, key): _coerce_value(val_type, val)
            for key, val in value.items()
        }
    if origin is Literal:
        choices = get_args(annotation)
        if value not in choices:
            raise ValueError(f"expected one of {choices}")
        return value
    if isinstance(annotation, type) and issubclass_safe(annotation, BaseModel):
        return annotation.model_validate(value)
    if annotation in (str, int, float, bool):
        if annotation is str:
            if not isinstance(value, str):
                raise ValueError("expected string")
            return value
        if annotation is bool:
            if not isinstance(value, bool):
                raise ValueError("expected bool")
            return value
        if annotation is int:
            if isinstance(value, bool):
                raise ValueError("expected int")
            if not isinstance(value, (int, float)):
                raise ValueError("expected int")
            return int(value)
        if annotation is float:
            if not isinstance(value, (int, float)):
                raise ValueError("expected float")
            return float(value)
    if annotation is type(None):
        if value is not None:
            raise ValueError("expected null")
        return None
    return value


def _dump_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump()
    if isinstance(value, list):
        return [_dump_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _dump_value(val) for key, val in value.items()}
    return value


def issubclass_safe(obj: Any, cls: Type[BaseModel]) -> bool:
    try:
        return issubclass(obj, cls)
    except TypeError:
        return False
