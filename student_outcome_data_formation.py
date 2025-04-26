import pandas as pd

# --- Load Raw Course Success Files ---
outcomes_14_20 = pd.read_csv("Course_Success_Data_2014_2020.csv")
outcomes_20_24 = pd.read_csv("Course_Success_Data_2020_2024.csv")

# --- Define Cleaner Function ---
def clean_outcomes(df):
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["Unnamed: 0"])  # Remove empty college rows
    df = df[~df["Unnamed: 0"].str.contains("Total", na=False)]  # Skip totals
    df = df[~df["Unnamed: 0"].str.contains("College Name", na=False)]

    category_map = {
        "": "Credit Enrollment Count",
        ".2": "Credit Success Count",
        ".5": "Degree Applicable Enrollment Count",
        ".7": "Degree Applicable Success Count",
        ".10": "Transferable Enrollment Count",
        ".12": "Transferable Success Count"
    }

    records = []

    for _, row in df.iterrows():
        college = row["Unnamed: 0"].replace(" Total", "").strip()
        for col in df.columns:
            if any(term in col for term in ["Fall", "Winter", "Spring"]):  # Only these terms
                term_parts = col.split(".")
                base_term = term_parts[0].strip()
                suffix = f".{term_parts[1]}" if len(term_parts) > 1 else ""

                if suffix not in category_map:
                    continue  # Ignore irrelevant columns

                season, year = base_term.split()
                year = int(year)

                # Assign to proper Academic Year
                if season == "Fall":
                    academic_year = f"{year}-{year+1}"
                else:  # Winter and Spring belong to Fall of previous year
                    academic_year = f"{year-1}-{year}"

                value = row[col]
                try:
                    value = float(str(value).replace(",", "").strip())
                except:
                    value = None

                records.append({
                    "College": college,
                    "Year": academic_year,
                    "Category": category_map[suffix],
                    "Value": value
                })

    long_df = pd.DataFrame(records)

    pivot_df = long_df.pivot_table(
        index=["College", "Year"],
        columns="Category",
        values="Value",
        aggfunc="sum"
    ).reset_index()

    return pivot_df

# --- Clean Each Dataset Separately ---
cleaned_outcomes_14_20 = clean_outcomes(outcomes_14_20)
cleaned_outcomes_20_24 = clean_outcomes(outcomes_20_24)

# --- Save Cleaned Versions ---
cleaned_outcomes_14_20.to_csv("Cleaned_Course_Success_2014_2020.csv", index=False)
cleaned_outcomes_20_24.to_csv("Cleaned_Course_Success_2020_2024.csv", index=False)

# --- Combine into One Full Dataset ---
combined_outcomes = pd.concat([cleaned_outcomes_14_20, cleaned_outcomes_20_24], ignore_index=True)
combined_outcomes = combined_outcomes.sort_values(["College", "Year"])

combined_outcomes.to_csv("Combined_Course_Success_Data_2014_2024.csv", index=False)

print("✅ Student Outcome Data Cleaning and Combining Complete (Correct Terms Only)")
