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


class Pipeline(ReadableAPIObject):
    """A pipeline."""

    def __init__(self) -> None:
        super().__init__("pipeline")

    def _read(self, data: Dict[str, Any]) -> None:
        self.id_ = self._read_string(data, "id")
        self.name = self._read_string(data, "name")
        self.org_id = self._read_string(data, "org_id")
        self.project_id = self._read_string(data, "project_id")
        self.creation_time = self._read_datetime(data, "creation_time")
        self.pipeline_id = self._read_optional_string(data, "pipeline_id")
        self.trigger_id = self._read_optional_string(data, "trigger_id")
        self.command_id = self._read_optional_string(data, "command_id")
        self.event_id = self._read_optional_string(data, "event_id")
        self.concurrent = self._read_optional_boolean(data, "concurrent")
        self.status = self._read_string(data, "status")
        self.start_time = self._read_optional_datetime(data, "start_time")
        self.end_time = self._read_optional_datetime(data, "end_time")
