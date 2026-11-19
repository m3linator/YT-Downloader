"""
@file test_core.py
@brief Unit-Tests für die Download-Steuerung (Einzelvideo vs. Playlist).
"""

from pathlib import Path

import pytest

from downloader import core, playlist, utils
from downloader.playlist import PlaylistEntry
from downloader.utils import CleanTitlePP
from tests.fakes import FakeYDL


@pytest.fixture(autouse=True)
def fake_env(monkeypatch):
    FakeYDL.reset()
    monkeypatch.setattr(core, "YoutubeDL", FakeYDL)
    monkeypatch.setattr(utils, "get_download_dir", lambda: Path("/dl"))


def _opts(outtmpl):
    return {"outtmpl": outtmpl}


def test_single_video_ignores_playlist_and_registers_title_cleaner():
    report = core.download("https://youtube.com/watch?v=a&list=PL", _opts,
                           keep_features=True, whole_playlist=False)

    ydl = FakeYDL.instances[0]
    assert report.ok
    assert ydl.opts["noplaylist"] is True
    assert ydl.opts["outtmpl"] == str(Path("/dl") / "%(title)s.%(ext)s")
    pp, when = ydl.post_processors[0]
    assert isinstance(pp, CleanTitlePP) and pp.keep_features and when == "pre_process"


def test_single_video_failure_is_reported():
    FakeYDL.retcode = 1
    report = core.download("u", _opts, keep_features=False, whole_playlist=False)
    assert not report.ok and report.failed


def test_whole_playlist_downloads_each_entry_with_number(monkeypatch):
    monkeypatch.setattr(core, "fetch_entries",
                        lambda url: [PlaylistEntry(1, "u1", "A"), PlaylistEntry(2, "u2", "B")])

    report = core.download("pl", _opts, keep_features=False, whole_playlist=True)

    assert report.ok and len(report.succeeded) == 2
    by_url = {ydl.urls[0]: ydl.opts for ydl in FakeYDL.instances}
    assert by_url["u1"]["outtmpl"] == str(Path("/dl") / "01 - %(title)s.%(ext)s")
    assert by_url["u2"]["outtmpl"] == str(Path("/dl") / "02 - %(title)s.%(ext)s")
    assert all(opts["quiet"] for opts in by_url.values())


def test_empty_playlist_is_a_failure(monkeypatch):
    monkeypatch.setattr(core, "fetch_entries", lambda url: [])
    assert not core.download("pl", _opts, keep_features=False, whole_playlist=True).ok
