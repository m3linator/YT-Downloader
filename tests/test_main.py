"""
@file test_main.py
@brief Unit-Tests für die Benutzerführung in main.py.
"""

import pytest

import main
from downloader.playlist import DownloadReport


def _answers(*values):
    it = iter(values)
    return lambda prompt="": next(it)


@pytest.mark.parametrize(
    ("url", "answer", "expected"),
    [
        ("https://www.youtube.com/watch?v=a", None, False),
        ("https://www.youtube.com/playlist?list=PL", None, True),
        ("https://www.youtube.com/watch?v=a&list=PL", "1", False),
        ("https://www.youtube.com/watch?v=a&list=PL", "2", True),
        ("https://www.youtube.com/watch?v=a&list=PL", "", False),
    ],
)
def test_ask_whole_playlist(url, answer, expected):
    assert main.ask_whole_playlist(url, ask=_answers(answer)) is expected


def test_main_reports_success(monkeypatch, capsys):
    calls = []
    monkeypatch.setattr(main, "mp3_downloader",
                        lambda url, whole_playlist: calls.append((url, whole_playlist))
                        or DownloadReport(succeeded=["x"]))
    monkeypatch.setattr("builtins.input", _answers("mp3", "https://youtu.be/a"))

    assert main.main() == 0
    assert calls == [("https://youtu.be/a", False)]
    assert "erfolgreich" in capsys.readouterr().out


def test_main_reports_failure_honestly(monkeypatch, capsys):
    monkeypatch.setattr(main, "vid_download",
                        lambda url, whole_playlist: DownloadReport(failed=["01 - Kaputt"]))
    monkeypatch.setattr("builtins.input", _answers("video", "https://youtu.be/a"))

    assert main.main() == 1
    out = capsys.readouterr().out
    assert "erfolgreich" not in out
    assert "01 - Kaputt" in out


def test_main_rejects_unknown_format(monkeypatch):
    monkeypatch.setattr("builtins.input", _answers("wav"))
    assert main.main() == 1
