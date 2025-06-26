import pandas as pd
from pathlib import Path

# stores sleep history data
DATA_FILE = Path(__file__).parent.parent / "sleep_data.csv"

def load_data() -> pd.DataFrame:
    """
    Loads the sleep data CSV into a DataFrame.
    If the file doesn't exist yet, we should return empty DataFrame
    with columns: date, alarm_time, wakeup_time, snoozes.
    """
    # desired schema
    cols = ["date", "alarm_time", "wakeup_time", "snoozes"]

    if not DATA_FILE.exists():
        return pd.DataFrame(columns=cols)
    
    # read the csv; parsing 'date' columnn as datetime
    df = pd.read_csv(
        DATA_FILE,
        parse_dates=["date"],
        usecols=cols,           # gaurds against extra columns
    )

    return df


def save_entry(entry: dict) ->  None:
    """
    Append a single entry (with keys, date, alarm_time, wakeup_time, snoozes)
    into CSV. Create file if doesn't exist.
    """
    # load existing data or empty DataFrame
    df = load_data()

    # build a one row DataFrame from dict ensure we use only expected cols
    cols = ["date", "alarm_time", "wakeup_time", "snoozes"]
    row = {k: entry[k] for k in cols}
    new_df = pd.DataFrame([row])

    # concatenate and write back out
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)