import pandas as pd
import pytest
from pathlib import Path

from src.data import load_data, save_entry, DATA_FILE

@pytest.fixture(autouse=True)
def isolate_csv(tmp_path, monkeypatch):
    # redirect DATA_FILE to a temp file so we don't clobber real CSV
    fake = tmp_path / "sleep_data.csv"
    monkeypatch.setattr("src.data.DATA_FILE", fake)
    return fake

def test_load_empty(isolate_csv):
    df = load_data()
    assert df.empty
    assert list(df.columns) == ["date", "alarm_time", "wakeup_time", "snoozes"]

def test_save_and_load(isolate_csv):
    entry = {
        "date": "2025-06-25",
        "alarm_time": "07:00",
        "wakeup_time": "06:58",
        "snoozes": 0
    }
    save_entry(entry)
    df = load_data()
    # one row, matching our entry
    assert len(df) == 1
    row = df.iloc[0].to_dict()
    assert row["date"] == pd.to_datetime("2025-06-25")
    assert row["alarm_time"] == "07:00"
    assert row["wakeup_time"] == "06:58"
    assert row["snoozes"] == 0