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

import os
from typing import Optional


def api_key() -> Optional[str]:
    """Return the API key available in the current environment if there is
    one or None if there is not one.
    """
    return os.environ.get("EVENTLINE_API_KEY")


def project_id() -> Optional[str]:
    """Return the identifier of the current project if it is available in the
    current environment.
    """
    return os.environ.get("EVENTLINE_PROJECT_ID")


def context_path() -> Optional[str]:
    """Return the path of the context file if it is available in the current
    environment."""
    return os.environ.get("EVENTLINE_CONTEXT_PATH")
