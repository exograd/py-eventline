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


class Organization(ReadableAPIObject):
    """An organization."""

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__("organization", data)
        self.read_data()

    def read_data(self) -> None:
        self._read_string("id", attr="id_")
        self._read_string("name")
        self._read_string("address")
        self._read_string("postal_code")
        self._read_string("city")
        self._read_string("country")
        self._read_datetime("creation_time")
        self._read_boolean("disabled", optional=True)
        self._read_string("contact_email_address")
        self._read_boolean("non_essential_mail_opt_in", optional=True)
        self._read_string("vat_id_number", optional=True)
