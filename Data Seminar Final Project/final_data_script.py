import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# LIST OF PARQUET FILE PATHS
# ============================================

file_paths = [
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2014_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2015_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2016_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2017_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2018_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2019_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2020_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2021_final.parquet"
]

# ============================================
# READ AND COMBINE ALL FILES
# ============================================

df_list = []

for path in file_paths:
    print(f"Reading: {path}")
    
    temp_df = pd.read_parquet(
        path,
        columns=["student_edu_level_desc", "major1_title"]
    )
    
    df_list.append(temp_df)

# Combine all datasets
df = pd.concat(df_list, ignore_index=True)

print("Combined Shape:", df.shape)

# ============================================
# CLEAN DATA
# ============================================

df = df.dropna(subset=["student_edu_level_desc", "major1_title"])

df["student_edu_level_desc"] = df["student_edu_level_desc"].str.upper()
df["major1_title"] = df["major1_title"].str.upper()

# ============================================
# FUNCTION TO PLOT TOP 10 MAJORS
# ============================================

def plot_top_majors(level_keyword, graph_title):

    filtered_df = df[
        df["student_edu_level_desc"].str.contains(level_keyword, na=False)
    ]

    top_majors = (
        filtered_df["major1_title"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(top_majors.index, top_majors.values)

    # Add data labels
    for bar in bars:
        width = bar.get_width()
        
        ax.text(
            width + 5,                         # x position
            bar.get_y() + bar.get_height()/2, # y position
            f"{int(width):,}",                # label text
            va='center',
            fontsize=10
        )

    ax.set_title(f"Top 10 Majors for {graph_title}", fontsize=16)
    ax.set_xlabel("Number of Students", fontsize=12)
    ax.set_ylabel("Major", fontsize=12)

    plt.tight_layout()
    plt.show()

# ============================================
# GENERATE ALL 3 GRAPHS
# ============================================

plot_top_majors("BACHELOR", "Bachelor's")
plot_top_majors("MASTER", "Master's")
plot_top_majors("DOCTORATE", "PhD")










import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# FILE PATHS
# ============================================

file_paths = [
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2014_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2015_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2016_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2017_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2018_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2019_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2020_final.parquet",
    r"/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2021_final.parquet"
]

# ============================================
# READ ALL FILES
# ============================================

all_data = []

for path in file_paths:
    print(f"Reading: {path}")
    
    year = int(path.split("Cleaned_OPT_")[1].split("_final")[0])
    
    temp_df = pd.read_parquet(
        path,
        columns=["student_edu_level_desc", "major1_title"]
    )
    
    temp_df["year"] = year
    all_data.append(temp_df)

df = pd.concat(all_data, ignore_index=True)

print("Combined Shape:", df.shape)

# ============================================
# CLEAN DATA
# ============================================

df = df.dropna(subset=["student_edu_level_desc", "major1_title"])

df["student_edu_level_desc"] = (
    df["student_edu_level_desc"]
    .astype(str)
    .str.upper()
    .str.strip()
)

df["major1_title"] = (
    df["major1_title"]
    .astype(str)
    .str.upper()
    .str.strip()
)

# ============================================
# FUNCTION TO CREATE LINE GRAPH
# ============================================

def plot_major_trends(level_keyword, graph_title, top_n=5):
    
    filtered_df = df[
        df["student_edu_level_desc"].str.contains(level_keyword, na=False)
    ]
    
    print(f"{graph_title} rows:", filtered_df.shape[0])
    
    # Find top majors overall within this degree level
    top_majors = (
        filtered_df["major1_title"]
        .value_counts()
        .head(top_n)
        .index
    )
    
    filtered_df = filtered_df[
        filtered_df["major1_title"].isin(top_majors)
    ]
    
    # Count students by year and major
    trend_data = (
        filtered_df
        .groupby(["year", "major1_title"])
        .size()
        .reset_index(name="count")
    )
    
    # Pivot for line plotting
    pivot_df = (
        trend_data
        .pivot(index="year", columns="major1_title", values="count")
        .fillna(0)
        .sort_index()
    )
    
    # Sort legend by final year value, top to bottom
    sorted_columns = pivot_df.iloc[-1].sort_values(ascending=False).index
    
    # ============================================
    # PLOT
    # ============================================
    
    plt.figure(figsize=(13, 7))
    
    line_objects = []
    
    for major in sorted_columns:
        
        line, = plt.plot(
            pivot_df.index,
            pivot_df[major],
            marker="o",
            linewidth=2,
            label=major
        )
        
        line_objects.append(line)
        
        # Add data labels
        for x, y in zip(pivot_df.index, pivot_df[major]):
            plt.text(
                x,
                y,
                f"{int(y):,}",
                fontsize=7,
                ha="center",
                va="bottom"
            )
    
    plt.title(f"Top {top_n} Major Trends Over Time — {graph_title}", fontsize=16)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Number of Students", fontsize=12)
    
    plt.xticks(sorted(df["year"].unique()))
    plt.grid(True, linestyle="--", alpha=0.4)
    
    # Smaller legend, ordered by line height in the final year
    plt.legend(
        handles=line_objects,
        fontsize=8,
        title="Major",
        title_fontsize=9,
        loc="center left",
        bbox_to_anchor=(1.01, 0.5),
        frameon=False
    )
    
    plt.tight_layout()
    plt.show()

# ============================================
# GENERATE LINE CHARTS
# ============================================

plot_major_trends("BACHELOR", "Bachelor's", top_n=5)
plot_major_trends("MASTER", "Master's", top_n=5)
plot_major_trends("DOCTORATE", "PhD", top_n=5)