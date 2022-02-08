# Copyright (c) 2022 Exograd SAS.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
# IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import datetime
from typing import Any, Dict, List, Optional, TypeVar, Type


import dateutil.parser

FieldType = TypeVar("FieldType", str, datetime.datetime, int, bool, dict, list)


class InvalidAPIObjectError(Exception):
    """An error signaled when an API object contains invalid data."""

    def __init__(self, object_name: str, value: Any, reason: str) -> None:
        super().__init__(f"invalid {object_name}: {reason}")

        self.object_name = object_name
        self.value = value
        self.reason = reason


class APIObject:
    """An object exposed by the Eventline API."""

    def __init__(self, object_name: str):
        self._object_name = object_name

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        string = f"<eventline.{self._object_name}"
        if hasattr(self, "id_"):
            id_ = getattr(self, "id_")
            if id_ is not None:
                string += f" {id_}"
        string += ">"
        return string


class ReadableAPIObject(APIObject):
    """An API object which can be read from a JSON object."""

    def _read(self, data: Dict[str, Any]) -> None:
        pass

    def _get_optional_field(
        self,
        data: Dict[str, Any],
        key: str,
        class_type: Type[FieldType],
        class_name: str,
    ) -> Optional[FieldType]:
        if not isinstance(data, dict):
            raise InvalidAPIObjectError(
                "response", data, "response data are not an object"
            )
        if key not in data:
            return None
        value = data.get(key, None)
        if value is not None and not isinstance(value, class_type):
            article = "a"
            if class_name[0] in ("a", "e", "i", "o", "u"):
                article = "an"
            raise InvalidAPIObjectError(
                self._object_name,
                value,
                f"field '{key}' is not {article} {class_name}",
            )
        return value

    def _get_field(
        self,
        data: Dict[str, Any],
        key: str,
        class_type: Type[FieldType],
        class_name: str,
    ) -> FieldType:
        value = self._get_optional_field(data, key, class_type, class_name)
        if value is None:
            raise InvalidAPIObjectError(
                self._object_name, data, f"missing field '{key}'"
            )
        return value

    def _read_optional_string(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> Optional[str]:
        return self._get_optional_field(data, key, str, "string")

    def _read_string(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> str:
        return self._get_field(data, key, str, "string")

    def _read_optional_datetime(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> Optional[datetime.datetime]:
        string = self._get_field(data, key, str, "string")
        value = None
        if string is not None:
            try:
                value = dateutil.parser.isoparse(string)
            except Exception as ex:
                raise InvalidAPIObjectError(
                    self._object_name,
                    string,
                    f"field '{key}' is not a valid datetime",
                ) from ex
        return value

    def _read_datetime(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> datetime.datetime:
        value = self._read_optional_datetime(data, key)
        if value is None:
            raise InvalidAPIObjectError(
                self._object_name, data, f"missing field '{key}'"
            )
        return value

    def _read_optional_integer(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> Optional[int]:
        return self._get_optional_field(data, key, int, "integer")

    def _read_integer(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> int:
        return self._get_field(data, key, int, "integer")

    def _read_optional_boolean(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> Optional[bool]:
        value = self._get_optional_field(data, key, bool, "boolean")
        if value is None:
            value = False
        return value

    def _read_boolean(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> bool:
        return self._get_field(data, key, bool, "boolean")

    def _read_optional_object(
        self,
        data: Dict[str, Any],
        key: str,
        class_type: Any,
    ) -> Optional[object]:
        obj = self._get_optional_field(data, key, dict, "object")
        value = None
        if obj is not None:
            value = class_type()
            value._read(obj)
        return value

    def _read_object(
        self,
        data: Dict[str, Any],
        key: str,
        class_type: Any,
    ) -> object:
        value = self._read_optional_object(data, key, class_type)
        if value is None:
            raise InvalidAPIObjectError(
                self._object_name, data, f"missing field '{key}'"
            )
        return value

    def _read_optional_object_array(
        self,
        data: Dict[str, Any],
        key: str,
        element_class_type: Any,
    ) -> Optional[List[object]]:
        array = self._get_field(data, key, list, "array")
        value = None
        if array is not None:
            value = []
            for i, element in enumerate(array):
                if not isinstance(element, dict):
                    raise InvalidAPIObjectError(
                        self._object_name,
                        element,
                        f"element at index {i} of field '{key}' is not an "
                        "object",
                    )
                element_value = element_class_type()
                element_value._read(element)
                value.append(element_value)
        return value

    def _read_object_array(
        self,
        data: Dict[str, Any],
        key: str,
        element_class_type: Any,
    ) -> List[object]:
        value = self._read_optional_object_array(data, key, element_class_type)
        if value is None:
            raise InvalidAPIObjectError(
                self._object_name, data, f"missing field '{key}'"
            )
        return value

    def _read_optional_string_array(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> Optional[List[str]]:
        array = self._get_field(data, key, list, "array")
        value = None
        if array is not None:
            value = []
            for i, element in enumerate(array):
                if not isinstance(element, str):
                    raise InvalidAPIObjectError(
                        self._object_name,
                        element,
                        f"element at index {i} of field '{key}' is not a "
                        "string",
                    )
                value.append(element)
        return value

    def _read_string_array(
        self,
        data: Dict[str, Any],
        key: str,
    ) -> List[str]:
        value = self._read_optional_string_array(data, key)
        if value is None:
            raise InvalidAPIObjectError(
                self._object_name, data, f"missing field '{key}'"
            )
        return value


class SerializableAPIObject(APIObject):
    """An API object which can be serialized to a JSON object."""

    def _serialize(self) -> Dict[str, Any]:
        return {}
