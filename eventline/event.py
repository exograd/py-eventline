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
from typing import Any, Optional, Dict

from eventline.api_object import ReadableAPIObject, SerializableAPIObject


class Event(ReadableAPIObject):
    """An event."""

    def __init__(self) -> None:
        super().__init__("event")

    def _read(self, data: Dict[str, Any]) -> None:
        self.id_ = self._read_string(data, "id")
        self.org_id = self._read_string(data, "org_id")
        self.project_id = self._read_string(data, "project_id")
        self.trigger_id = self._read_optional_string(data, "trigger_id")
        self.command_id = self._read_optional_string(data, "command_id")
        self.creation_time = self._read_datetime(data, "creation_time")
        self.event_time = self._read_datetime(data, "event_time")
        self.connector = self._read_string(data, "connector")
        self.name = self._read_string(data, "name")
        self.data = data["data"]
        self.original_event_id = data["original_event_id"]


class NewEvent(SerializableAPIObject):
    """A new event."""

    def __init__(
        self,
        connector: str,
        name: str,
        data: Dict[str, Any],
        /,
        event_time: Optional[datetime.datetime] = None,
    ) -> None:
        super().__init__("new_event")
        self.event_time = event_time
        self.connector = connector
        self.name = name
        self.data = data

    def _serialize(self) -> Dict[str, Any]:
        data = {
            "connector": self.connector,
            "name": self.name,
            "data": self.data,
        }  # type: Dict[str, Any]
        if self.event_time is not None:
            event_time = self.event_time.replace(tzinfo=datetime.timezone.utc)
            data["event_time"] = event_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return data
