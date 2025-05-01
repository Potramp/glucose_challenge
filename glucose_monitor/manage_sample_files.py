import pandas as pd
from pathlib import Path
from glucose_monitor.database import DB_ENGINE, create_db_and_tables

ROOT_DIR = Path(__file__).parent.parent


def get_filenames() -> list:
    """List sample files."""
    sample_path = ROOT_DIR / "sample_files"
    filenames = sample_path.glob("*.csv")
    return [filepath for filepath in filenames if filepath.is_file()]


def read_sample_files_to_df(filenames: list) -> pd.DataFrame:
    df = pd.DataFrame()
    for file in filenames:
        sample_df = pd.read_csv(file, skiprows=1)
        df = pd.concat([df, sample_df])
    return df


if __name__ == "__main__":
    create_db_and_tables()
    filenames = get_filenames()
    df = read_sample_files_to_df(filenames)
    df = df.drop(list(df)[6:], axis=1)
    df.columns = [
        "device",
        "device_id",
        "device_timestamp",
        "recording_type",
        "glucose_value_history",
        "glucose_scan",
    ]
    df.to_sql(name="glucose_levels", con=DB_ENGINE, if_exists="append", index=False)
