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
from typing import Any, Dict, Optional


import dateutil.parser


class InvalidObjectError(Exception):
    """An error signaled when an API object contains invalid data."""

    def __init__(self, object_name: str, value: Any, reason: str) -> None:
        super().__init__(f"invalid {object_name}: {reason}")

        self.object_name = object_name
        self.value = value
        self.reason = reason


class APIObject:
    """An object exposed by the Eventline API."""

    def __init__(self, object_name: str):
        self.object_name = object_name

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        string = f"<eventline.{self.object_name}"
        if hasattr(self, "id_"):
            id_ = getattr(self, "id_")
            if id_ is not None:
                string += f" {id_}"
        string += ">"
        return string


class ReadableAPIObject(APIObject):
    """An API object which can be read from a JSON object."""

    def __init__(self, object_name: str, data: Dict[str, Any]) -> None:
        super().__init__(object_name)
        self._raw_data = data

    def _get_field(
        self,
        key: str,
        class_type: Any,
        class_name: str,
        /,
        optional: bool = False,
        default: Optional[Any] = None,
    ) -> Any:
        if optional is False and key not in self._raw_data:
            raise InvalidObjectError(
                self.object_name, self._raw_data, f"missing field '{key}'"
            )
        value = self._raw_data.get(key, default)
        if not isinstance(value, class_type):
            article = "a"
            if class_type[0] in ("a", "e", "i", "o", "u"):
                article = "an"
            raise InvalidObjectError(
                self.object_name,
                value,
                f"field '{key}' is not {article} {class_name}",
            )
        return value

    def _read_string(
        self,
        key: str,
        /,
        optional: bool = False,
        default: Optional[str] = None,
        attr: Optional[str] = None,
    ) -> None:
        value = self._get_field(
            key, str, "string", optional=optional, default=default
        )
        if attr is None:
            attr = key
        setattr(self, attr, value)

    def _read_datetime(
        self,
        key: str,
        /,
        optional: bool = False,
        default: Optional[datetime.datetime] = None,
        attr: Optional[str] = None,
    ) -> None:
        string = self._get_field(key, str, "string", optional=optional)
        value = default
        if string is not None:
            try:
                value = dateutil.parser.isoparse(string)
            except Exception as ex:
                raise InvalidObjectError(
                    self.object_name,
                    string,
                    f"field '{key}' is not a valid datetime",
                ) from ex
        if attr is None:
            attr = key
        setattr(self, attr, value)

    def _read_boolean(
        self,
        key: str,
        /,
        optional: bool = False,
        default: bool = False,
        attr: Optional[str] = None,
    ) -> None:
        value = self._get_field(
            key, bool, "boolean", optional=optional, default=default
        )
        if attr is None:
            attr = key
        setattr(self, attr, value)

    def _read_object(
        self,
        key: str,
        class_type: Any,
        /,
        attr: Optional[str] = None,
    ) -> None:
        obj = self._get_field(key, dict, "object")
        value = class_type(obj)
        if attr is None:
            attr = key
        setattr(self, attr, value)
