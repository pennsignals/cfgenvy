# -*- coding: utf-8 -*-
"""Parser."""

from __future__ import annotations

from argparse import ArgumentParser
from logging import getLogger
from os import environ as osenviron
from sys import argv as sysargv
from typing import IO, Any, Mapping, Optional, Sequence, Type

from .env import Env
from .yaml import yaml_loads

logger = getLogger(__name__)


class Parser:
    """Parser."""

    @classmethod
    def load(
        cls,
        *,
        config_file: str,
        env: Optional[Mapping[str, str]] = None,
        env_cls: Optional[Type[Env]] = None,
        env_file: Optional[str] = None,
    ):
        """Load."""
        _env = env or osenviron
        _env_cls = env_cls or Env

        if env_file:
            logger.debug("Environment variables are only from %s", env_file)
            with open(env_file) as envs:
                with open(config_file) as configs:
                    return cls.loads(
                        configs=configs,
                        env=_env,
                        env_cls=_env_cls,
                        envs=envs,
                    )

        logger.debug("Environment variables are being used.")
        with open(config_file) as configs:
            return cls.loads(
                configs=configs,
                env=_env,
                envs=None,
                env_cls=_env_cls,
            )

    @classmethod
    def loads(
        cls,
        *,
        configs: IO[str],
        env: Optional[Mapping[str, str]] = None,
        envs: Optional[IO[str]] = None,
        env_cls: Optional[Type[Env]] = None,
    ) -> Any:
        """Loads from strings."""
        _env = env or osenviron
        _env_cls = env_cls or Env

        if envs is not None:
            _env = _env_cls.loads(envs)

        _env_cls.as_yaml_type(env=_env)
        cls.yaml_types()
        return yaml_loads(configs)

    @classmethod
    def parse(
        cls,
        *,
        argv: Optional[Sequence[str]] = None,
        env: Optional[Mapping[str, str]] = None,
        env_cls: Optional[Type[Env]] = None,
    ) -> Mapping[str, Any]:
        """Parse."""
        _argv = argv or sysargv[1:]
        _env = env or osenviron
        _env_cls = env_cls or Env

        parser = ArgumentParser()
        parser.add_argument(
            "-c",
            "--config",
            dest="config_file",
            type=str,
            help="configuration yaml file",
            default=_env.get("CONFIG", None),
        )
        parser.add_argument(
            "-e",
            "--env",
            dest="env_file",
            type=str,
            help="env file",
            default=_env.get("ENV", None),
        )
        args = parser.parse_args(_argv)
        if args.config_file is None:
            parser.error(
                " ".join(
                    (
                        "the following arguments are required:",
                        "-c/--config or CONFIG from environment variable",
                    )
                )
            )
        return cls.load(
            config_file=args.config_file,
            env=_env,
            env_file=args.env_file,
            env_cls=_env_cls,
        )

    @classmethod
    def yaml_types(cls):
        """Yaml types."""
        # override and register yaml data types
        # for safe load and dump
        # using yaml_type() and yaml_implicit_type()