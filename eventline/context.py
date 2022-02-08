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

import json
from typing import Any, Dict, Optional

from eventline.api_object import ReadableAPIObject
from eventline.event import Event
import eventline.environment


class Context(ReadableAPIObject):
    """A runtime context."""

    def __init__(self) -> None:
        super().__init__("context")

    def _read(self, data: Dict[str, Any]) -> None:
        self.event = self._read_object(data, "event", Event)
        self.task_parameters = data["task_parameters"]
        self.instance_id = self._read_integer(data, "instance_id")
        self.identities = data["identities"]


def load_context(path: Optional[str] = None) -> Context:
    """Load and return a context object. If the path parameter is None, use the
    EVENTLINE_CONTEXT_PATH environment variable.
    """
    if path is None:
        path = eventline.environment.context_path()
        if path is None:
            raise Exception("no context path available")
    content = None
    with open(path, "r", encoding="UTF-8") as file:
        content = file.read()
    data = json.loads(content)
    context = Context()
    context._read(data)
    return context
