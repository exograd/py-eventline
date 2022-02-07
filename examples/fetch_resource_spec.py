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

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))

import eventline

logging.basicConfig(level=logging.INFO)
eventline.client.log.setLevel(logging.DEBUG)


def string_presenter(dumper, string):
    tag = "tag:yaml.org,2002:str"
    if "\n" in string:
        return dumper.represent_scalar(tag, string, style="|")
    return dumper.represent_scalar(tag, string)


yaml.add_representer(str, string_presenter)

parser = argparse.ArgumentParser(
    description="Fetch and print the specification of a resource."
)
parser.add_argument(
    "--project",
    dest="project",
    type=str,
    default="default",
    help="the name of the project",
)
parser.add_argument(
    "type",
    type=str,
    choices=["trigger", "pipeline", "task", "command"],
    help="the type of the resource",
)
parser.add_argument("name", type=str, help="the name of the resource")
args = parser.parse_args()

client = eventline.APIClient(project_name=args.project)

resource = client.get_resource_by_name(args.type, args.name)
print(yaml.dump(resource.spec))
