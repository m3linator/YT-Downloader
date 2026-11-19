"""
@file test_utils.py
@brief Unit-Tests für Titel-Säuberung, Postprocessor und yt-dlp-Optionen.
"""

from pathlib import Path

import pytest

from downloader import utils
from downloader.utils import CleanTitlePP, base_ydl_opts, build_outtmpl, clean_title, split_artist


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Artist - Song (Official Video)", "Song"),
        ("Artist – Song [HD]", "Song"),
        ("Artist - Song | Official Audio", "Song"),
        ("Artist - Song (Live in Berlin)", "Song (Live in Berlin)"),
        ("Song (Remix) (Lyrics)", "Song (Remix)"),
        ("Song: Part 1?", "Song Part 1"),
        ("", ""),
    ],
)
def test_clean_title(raw, expected):
    assert clean_title(raw) == expected


def test_clean_title_keeps_features_for_audio():
    assert clean_title("A - Song (feat. B) (Official Audio)", keep_features=True) == "Song (feat. B)"


def test_clean_title_drops_features_for_video():
    assert clean_title("A - Song (feat. B) (Official Video)") == "Song"


def test_split_artist():
    assert split_artist("Kanye West - Bound 2") == ("Kanye West", "Bound 2")
    assert split_artist("Just a title") == (None, "Just a title")


def _run_pp(info, keep_features=True):
    _, result = CleanTitlePP(keep_features=keep_features).run(info)
    return result


def test_pp_sets_artist_from_title_when_missing():
    info = _run_pp({"title": "Kanye West - Bound 2 (Official Audio)"})
    assert info["title"] == "Bound 2"
    assert info["artist"] == "Kanye West"


def test_pp_keeps_existing_artist():
    info = _run_pp({"title": "Someone - Song", "artist": "Real Artist"})
    assert info["artist"] == "Real Artist"


def test_build_outtmpl_without_and_with_index(monkeypatch):
    monkeypatch.setattr(utils, "get_download_dir", lambda: Path("/dl"))
    assert build_outtmpl() == str(Path("/dl") / "%(title)s.%(ext)s")
    assert build_outtmpl(3) == str(Path("/dl") / "03 - %(title)s.%(ext)s")
    assert build_outtmpl(7, width=3) == str(Path("/dl") / "007 - %(title)s.%(ext)s")


def test_base_opts_do_not_force_player_clients():
    opts = base_ydl_opts()
    assert "extractor_args" not in opts
    assert opts["concurrent_fragment_downloads"] > 1
    assert opts["ignoreerrors"] is True


def test_base_opts_accept_custom_outtmpl():
    assert base_ydl_opts(outtmpl="x")["outtmpl"] == "x"
