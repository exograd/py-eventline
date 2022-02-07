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

    def __init__(self) -> None:
        super().__init__("organization")

    def _read(self, data: Dict[str, Any]) -> None:
        self.id_ = self._read_string(data, "id")
        self.name = self._read_string(data, "name")
        self.address = self._read_string(data, "address")
        self.postal_code = self._read_string(data, "postal_code")
        self.city = self._read_string(data, "city")
        self.country = self._read_string(data, "country")
        self.creation_time = self._read_datetime(data, "creation_time")
        self.disabled = self._read_optional_boolean(data, "disabled")
        self.contact_email_address = self._read_string(
            data, "contact_email_address"
        )
        self.non_essential_mail_opt_in = self._read_optional_boolean(
            data, "non_essential_mail_opt_in"
        )
        self.vat_id_number = self._read_optional_string(data, "vat_id_number")
