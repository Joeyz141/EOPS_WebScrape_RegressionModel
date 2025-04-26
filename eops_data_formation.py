import pandas as pd

# --- Load Raw EOPS Files ---
eops_14_20 = pd.read_csv("EOPS_2014_to_2020.csv")
eops_20_24 = pd.read_csv("EOPS_2020_to_2024.csv")

# --- Define Cleaner Function ---
def clean_eops(df):
    records = []
    colleges = df["Unnamed: 0"].dropna().unique()
    years = [col for col in df.columns if "Annual" in col]

    for college in colleges:
        if not isinstance(college, str) or "Total" in college or "College Name" in college:
            continue
        college_name = college.replace(" Total", "").strip()
        college_rows = df[df["Unnamed: 0"] == college]

        for year_col in years:
            try:
                # Get values for each status
                eops_and_care_row = college_rows[college_rows["Unnamed: 1"] == "EOPS and CARE participant"]
                eops_row = college_rows[college_rows["Unnamed: 1"] == "EOPS participant"]
                non_eops_row = college_rows[college_rows["Unnamed: 1"] == "Not an EOPS/CARE participant"]

                eops_and_care = int(str(eops_and_care_row[year_col].values[0]).replace(",", "").strip()) if not eops_and_care_row.empty else 0
                eops_only = int(str(eops_row[year_col].values[0]).replace(",", "").strip()) if not eops_row.empty else 0
                non_eops = int(str(non_eops_row[year_col].values[0]).replace(",", "").strip()) if not non_eops_row.empty else 0

                # Calculate correct totals
                student_count = eops_and_care + eops_only + non_eops
                eops_student_count = eops_only

                records.append({
                    "College": college_name,
                    "Year": year_col.replace("Annual ", ""),
                    "Student Count": student_count,
                    "EOPS Student Count": eops_student_count
                })

            except Exception as e:
                print(f"⚠️ Error processing {college_name} for {year_col}: {e}")

    return pd.DataFrame(records)

# --- Clean Each Dataset Separately ---
cleaned_eops_14_20 = clean_eops(eops_14_20)
cleaned_eops_20_24 = clean_eops(eops_20_24)

# --- Save Cleaned Individual Files ---
cleaned_eops_14_20.to_csv("Cleaned_EOPS_2014_2020.csv", index=False)
cleaned_eops_20_24.to_csv("Cleaned_EOPS_2020_2024.csv", index=False)

# --- Combine into One Full Dataset ---
combined_eops = pd.concat([cleaned_eops_14_20, cleaned_eops_20_24], ignore_index=True)
combined_eops = combined_eops.sort_values(["College", "Year"])

combined_eops.to_csv("Combined_EOPS_Participation_Data_2014_2024.csv", index=False)

print("✅ EOPS Data Cleaning and Combining Complete (Student Count fixed properly)")
