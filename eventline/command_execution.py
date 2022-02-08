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

from eventline.api_object import ReadableAPIObject, SerializableAPIObject


class CommandExecutionInput(SerializableAPIObject):
    """The set of data used to execute a command."""

    def __init__(self, parameters: Dict[str, Any]) -> None:
        super().__init__("command_execution_input")
        self.parameters = parameters

    def _serialize(self) -> Dict[str, Any]:
        data = {"parameters": self.parameters}
        return data


class CommandExecution(ReadableAPIObject):
    """A representation of the execution of a command."""

    def __init__(self) -> None:
        super().__init__("command_execution")

    def _read(self, data: Dict[str, Any]) -> None:
        self.id_ = self._read_string(data, "id")
        self.org_id = self._read_string(data, "org_id")
        self.project_id = self._read_string(data, "project_id")
        self.executor_id = self._read_optional_string(data, "executor_id")
        self.execution_time = self._read_datetime(data, "execution_time")
        self.command_id = self._read_string(data, "command_id")
        self.parameters = data["parameters"]
        self.event_id = self._read_string(data, "event_id")
        self.pipeline_ids = self._read_string_array(data, "pipeline_ids")
