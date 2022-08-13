"""Test cfgenvy."""

from __future__ import annotations

from io import StringIO

from pytest import mark, raises

from cfgenvy import (
    Parser,
    YamlMapping,
    yaml_dump,
    yaml_dumps,
    yaml_load,
    yaml_type,
)


class Service(
    Parser,
    YamlMapping,
):
    """Service."""

    YAML = "!test"

    @classmethod
    def yaml_types(cls) -> None:
        """Yaml types."""
        cls.as_yaml_type()

    def __init__(
        self,
        *,
        host: str,
        password: str,
        username: str,
    ) -> None:
        """__init__."""
        self.host = host
        self.password = password
        self.username = username

    def as_yaml(self) -> dict[str, str]:
        """As yaml."""
        return {
            "host": self.host,
            "password": self.password,
            "username": self.username,
        }


class NoYaml:  # pylint: disable=too-few-public-methods
    """No Yaml."""

    YAML = "!no_yaml"

    @classmethod
    def as_yaml_type(cls, tag: str | None = None) -> None:
        """As yaml type."""
        yaml_type(
            cls,
            tag or cls.YAML,
            init=None,
            repr=None,
        )


CONFIG_FILE = "./test/test.yaml"
NO_ENV_CONFIG_FILE = "./test/no_env_test.yaml"

ENV_FILE = "./test/test.env"

CONFIGS = """
!test
host: 127.0.0.1
password: ${PASSWORD}
username: ${USERNAME}
""".strip()

NO_ENV_CONFIGS = """
!test
host: 127.0.0.1
password: password
username: username
""".strip()

ENVS = """
# a comment

PASSWORD=password
USERNAME=username
""".strip()

BAD_ENVS = """
PSSWRD=password
USERNAME=username
""".strip()

EMPTY_ENVS = """
""".strip()

EXPECTED = """
!test
host: 127.0.0.1
password: password
username: username
""".strip()


def build(expected=EXPECTED):
    """Build."""
    Service.yaml_types()
    return (
        Service,
        {
            "host": "127.0.0.1",
            "password": "password",
            "username": "username",
        },
        expected,
    )


def deserialize_args(
    config_file=CONFIG_FILE,
    env_file=ENV_FILE,
    expected=EXPECTED,
):
    """Deserialize override env."""
    return (
        Service.parse,
        {
            "argv": ["-c", config_file, "-e", env_file],
            "env": {
                "PASSWORD": "nope",
                "USERNAME": "nope",
            },
        },
        expected,
    )


def deserialize_env(
    config_file=CONFIG_FILE,
    expected=EXPECTED,
):
    """Deserialize env."""
    return (
        Service.parse,
        {
            "env": {
                "CONFIG": config_file,
                "PASSWORD": "password",
                "USERNAME": "username",
            }
        },
        expected,
    )


def deserialize_file(
    config_file=CONFIG_FILE,
    env_file=ENV_FILE,
    expected=EXPECTED,
):
    """Deserialize file."""
    return (
        Service.load,
        {
            "config_file": config_file,
            "env_file": env_file,
        },
        expected,
    )


def deserialize_streams(
    configs=CONFIGS,
    envs=ENVS,
    expected=EXPECTED,
):
    """Deserialize string."""
    return (
        Service.loads,
        {
            "configs": StringIO(configs),
            "envs": StringIO(envs),
        },
        expected,
    )


@mark.parametrize(
    "cls,kwargs,expected",
    (
        build(),
        deserialize_streams(),
        deserialize_streams(configs=NO_ENV_CONFIGS),
        deserialize_streams(configs=NO_ENV_CONFIGS, envs=EMPTY_ENVS),
        deserialize_file(),
        deserialize_env(),
        deserialize_args(),
    ),
)
def test_product(cls, kwargs, expected):
    """Test product."""
    product = cls(**kwargs)
    actual = yaml_dumps(product).strip()
    assert actual == expected


def deserialize_bad_streams(
    configs=CONFIGS,
    envs=BAD_ENVS,
):
    """Deserialize bad streams."""
    return (
        Service.loads,
        {
            "configs": StringIO(configs),
            "envs": StringIO(envs),
        },
    )


@mark.parametrize(
    "cls,kwargs",
    (deserialize_bad_streams(),),
)
def test_bad_env(cls, kwargs):
    """Test bad env."""
    with raises(ValueError) as wrapped:
        _ = cls(**kwargs)
    assert wrapped.value.args[0] == "No value for ${PASSWORD}."


def test_files(
    cls=Service,
    config_file=NO_ENV_CONFIG_FILE,
    out_file=NO_ENV_CONFIG_FILE,
):
    """Test file io."""
    cls.yaml_types()
    service = yaml_load(config_file)
    yaml_dump(service, out_file)


def test_no_yaml(cls=NoYaml):
    """Test omitted init or repr."""
    cls.as_yaml_type()


def test_parse_error(cls=Service):
    """Test parse error."""
    cls.yaml_types()
    with raises(SystemExit) as wrapped:
        _ = cls.parse()
    assert wrapped.value.args[0] == 2
