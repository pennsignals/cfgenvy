# -*- coding: utf-8 -*-
"""Test import."""


def test_import():
    """Test import."""
    import envyaml  # pylint: disable=import-outside-toplevel

    assert envyaml.Env is not None
