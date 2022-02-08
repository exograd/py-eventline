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

import eventline

logging.basicConfig(level=logging.INFO)
eventline.client.log.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(description="Execute an Eventline command.")
parser.add_argument(
    "--project",
    dest="project",
    type=str,
    default="default",
    help="the name of the project",
)
parser.add_argument("name", type=str, help="the name of the command")
parser.add_argument(
    "parameter", nargs="*", type=str, help="a command parameter (name=value)"
)
args = parser.parse_args()

client = eventline.APIClient(project_name=args.project)

# Fetch the command to obtain its identifier and the list of definitions for
# its parameters.
command = client.get_resource_by_name("command", args.name)


# Parse parameters passed as command line arguments according to their
# definition.
parameters = {}
parameter_defs = command.spec["data"]["parameters"]

for parameter_string in args.parameter:
    name, value_string = parameter_string.split("=")
    parameter_def = None
    for def_ in parameter_defs:
        if def_["name"] == name:
            parameter_def = def_
            break
    if parameter_def is None:
        print(f"unknown parameter {name}", file=sys.stderr)
        exit(1)
    type_ = parameter_def["type"]
    value = None
    if type_ == "number":
        try:
            value = int(value_string)
        except:
            try:
                value = float(value_string)
            except:
                print(f"invalid number '{value_string}'", file=sys.stderr)
                exit(1)
    elif type_ == "string":
        value = value_string
    elif type_ == "boolean":
        value_string = value_string.lower()
        if value_string == "true":
            value = True
        elif value_string == "false":
            value = False
        else:
            print(f"invalid boolean '{value_string}'", file=sys.stderr)
            exit(1)
    parameters[name] = value

for parameter_def in parameter_defs:
    if "default" in parameter_def:
        continue
    name = parameter_def["name"]
    if name not in parameters:
        print(f"missing parameter {name}", file=sys.stderr)
        exit(1)

# Execute the command
input_ = eventline.CommandExecutionInput(parameters)

execution = client.execute_command(command.id_, input_)

print(f"command executed")

nb_pipelines = len(execution.pipeline_ids)
if nb_pipelines == 1:
    print(f"{nb_pipelines} pipeline created")
else:
    print(f"{nb_pipelines} pipelines created")

print(execution.id_)
