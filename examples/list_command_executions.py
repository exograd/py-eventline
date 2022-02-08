#!/usr/bin/env python

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

import argparse
import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

from tabulate import tabulate

import eventline
import eventline.client

logging.basicConfig(level=logging.INFO)
eventline.client.log.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(
    description="List all accounts in the Eventline organization."
)
parser.add_argument(
    "--project",
    dest="project",
    type=str,
    default="default",
    help="the name of the project",
)
parser.add_argument(
    "--command",
    dest="command",
    type=str,
    default=None,
    help="the name of a command",
)
args = parser.parse_args()

client = eventline.APIClient(project_name=args.project)

# Obtain the command id if there is one
command = None
command_id = None
if args.command is not None:
    command = client.get_resource_by_name("command", args.command)
    command_id = command.id_

# Fetch and print command executions
table = []

cursor = eventline.Cursor(size=20, order="desc")
while cursor is not None:
    page = client.get_command_executions(command_id=command_id, cursor=cursor)
    for execution in page.elements:
        table.append(
            [
                execution.execution_time,
                execution.command_id,
                execution.event_id,
                len(execution.pipeline_ids),
            ]
        )
    cursor = page.next

print(tabulate(table, ["Date", "Command id", "Event id", "Nb pipelines"]))
