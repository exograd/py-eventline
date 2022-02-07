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

from typing import Optional, TypeVar
import urllib.parse

from eventline.account import Account
from eventline.api_object import ReadableAPIObject
from eventline.client import Client, Response
from eventline.organization import Organization
from eventline.pagination import Cursor, Page
from eventline.project import Project, NewProject, ProjectUpdate

T = TypeVar("T", bound=ReadableAPIObject)


class APIClient(Client):
    """A high level API client for the Eventline API."""

    def get_current_organization(self) -> Organization:
        """Fetch the organization associated with the credentials currently
        used by the client."""
        response = self.send_request("GET", "/org")
        return read_response(response, Organization())

    def get_current_account(self) -> Account:
        """Fetch the account associated with the credentials currently used
        by the client."""
        response = self.send_request("GET", "/account")
        return read_response(response, Account())

    def get_accounts(self, /, cursor: Optional[Cursor] = None) -> Page:
        """Fetch all accounts in the organization."""
        response = self.send_request("GET", "/accounts", cursor=cursor)
        return read_response(response, Page(Account))

    def get_account(self, id_: str) -> Account:
        """Fetch an account by identifier."""
        response = self.send_request("GET", f"/accounts/id/{path_escape(id_)}")
        return read_response(response, Account())

    def get_projects(self, /, cursor: Optional[Cursor] = None) -> Page:
        """Fetch all projects in the organization."""
        response = self.send_request("GET", "/projects", cursor=cursor)
        return read_response(response, Page(Project))

    def create_project(self, new_project: NewProject) -> Project:
        """Create a new project."""
        body = new_project._serialize()
        response = self.send_request("POST", "/projects", body=body)
        return read_response(response, Project())

    def get_project(self, id_: str) -> Project:
        """Fetch a project by identifier."""
        response = self.send_request("GET", f"/projects/id/{path_escape(id_)}")
        return read_response(response, Project())

    def get_project_by_name(self, name: str) -> Project:
        """Fetch a project by name."""
        response = self.send_request(
            "GET", f"/projects/name/{path_escape(name)}"
        )
        return read_response(response, Project())

    def update_project(
        self, id_: str, project_update: ProjectUpdate
    ) -> Project:
        """Update an existing project."""
        body = project_update._serialize()
        response = self.send_request(
            "PUT", f"/projects/id/{path_escape(id_)}", body=body
        )
        return read_response(response, Project())

    def delete_project(self, id_: str) -> None:
        """Delete a project."""
        self.send_request("DELETE", f"/projects/id/{path_escape(id_)}")


def path_escape(string: str) -> str:
    return urllib.parse.quote(string)


def read_response(response: Response, value: T) -> T:
    """Read the content of a response and use it to populate an API object."""
    value._read(response.body)
    return value
