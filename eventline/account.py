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


class Account(ReadableAPIObject):
    """A user account."""

    def __init__(self) -> None:
        super().__init__("account")

    def read_data(self, data: Dict[str, Any]) -> None:
        self._read_string(data, "id", attr="id_")
        self._read_string(data, "org_id")
        self._read_datetime(data, "creation_time")
        self._read_boolean(data, "disabled", optional=True)
        self._read_string(data, "email_address")
        self._read_string(data, "name", optional=True)
        self._read_string(data, "role")
        self._read_datetime(data, "last_login_time", optional=True)
        self._read_string(data, "last_project_id", optional=True)
        self._read_object(data, "settings", AccountSettings)


class AccountSettings(ReadableAPIObject):
    """The settings associated with a user account."""

    def __init__(self) -> None:
        super().__init__("account_settings")

    def read_data(self, data: Dict[str, Any]) -> None:
        self._read_string(data, "date_format", optional=True)
