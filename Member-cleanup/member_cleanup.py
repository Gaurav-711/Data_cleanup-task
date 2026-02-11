

#Original file is located at https://colab.research.google.com/drive/19vreE5wow4HJeiS04kHu9eZjADtHJhOd


import pandas as pd
import re
from datetime import datetime, timedelta
from dateutil import parser

#fixing excel csv mixture

df_raw = pd.read_excel("signup.xls", engine="xlrd")

rows = []

for row in df_raw.iloc[:, 0].astype(str):
    parts = row.split(",")

    # Identify email position
    email_index = None
    for i, part in enumerate(parts):
        if "@" in part:
            email_index = i
            break

    if email_index is None:
        continue

    name = ",".join(parts[:email_index]).strip()
    email = parts[email_index].strip()
    signup_date = parts[email_index + 1].strip()
    plan = parts[email_index + 2].strip()
    notes = ",".join(parts[email_index + 3:]).strip()

    rows.append([name, email, signup_date, plan, notes])

df = pd.DataFrame(rows, columns=["name", "email", "signup_date", "plan", "notes"])

#cleaning function

def clean_name(name):
    if pd.isna(name):
        return None

    name = name.replace("4", "a").strip()

    # Convert "Last, First" → "First Last"
    if "," in name:
        parts = name.split(",")
        if len(parts) == 2:
            name = parts[1].strip() + " " + parts[0].strip()

    name = name.replace(",", "")
    return name.title()


def clean_email(email):
    if pd.isna(email):
        return None

    email = email.strip().lower()

    # Gmail normalization
    if "gmail.com" in email:
        local, domain = email.split("@")
        local = local.split("+")[0]
        local = local.replace(".", "")
        email = local + "@" + domain

    return email


def parse_date(date_value):
    if pd.isna(date_value):
        return None

    if str(date_value).lower() == "yesterday":
        return (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        parsed = parser.parse(str(date_value))
        return parsed.strftime("%Y-%m-%d")
    except:
        return None


#cleaning

df["name"] = df["name"].apply(clean_name)
df["email"] = df["email"].apply(clean_email)
df["signup_date"] = df["signup_date"].apply(parse_date)


#Identify Unnecessary Leads
def extra(row):
    name = str(row["name"]).lower()
    email = str(row["email"]).lower()
    notes = str(row["notes"]).lower()

    allowed_domains = ["gmail.com", "yahoo.com", "outlook.com"]

    domain_valid = any(email.endswith(d) for d in allowed_domains)

    if (
        "test" in name
        or "test" in email
        or "ignore" in notes
        or not re.match(r"[^@]+@[^@]+\.[^@]+", email)
        or not domain_valid
        or pd.isna(row["signup_date"])
    ):
        return True

    return False


df["Extra"] = df.apply(extra, axis=1)

quarantine_df = df[df["Extra"]].copy()
clean_df = df[~df["Extra"]].copy()


clean_df["signup_date"] = pd.to_datetime(clean_df["signup_date"])
clean_df = clean_df.sort_values(by="signup_date", ascending=False)

#unique palns
plan_counts = (
    clean_df.groupby("name")["plan"]
    .nunique()
    .reset_index()
)

plan_counts["is_multi_plan"] = plan_counts["plan"] > 1
plan_counts = plan_counts[["name", "is_multi_plan"]]

# Keep latest signup per person
clean_df = clean_df.drop_duplicates(subset=["name"], keep="first")
clean_df = clean_df.merge(plan_counts, on="name", how="left")
clean_df["is_multi_plan"] = clean_df["is_multi_plan"].fillna(False)

#save files
clean_df.to_csv("members_final.csv", index=False)
quarantine_df.to_csv("Extra.csv", index=False)

print("Cleanup complete.")
print("Generated: members_final.csv and quarantine.csv")