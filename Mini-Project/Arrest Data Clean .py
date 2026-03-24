import pandas as pd
import os

# ----------------------------
# 1. Load the Excel file
# ----------------------------
df = pd.read_excel('/Users/phuong/Desktop/Mini-Project/Arrests.xlsx')

# ----------------------------
# 2. Keep only selected columns
# ----------------------------
columns_to_keep = [
    "Apprehension Date",
    "Apprehension State",
    "Apprehension AOR",
    "Apprehension Criminality",
    "Final Order Yes No",
    "Citizenship Country",
    "Gender"
]

df_edited = df[columns_to_keep]

# ----------------------------
# 3. Save new Excel file in the same folder as the original
# ----------------------------
folder = os.path.dirname('/Users/phuong/Desktop/Mini-Project/Arrests.xlsx')
output_path = os.path.join(folder, "Arrests_Edited.xlsx")
df_edited.to_excel(output_path, index=False)

print("File saved successfully as: Arrests_Edited.xlsx")



# --------------------------------------------------------
# Drop Missing Data Not Recovered
# --------------------------------------------------------
import pandas as pd

# Load your edited arrests file
df = pd.read_excel('/Users/phuong/Desktop/Mini-Project/Arrests_Edited.xlsx')

# ----------------------------
# 1. Remove rows where BOTH 'Apprehension State' and 'Apprehension AOR' are missing
# ----------------------------
df_cleaned = df.dropna(subset=['Apprehension State', 'Apprehension AOR'], how='all')

# ----------------------------
# 2. List unique 'Apprehension AOR' values where 'Apprehension State' is missing
# ----------------------------
missing_state_aors = df_cleaned.loc[df_cleaned['Apprehension State'].isna(), 'Apprehension AOR'].unique()

# ----------------------------
# Optional: save the cleaned file back
# ----------------------------
output_path = '/Users/phuong/Desktop/Mini-Project/Arrests_Edited_Cleaned.xlsx'
df_cleaned.to_excel(output_path, index=False)

# ----------------------------
# Print the results
# ----------------------------
print(f"Cleaned file saved as: {output_path}")
print("Unique 'Apprehension AOR' missing 'Apprehension State':")
print(missing_state_aors)

# --------------------------------------------------------
# Fill In The Missing Data
# --------------------------------------------------------


import pandas as pd

# Load the cleaned arrests file
df = pd.read_excel('/Users/phuong/Desktop/Mini-Project/Arrests_Edited_Cleaned.xlsx')

# ----------------------------
# 1. Define the mapping dictionary
# ----------------------------
aor_to_state = {
    'Atlanta Area of Responsibility': 'GEORGIA',
    'San Francisco Area of Responsibility': 'CALIFORNIA',
    'El Paso Area of Responsibility': 'TEXAS',
    'Salt Lake City Area of Responsibility': 'UTAH',
    'Phoenix Area of Responsibility': 'ARIZONA',
    'Houston Area of Responsibility': 'TEXAS',
    'Baltimore Area of Responsibility': 'MARYLAND',
    'Philadelphia Area of Responsibility': 'PENNSYLVANIA',
    'Dallas Area of Responsibility': 'TEXAS',
    'Newark Area of Responsibility': 'NEW JERSEY',
    'Miami Area of Responsibility': 'FLORIDA',
    'Boston Area of Responsibility': 'MASSACHUSETTS',
    'Harlingen Area of Responsibility': 'TEXAS',
    'Los Angeles Area of Responsibility': 'CALIFORNIA',
    'Detroit Area of Responsibility': 'MICHIGAN',
    'Denver Area of Responsibility': 'COLORADO',
    'Chicago Area of Responsibility': 'ILLINOIS',
    'St. Paul Area of Responsibility': 'MINNESOTA',
    'Seattle Area of Responsibility': 'WASHINGTON',
    'New Orleans Area of Responsibility': 'LOUISIANA',
    'Washington Area of Responsibility': 'DISTRICT OF COLUMBIA',
    'San Diego Area of Responsibility': 'CALIFORNIA',
    'San Antonio Area of Responsibility': 'TEXAS',
    'New York City Area of Responsibility': 'NEW YORK',
    'HQ Area of Responsibility': 'VIRGINIA',
    'Buffalo Area of Responsibility': 'NEW YORK'
}

# ----------------------------
# 2. Fill missing 'Apprehension State' values using the dictionary
# ----------------------------
df['Apprehension State'] = df.apply(
    lambda row: aor_to_state[row['Apprehension AOR']] if pd.isna(row['Apprehension State']) else row['Apprehension State'],
    axis=1
)

# ----------------------------
# 3. Save the updated file
# ----------------------------
output_path = '/Users/phuong/Desktop/Mini-Project/Arrests_Edited_Filled.xlsx'
df.to_excel(output_path, index=False)

print("Missing 'Apprehension State' values filled and file saved as:", output_path)

# --------------------------------------------------------
# Fill In The Year
# --------------------------------------------------------

import pandas as pd

# Load the filled arrests file
df = pd.read_excel('/Users/phuong/Desktop/Mini-Project/Arrests_Edited_Filled.xlsx')

# Ensure 'Apprehension Date' is datetime
df['Apprehension Date'] = pd.to_datetime(df['Apprehension Date'], errors='coerce')

# Create 'Apprehension Year'
df['Apprehension Year'] = df['Apprehension Date'].dt.year

# Reorder columns: move 'Apprehension Year' right after 'Apprehension Date'
cols = df.columns.tolist()
date_idx = cols.index('Apprehension Date')
# Remove 'Apprehension Year' from current position
cols.remove('Apprehension Year')
# Insert it right after 'Apprehension Date'
cols.insert(date_idx + 1, 'Apprehension Year')
df = df[cols]

# Save the updated file
output_path = '/Users/phuong/Desktop/Mini-Project/Arrests_Edited_With_Year.xlsx'
df.to_excel(output_path, index=False)

print("New column 'Apprehension Year' added after 'Apprehension Date' and file saved as:", output_path)





import pandas as pd

# Load file
df = pd.read_excel('/Users/phuong/Desktop/Mini-Project/Arrests_Edited_With_Year.xlsx')

# Ensure date column is datetime
df['Apprehension Date'] = pd.to_datetime(df['Apprehension Date'], errors='coerce')

# Extract year and month (if not already present)
df['Year'] = df['Apprehension Date'].dt.year
df['Month'] = df['Apprehension Date'].dt.month

# Filter Jan–Oct (months 1–10)
jan_oct = df[df['Month'].between(1, 10)]

# Count arrests for each year
arrests_2024 = jan_oct[jan_oct['Year'] == 2024].shape[0]
arrests_2025 = jan_oct[jan_oct['Year'] == 2025].shape[0]

print("Total arrests Jan–Oct 2024:", arrests_2024)
print("Total arrests Jan–Oct 2025:", arrests_2025)












