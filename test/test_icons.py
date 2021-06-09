"""
Test icon generation for nodes.
"""
from pathlib import Path
from typing import Dict, Tuple

import pytest

from roentgen.icon import IconSet
from roentgen.grid import IconCollection
from test import SCHEME, SHAPE_EXTRACTOR

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


@pytest.fixture
def init_directories() -> Tuple[Path, Path]:
    """Create temporary directories."""
    temp_directory: Path = Path("temp")
    temp_directory.mkdir(exist_ok=True)

    set_directory: Path = temp_directory / "icon_set"
    set_directory.mkdir(exist_ok=True)

    return temp_directory, set_directory


@pytest.fixture
def init_collection() -> IconCollection:
    """Create collection of all possible icon sets."""
    return IconCollection.from_scheme(SCHEME, SHAPE_EXTRACTOR)


def test_grid(init_collection, init_directories) -> None:
    """Test grid drawing."""
    temp_directory, _ = init_directories
    init_collection.draw_grid(temp_directory / "grid.svg")


def test_icons(init_collection, init_directories) -> None:
    """Test individual icons drawing."""
    _, set_directory = init_directories
    init_collection.draw_icons(set_directory)


def get_icon(tags: Dict[str, str]) -> IconSet:
    """
    Construct icon from tags.
    """
    icon, _ = SCHEME.get_icon(SHAPE_EXTRACTOR, tags)
    return icon


def test_no_icons() -> None:
    """
    Tags that has no description in scheme and should be visualized with default
    shape.
    """
    icon = get_icon({"aaa": "bbb"})
    assert icon.main_icon.is_default()


def test_icon() -> None:
    """
    Tags that should be visualized with single main icon and without extra
    icons.
    """
    icon = get_icon({"natural": "tree"})
    assert not icon.main_icon.is_default()
    assert not icon.extra_icons


def test_icon_1_extra() -> None:
    """
    Tags that should be visualized with single main icon and single extra icon.
    """
    icon = get_icon({"barrier": "gate", "access": "private"})
    assert not icon.main_icon.is_default()
    assert len(icon.extra_icons) == 1


def test_icon_2_extra() -> None:
    """
    Tags that should be visualized with single main icon and two extra icons.
    """
    icon = get_icon({"barrier": "gate", "access": "private", "bicycle": "yes"})
    assert not icon.main_icon.is_default()
    assert len(icon.extra_icons) == 2


def test_no_icon_1_extra() -> None:
    """
    Tags that should be visualized with default main icon and single extra icon.
    """
    icon = get_icon({"access": "private"})
    assert icon.main_icon.is_default()
    assert len(icon.extra_icons) == 1


def test_no_icon_2_extra() -> None:
    """
    Tags that should be visualized with default main icon and two extra icons.
    """
    icon = get_icon({"access": "private", "bicycle": "yes"})
    assert icon.main_icon.is_default()
    assert len(icon.extra_icons) == 2
