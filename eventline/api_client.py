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

from typing import Dict, List, Optional, TypeVar
import urllib.parse

from eventline.account import Account
from eventline.api_object import ReadableAPIObject
from eventline.client import Client, Response
from eventline.command_execution import CommandExecutionInput, CommandExecution
from eventline.event import Event, NewEvent
from eventline.organization import Organization
from eventline.pagination import Cursor, Page
from eventline.pipeline import Pipeline
from eventline.project import Project, NewProject, ProjectUpdate
from eventline.resource import Resource
from eventline.task import Task

ResponseObjectType = TypeVar("ResponseObjectType", bound=ReadableAPIObject)


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
        """Fetch projects in the organization."""
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

    def get_resources(self, /, cursor: Optional[Cursor] = None) -> Page:
        """Fetch resources in the project."""
        response = self.send_request("GET", "/resources", cursor=cursor)
        return read_response(response, Page(Resource))

    def get_resource(self, id_: str) -> Resource:
        """Fetch a resource by identifier."""
        response = self.send_request(
            "GET", f"/resources/id/{path_escape(id_)}"
        )
        return read_response(response, Resource())

    def get_resource_by_name(self, type_: str, name: str) -> Resource:
        """Fetch a resource by type and name."""
        response = self.send_request(
            "GET",
            f"/resources/type/{path_escape(type_)}/name/{path_escape(name)}",
        )
        return read_response(response, Resource())

    def execute_command(
        self, id_: str, input_: CommandExecutionInput
    ) -> CommandExecution:
        """Execute a command and return the associated command execution
        object."""
        body = input_._serialize()
        response = self.send_request(
            "POST", f"/commands/id/{path_escape(id_)}/execute", body=body
        )
        return read_response(response, CommandExecution())

    def get_command_executions(
        self,
        /,
        command_id: Optional[str] = None,
        cursor: Optional[Cursor] = None,
    ) -> Page:
        """Fetch a list of command executions."""
        query_parameters = {}
        if command_id is not None:
            query_parameters["command"] = command_id
        response = self.send_request(
            "GET",
            "/command_executions",
            query_parameters=query_parameters,
            cursor=cursor,
        )
        return read_response(response, Page(CommandExecution))

    def get_command_execution(self, id_: str) -> CommandExecution:
        """Fetch a command execution by identifier."""
        response = self.send_request(
            "GET", f"/command_executions/id/{path_escape(id_)}"
        )
        return read_response(response, CommandExecution())

    def create_event(self, new_event: NewEvent) -> List[Event]:
        """Create a new custom event."""
        body = new_event._serialize()
        response = self.send_request("POST", "/events", body=body)
        events = []
        for value_object in response.body:
            value = Event()
            value._read(value_object)
            events.append(value)
        return events

    def replay_event(self, id_: str) -> Event:
        """Replay an existing event."""
        response = self.send_request(
            "POST", f"/events/id/{path_escape(id_)}/replay"
        )
        return read_response(response, Event())

    def get_pipelines(self, /, cursor: Optional[Cursor] = None) -> Page:
        """Fetch pipelines in the project."""
        response = self.send_request("GET", "/pipelines", cursor=cursor)
        return read_response(response, Page(Pipeline))

    def get_pipeline(self, id_: str) -> Pipeline:
        """Fetch a pipeline by identifier."""
        response = self.send_request(
            "GET", f"/pipelines/id/{path_escape(id_)}"
        )
        return read_response(response, Pipeline())

    def abort_pipeline(self, id_: str) -> None:
        """Abort a pipeline."""
        self.send_request("POST", f"/pipelines/id/{path_escape(id_)}/abort")

    def restart_pipeline(self, id_: str) -> None:
        """Restart a finished pipeline."""
        self.send_request("POST", f"/pipelines/id/{path_escape(id_)}/restart")

    def restart_pipeline_from_failure(self, id_: str) -> None:
        """Restart the failed tasks in a finished pipeline."""
        self.send_request(
            "POST", f"/pipelines/id/{path_escape(id_)}/restart_from_failure"
        )

    def get_scratchpad(self, id_: str) -> Dict[str, str]:
        """Fetch all entries in a scratchpad."""
        response = self.send_request(
            "GET", f"/pipelines/id/{path_escape(id_)}/scratchpad"
        )
        return response.body

    def delete_scratchpad(self, id_: str) -> None:
        """Delete all entries in a scratchpad."""
        self.send_request(
            "DELETE", f"/pipelines/id/{path_escape(id_)}/scratchpad"
        )

    def get_scratchpad_entry(self, id_: str, key: str) -> str:
        """Fetch an entry in a scratchpad."""
        response = self.send_request(
            "GET",
            f"/pipelines/id/{path_escape(id_)}/scratchpad"
            f"/key/{path_escape(key)}",
        )
        return response.body

    def set_scratchpad_entry(self, id_: str, key: str, value: str) -> None:
        """set the value of an entry in a scratchpad."""
        self.send_request(
            "PUT",
            f"/pipelines/id/{path_escape(id_)}/scratchpad"
            f"/key/{path_escape(key)}",
            body=value,
            raw_body=True,
        )

    def delete_scratchpad_entry(self, id_: str, key: str) -> None:
        """Delete an entry in a scratchpad."""
        self.send_request(
            "DELETE",
            f"/pipelines/id/{path_escape(id_)}/scratchpad"
            f"/key/{path_escape(key)}",
        )

    def get_tasks(self, /, cursor: Optional[Cursor] = None) -> Page:
        """Fetch tasks in the project."""
        response = self.send_request("GET", "/tasks", cursor=cursor)
        return read_response(response, Page(Task))

    def get_task(self, id_: str) -> Task:
        """Fetch a task by identifier."""
        response = self.send_request("GET", f"/tasks/id/{path_escape(id_)}")
        return read_response(response, Task())

    def get_events(self, /, cursor: Optional[Cursor] = None) -> Page:
        """Fetch a list of events."""
        response = self.send_request("GET", "/events", cursor=cursor)
        return read_response(response, Page(Event))

    def get_event(self, id_: str) -> Event:
        """Fetch an event by identifier."""
        response = self.send_request("GET", f"/events/id/{path_escape(id_)}")
        return read_response(response, Event())


def path_escape(string: str) -> str:
    return urllib.parse.quote(string)


def read_response(
    response: Response, value: ResponseObjectType
) -> ResponseObjectType:
    """Read the content of a response and use it to populate an API object."""
    value._read(response.body)
    return value
