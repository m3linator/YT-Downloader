"""
@file test_playlist.py
@brief Unit-Tests für Playlist-Erkennung, Eintragsliste und Parallel-Download.
"""

import threading

import pytest

from downloader import playlist
from downloader.playlist import (
    DownloadReport,
    PlaylistEntry,
    download_parallel,
    fetch_entries,
    has_playlist,
    has_video,
)
from tests.fakes import FakeYDL


@pytest.mark.parametrize(
    ("url", "playlist_expected", "video_expected"),
    [
        ("https://www.youtube.com/watch?v=abc", False, True),
        ("https://www.youtube.com/watch?v=abc&t=116s", False, True),
        ("https://www.youtube.com/watch?v=abc&list=PL1&index=3", True, True),
        ("https://www.youtube.com/playlist?list=PL1", True, False),
        ("https://youtu.be/abc?list=PL1", True, True),
        ("https://www.youtube.com/shorts/abc", False, True),
    ],
)
def test_url_classification(url, playlist_expected, video_expected):
    assert has_playlist(url) is playlist_expected
    assert has_video(url) is video_expected


def test_fetch_entries_keeps_youtube_positions_and_skips_missing(monkeypatch):
    FakeYDL.reset(info={"entries": [
        {"url": "u1", "title": "One"},
        None,  # nicht verfügbares Video
        {"url": "u3", "title": "Three"},
    ]})
    monkeypatch.setattr(playlist, "YoutubeDL", FakeYDL)

    entries = fetch_entries("https://www.youtube.com/playlist?list=PL1")

    assert entries == [PlaylistEntry(1, "u1", "One"), PlaylistEntry(3, "u3", "Three")]
    assert FakeYDL.instances[0].opts["extract_flat"] == "in_playlist"


def test_fetch_entries_returns_empty_list_on_failure(monkeypatch):
    FakeYDL.reset(info=None)
    monkeypatch.setattr(playlist, "YoutubeDL", FakeYDL)
    assert fetch_entries("x") == []


def _entries(n):
    return [PlaylistEntry(i, f"u{i}", f"T{i}") for i in range(1, n + 1)]


def test_download_parallel_reports_success_and_failure_in_order():
    def worker(entry, width):
        if entry.index == 2:
            return False
        if entry.index == 3:
            raise RuntimeError("boom")
        return True

    report = download_parallel(_entries(4), worker, max_workers=4)

    assert report.succeeded == ["01 - T1", "04 - T4"]
    assert report.failed == ["02 - T2", "03 - T3"]
    assert not report.ok


def test_download_parallel_uses_wider_numbering_for_large_playlists():
    widths = set()
    download_parallel(_entries(100), lambda e, w: widths.add(w) or True)
    assert widths == {3}


def test_download_parallel_really_runs_concurrently():
    barrier = threading.Barrier(3, timeout=2)

    def worker(entry, width):
        barrier.wait()  # blockiert, bis 3 Worker gleichzeitig laufen
        return True

    assert download_parallel(_entries(3), worker, max_workers=3).ok


def test_report_ok_requires_at_least_one_success():
    assert not DownloadReport().ok
    assert DownloadReport(succeeded=["a"]).ok
