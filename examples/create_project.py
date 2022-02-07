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

parser = argparse.ArgumentParser(description="Create an Eventline project.")
parser.add_argument("name", type=str, help="the name of the project")
args = parser.parse_args()

new_project = eventline.NewProject(args.name)

client = eventline.APIClient()

project = client.create_project(new_project)

print(f"project {project.id_} created")
