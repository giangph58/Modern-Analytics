import os
import pandas as pd


def get_data_dir():
    """Get the absolute path to the data directory."""
    if os.environ.get("HEALTH_APP_DATA_DIR"):
        return os.environ.get("HEALTH_APP_DATA_DIR")
    return os.path.join(os.path.dirname(__file__), "data")


def get_data_path(filename):
    """Get absolute path to a data file."""
    return os.path.join(get_data_dir(), filename)


def load_fund_data():
    """Load topic data from CSV file"""
    # Path to the real data file
    data_path = get_data_path("FundsGDPhealth_export.csv")

    # Read the CSV file
    fund_df = pd.read_csv(data_path)
    fund_df["country_name"] = fund_df["TIME"]
    fund_df["GDPM2124"] = fund_df[["GDP2021", "GDP2022", "GDP2023", "GDP2024"]].mean(axis=1)

    fund_df["HLYM2122"] = fund_df[["HLY2021", "HLY2022"]].mean(axis=1)
    return fund_df


plot_data = load_fund_data()

def load_topic_data():
    """Load topic data from CSV file"""
    # Path to the real data file
    data_path = get_data_path("topic_df.csv")

    # Read the CSV file
    topic_df = pd.read_csv(data_path)
    return topic_df


topic_data = load_topic_data()


def load_orgs_data():
    data_path = get_data_path("health_orgs.csv")
    orgs_df = pd.read_csv(data_path)
    return orgs_df

orgs_data = load_orgs_data()


def load_orgs_pub_data():
    data_path = get_data_path("health_orgs_pub.csv")
    orgs_df = pd.read_csv(data_path)
    return orgs_df

orgs_pub_data = load_orgs_pub_data()
