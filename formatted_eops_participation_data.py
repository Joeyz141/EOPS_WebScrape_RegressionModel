import pandas as pd

# Path to the new CSV file
csv_file = r"C:\Users\Slain\OneDrive\Desktop\Thesis WebScrape\EOPS\EOPSSumm_2014_2020.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Define the target years
years = [f"Annual {year}-{year+1}" for year in range(2020, 2024)]

# Prepare structured list
records = []

# Get unique colleges
colleges = df["Unnamed: 0"].dropna().unique()

# Iterate through each college
for college in colleges:
    if not isinstance(college, str) or not college.strip() or "Total" in college or college == "College Name":
        continue  # Skip invalid or total rows

    # Clean up college name
    college = college.replace(" Total", "").strip()

    # Filter rows for the current college
    college_rows = df[df["Unnamed: 0"] == college]

    # Iterate through all years for the current college
    for year in years:
        try:
            # Dynamically check if the column exists
            student_count_col = year
            eops_student_count_col = year

            # Ensure the column exists
            if student_count_col in df.columns and eops_student_count_col in df.columns:
                # Extract the correct rows for Total and EOPS
                eops_row = college_rows[college_rows["Unnamed: 1"] == "EOPS participant"]
                total_row = college_rows[college_rows["Unnamed: 1"] == "Not an EOPS/CARE participant"]

                # Extract and clean data
                student_count = (
                    int(str(total_row[student_count_col].values[0]).replace(",", "").strip())
                    if not total_row.empty else 0
                )
                eops_student_count = (
                    int(str(eops_row[eops_student_count_col].values[0]).replace(",", "").strip())
                    if not eops_row.empty else 0
                )
            else:
                # If the year column is missing, default to 0
                student_count = 0
                eops_student_count = 0

            # Validate and fix data
            if eops_student_count > student_count:
                # Swap values if misaligned
                student_count, eops_student_count = eops_student_count, student_count

            # Recalculate EOPS Participation to ensure accuracy
            calculated_participation = (eops_student_count / student_count) * 100 if student_count > 0 else 0
            eops_participation = f"{calculated_participation:.2f}%" if student_count > 0 else "0.00%"

            # Append the record
            records.append({
                "College": college,
                "Year": year.replace("Annual ", ""),
                "Student Count": student_count,
                "EOPS Student Count": eops_student_count,
                "EOPS Participation": eops_participation
            })
        except Exception as e:
            # Log the error for debugging
            print(f"Error processing {college} for {year}: {e}")
            records.append({
                "College": college,
                "Year": year.replace("Annual ", ""),
                "Student Count": 0,
                "EOPS Student Count": 0,
                "EOPS Participation": "0.00%"
            })

# Create final DataFrame
formatted_df = pd.DataFrame(records)

# Debug: Check for suspicious values
suspicious_colleges = formatted_df[formatted_df["Student Count"] == 0]
print("Suspicious Colleges with 0 Student Count:")
print(suspicious_colleges)

# Sort by College and Year
formatted_df = formatted_df.sort_values(by=["College", "Year"])

# Save to CSV
final_output_path = r"C:\Users\Slain\OneDrive\Desktop\Thesis WebScrape\EOPS\Formatted_EOPS_Participation_Data_2014_to_2020.csv"
formatted_df.to_csv(final_output_path, index=False)

# Display the DataFrame (optional, remove if not needed)
print("Formatted EOPS Participation Data:")
print(formatted_df)