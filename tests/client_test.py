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

import pytest

from eventline.client import ClientError, APIError, Client


def test_invalid_endpoint():
    with pytest.raises(ClientError):
        Client(endpoint="ftp://eventline.net")


def test_build_uri_default_endpoint():
    c = Client()
    assert c.build_uri("/") == f"{Client.default_endpoint}/"
    assert c.build_uri("/status") == f"{Client.default_endpoint}/status"


def test_build_uri_custom_endpoint():
    c = Client(endpoint="https://example.com/test")
    assert c.build_uri("/") == "https://example.com/test/"
    assert c.build_uri("/status") == "https://example.com/test/status"


def test_send_request_status():
    c = Client()
    res = c.send_request("GET", "/status")
    assert res.status == 200


def test_send_request_error():
    c = Client()
    with pytest.raises(APIError) as exinfo:
        c.send_request("GET", "/does_not_exist")
    ex = exinfo.value
    assert ex.status == 404
    assert ex.error_code == "route_not_found"
