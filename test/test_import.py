# -*- coding: utf-8 -*-
"""Test import."""


def test_import():
    """Test import."""
    import cfgenvy  # pylint: disable=import-outside-toplevel

    assert cfgenvy.Env is not None
    assert cfgenvy.Parser is not None
