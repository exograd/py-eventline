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

from typing import Any, Dict

from eventline.api_object import ReadableAPIObject


class Cursor(ReadableAPIObject):
    """A cursor marking a position in a list of paginated objects."""

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__("cursor", data)
        self.read_data()

    def read_data(self) -> None:
        self._read_string("before", optional=True)
        self._read_string("after", optional=True)
        self._read_integer("size", optional=True)
        self._read_string("sort", optional=True)
        self._read_string("order", optional=True)


class Page(ReadableAPIObject):
    """A list of objects."""

    def __init__(self, element_class_type: Any, data: Dict[str, Any]) -> None:
        super().__init__("page", data)
        self.element_class_type = element_class_type
        self.read_data()

    def read_data(self) -> None:
        self._read_object_array("elements", self.element_class_type)
        self._read_object("previous", Cursor, optional=True)
        self._read_object("next", Cursor, optional=True)
