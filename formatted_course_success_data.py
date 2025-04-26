import os
import pandas as pd

# File paths
csv_path = r"C:\Users\Slain\OneDrive\Desktop\Thesis WebScrape\Success Metrics\CourseRetSuccessSumm.csv"
output_path = r"C:\Users\Slain\OneDrive\Desktop\Thesis WebScrape\Success Metrics\Formatted_Course_Success_Data.csv"

# Load CSV and clean columns
df = pd.read_csv(csv_path, skiprows=2)
df.columns = df.columns.str.strip()

# Define target academic years
target_years = ["2020-2021", "2021-2022", "2022-2023", "2023-2024"]

# Define suffix-to-category mapping
category_map = {
    "": "Credit Enrollment Count",
    ".1": "Credit Retention Count",
    ".2": "Credit Success Count",
    ".5": "Degree Applicable Enrollment Count",
    ".6": "Degree Applicable Retention Count",
    ".7": "Degree Applicable Success Count",
    ".10": "Transferable Enrollment Count",
    ".11": "Transferable Retention Count",
    ".12": "Transferable Success Count"
}

# Create long-form table
records = []

for _, row in df.iterrows():
    college_raw = row.get("Unnamed: 0")
    if not isinstance(college_raw, str):
        continue
    college = college_raw.replace(" Total", "").strip()
    for col in df.columns:
        if any(term in col for term in ["Fall", "Spring", "Summer", "Winter"]):
            term_parts = col.split(".")
            base_term = term_parts[0].strip()
            suffix = f".{term_parts[1]}" if len(term_parts) > 1 else ""
            category = category_map.get(suffix, None)

            if category:
                value = row[col]
                try:
                    if pd.isna(value) or value == "null" or str(value).strip() == "":
                        value = None
                    else:
                        value = float(str(value).replace(",", "").strip())
                except:
                    value = None

                # Map to academic year
                if " " in base_term:
                    season, year = base_term.split()
                    year = int(year)
                    if season == "Fall":
                        academic_year = f"{year}-{year + 1}"
                    else:
                        academic_year = f"{year - 1}-{year}"
                else:
                    continue

                if academic_year in target_years:
                    records.append({
                        "College": college,
                        "Year": academic_year,
                        "Category": category,
                        "Value": value
                    })

# Convert to DataFrame
long_df = pd.DataFrame(records)

# Pivot to wide format
pivot_df = long_df.pivot_table(
    index=["College", "Year"],
    columns="Category",
    values="Value",
    aggfunc="sum"
).reset_index()

# Calculate derived percentages
def safe_rate(numerator, denominator):
    if pd.isna(numerator) or pd.isna(denominator) or denominator == 0:
        return "0.00%"
    return f"{round((numerator / denominator) * 100, 2):.2f}%"

pivot_df["Credit Retention Rate (%)"] = pivot_df.apply(
    lambda row: safe_rate(row.get("Credit Retention Count"), row.get("Credit Enrollment Count")), axis=1)

pivot_df["Credit Success Rate (%)"] = pivot_df.apply(
    lambda row: safe_rate(row.get("Credit Success Count"), row.get("Credit Enrollment Count")), axis=1)

pivot_df["Degree Applicable Retention Rate (%)"] = pivot_df.apply(
    lambda row: safe_rate(row.get("Degree Applicable Retention Count"), row.get("Degree Applicable Enrollment Count")), axis=1)

pivot_df["Degree Applicable Success Rate (%)"] = pivot_df.apply(
    lambda row: safe_rate(row.get("Degree Applicable Success Count"), row.get("Degree Applicable Enrollment Count")), axis=1)

pivot_df["Transferable Retention Rate (%)"] = pivot_df.apply(
    lambda row: safe_rate(row.get("Transferable Retention Count"), row.get("Transferable Enrollment Count")), axis=1)

pivot_df["Transferable Success Rate (%)"] = pivot_df.apply(
    lambda row: safe_rate(row.get("Transferable Success Count"), row.get("Transferable Enrollment Count")), axis=1)

# Save final CSV
pivot_df.to_csv(output_path, index=False)
print(f"✅ Saved cleaned course success data to: {output_path}")
