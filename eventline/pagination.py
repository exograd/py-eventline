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

from typing import Any, Dict, Optional

from eventline.api_object import ReadableAPIObject


class Cursor(ReadableAPIObject):
    """A cursor marking a position in a list of paginated objects."""

    def __init__(
        self, /, size: int = 20, sort: str = "id", order: str = "asc"
    ) -> None:
        super().__init__("cursor")
        self.before = None  # type: Optional[str]
        self.after = None  # type: Optional[str]
        self.size = size
        self.sort = sort
        self.order = order

    def read_data(self, data: Dict[str, Any]) -> None:
        self._read_string(data, "before", optional=True)
        self._read_string(data, "after", optional=True)
        self._read_integer(data, "size", optional=True)
        self._read_string(data, "sort", optional=True)
        self._read_string(data, "order", optional=True)


class Page(ReadableAPIObject):
    """A list of objects."""

    def __init__(self, element_class_type: Any) -> None:
        super().__init__("page")
        self.element_class_type = element_class_type

    def read_data(self, data: Dict[str, Any]) -> None:
        self._read_object_array(data, "elements", self.element_class_type)
        self._read_object(data, "previous", Cursor, optional=True)
        self._read_object(data, "next", Cursor, optional=True)
