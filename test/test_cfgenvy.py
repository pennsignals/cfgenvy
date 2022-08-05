"""Test cfgenvy."""

from io import StringIO
from typing import Optional

from pytest import mark

from cfgenvy import Parser, yaml_dumps, yaml_type


class Service(Parser):
    """Service."""

    YAML = "!test"

    @classmethod
    def _yaml_init(cls, loader, node):
        """Yaml init."""
        return cls(**loader.construct_mapping(node, deep=True))

    @classmethod
    def _yaml_repr(cls, dumper, self, *, tag: str):
        """Yaml repr."""
        return dumper.represent_mapping(tag, self.as_yaml())

    @classmethod
    def as_yaml_type(cls, tag: Optional[str] = None):
        """As yaml type."""
        yaml_type(
            cls,
            tag or cls.YAML,
            init=cls._yaml_init,
            repr=cls._yaml_repr,
        )

    @classmethod
    def yaml_types(cls):
        """Yaml types."""
        cls.as_yaml_type()

    def __init__(self, password, username):
        """__init__."""
        self.password = password
        self.username = username

    def as_yaml(self):
        """As yaml."""
        return {
            "password": self.password,
            "username": self.username,
        }


CONFIG_FILE = "./test/test.yaml"

ENV_FILE = "./test/test.env"

CONFIGS = """
!test
password: ${PASSWORD}
username: ${USERNAME}
""".strip()

ENVS = """
PASSWORD=password
USERNAME=username
""".strip()

EXPECTED = """
!test
password: password
username: username
""".strip()


def build(expected=EXPECTED):
    """Build."""
    Service.as_yaml_type()
    return (
        Service,
        {
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
