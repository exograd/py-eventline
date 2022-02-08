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
import json
import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

import eventline

logging.basicConfig(level=logging.INFO)
eventline.client.log.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(description="Create a custom event.")
parser.add_argument(
    "--project",
    dest="project",
    type=str,
    default="default",
    help="the name of the project",
)
parser.add_argument("name", type=str, help="the name of the event")
parser.add_argument(
    "data",
    nargs="?",
    type=str,
    help='the JSON object representing event data ("-" to read stdin)',
)
args = parser.parse_args()

client = eventline.APIClient(project_name=args.project)

# Parse event data
data_string = args.data
if data_string == "-":
    data_string = sys.stdin.read()

data = json.loads(data_string)

# Create the event
new_event = eventline.NewEvent("custom", args.name, data)

events = client.create_event(new_event)

nb_events = len(events)
if nb_events == 1:
    print(f"{nb_events} event created:")
else:
    print(f"{nb_events} events created:")

for event in events:
    print(event.id_)
