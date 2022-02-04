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

from typing import Optional
import urllib.parse

from eventline.client import Client
from eventline.account import Account
from eventline.organization import Organization
from eventline.pagination import Cursor, Page


class APIClient(Client):
    """A high level API client for the Eventline API."""

    def get_current_organization(self) -> Organization:
        """Fetch the organization associated with the credentials currently
        used by the client."""
        response = self.send_request("GET", "/org")
        return Organization(response.body)

    def get_current_account(self) -> Account:
        """Fetch the account associated with the credentials currently used
        by the client."""
        response = self.send_request("GET", "/account")
        return Account(response.body)

    def get_accounts(self, /, cursor: Optional[Cursor] = None) -> Page:
        """Fetch all accounts in the organization."""
        response = self.send_request("GET", "/accounts", cursor=cursor)
        return Page(Account, response.body)

    def get_account(self, id_: str) -> Account:
        """Fetch an account by identifier."""
        response = self.send_request(
            "GET", f"/accounts/id/{urllib.parse.quote(id_)}"
        )
        return Account(response.body)
