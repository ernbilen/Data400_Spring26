import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import warnings
warnings.filterwarnings("ignore")

# ── FILE PATHS ────────────────────────────────────────────────────────────────
file_paths = [
    "/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2014_final.parquet",
    "/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2015_final.parquet",
    "/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2016_final.parquet",
    "/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2017_final.parquet",
    "/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2018_final.parquet",
    "/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2019_final.parquet",
    "/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2020_final.parquet",
    "/Users/phuong/Library/Mobile Documents/com~apple~CloudDocs/ICE/Final/Cleaned_OPT_2021_final.parquet",
]

FEATURES_RAW = [
    "tuition_and_fees",
    "students_personal_funds",
    "funds_from_this_school",
    "funds_from_other_sources",
    "on-campus_employment",
    "unemployment_days",
    "use_stem_opt",
]

# Dollar variables to rescale to $1,000 units for interpretable AME
DOLLAR_COLS = [
    "tuition_and_fees",
    "students_personal_funds",
    "funds_from_this_school",
    "funds_from_other_sources",
    "on-campus_employment",
]

TARGET = "any_postgrad"

# Clean display names for the plot
DISPLAY_NAMES = {
    "tuition_and_fees":        "Tuition & Fees ($1K)",
    "students_personal_funds": "Personal Funds ($1K)",
    "funds_from_this_school":  "School-Provided Funds ($1K)",
    "funds_from_other_sources":"Other Funding Sources ($1K)",
    "on-campus_employment":    "On-Campus Employment ($1K)",
    "unemployment_days":       "Unemployment Days",
    "use_stem_opt":            "Used STEM OPT (0/1)",
}

# ── LOAD & CLEAN ──────────────────────────────────────────────────────────────
cols_needed = FEATURES_RAW + [TARGET]

df = pd.concat(
    [pq.read_table(p, columns=cols_needed).to_pandas() for p in file_paths],
    ignore_index=True
).dropna(subset=cols_needed)

df[TARGET] = df[TARGET].astype(int)

# Rescale dollar columns to thousands
for col in DOLLAR_COLS:
    df[col] = df[col] / 1000.0

print(f"Rows: {len(df):,}")
print(f"Outcome rate: {df[TARGET].mean():.3f}  ({df[TARGET].sum():,} post-grad / {len(df):,} total)\n")

# ── TRAIN / TEST SPLIT ────────────────────────────────────────────────────────
X = df[FEATURES_RAW]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

scaler     = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ── FIT LOGIT — class_weight='balanced' fixes the imbalance problem ───────────
logit = LogisticRegression(
    max_iter=1000, solver="lbfgs",
    class_weight="balanced",          # ← KEY FIX
    random_state=42
)
logit.fit(X_train_sc, y_train)

y_pred      = logit.predict(X_test_sc)
y_pred_prob = logit.predict_proba(X_test_sc)[:, 1]

print("── Test Set Performance ───────────────────────────────")
print(classification_report(y_test, y_pred, target_names=["No Postgrad", "Postgrad"]))
print(f"ROC-AUC : {roc_auc_score(y_test, y_pred_prob):.4f}\n")

# ── AVERAGE MARGINAL EFFECTS ──────────────────────────────────────────────────
coefs_orig = logit.coef_[0] / scaler.scale_
p_hat      = logit.predict_proba(scaler.transform(X))[:, 1]
ame        = coefs_orig * (p_hat * (1 - p_hat)).mean()

# ── BOOTSTRAP 95% CI ──────────────────────────────────────────────────────────
np.random.seed(42)
boot_ames = np.zeros((500, len(FEATURES_RAW)))
X_arr, y_arr = X.values, y.values

for b in range(500):
    idx      = np.random.choice(len(X_arr), len(X_arr), replace=True)
    sc_b     = StandardScaler().fit(X_arr[idx])
    Xb_sc    = sc_b.transform(X_arr[idx])
    m        = LogisticRegression(
        max_iter=500, solver="lbfgs", class_weight="balanced"
    ).fit(Xb_sc, y_arr[idx])
    c_orig_b    = m.coef_[0] / sc_b.scale_
    p_b         = m.predict_proba(Xb_sc)[:, 1]
    boot_ames[b] = c_orig_b * (p_b * (1 - p_b)).mean()

ci_lo = np.percentile(boot_ames, 2.5,  axis=0)
ci_hi = np.percentile(boot_ames, 97.5, axis=0)

# ── RESULTS TABLE ─────────────────────────────────────────────────────────────
results = pd.DataFrame({
    "feature":      FEATURES_RAW,
    "display_name": [DISPLAY_NAMES[f] for f in FEATURES_RAW],
    "AME":          ame,
    "ci_lo":        ci_lo,
    "ci_hi":        ci_hi,
}).sort_values("AME", ascending=False).reset_index(drop=True)

# Convert to percentage points for display
results["AME_pp"]   = results["AME"]   * 100
results["ci_lo_pp"] = results["ci_lo"] * 100
results["ci_hi_pp"] = results["ci_hi"] * 100

print("── Average Marginal Effects (dy/dx) ──────────────────────────────────")
print("  1-unit ↑ in X  →  AME percentage-point change in P(post-grad)\n")
print(f"  {'Variable':<30} {'AME (pp)':>10}   95% CI (pp)           Significant?")
print("  " + "─" * 72)
for _, row in results.iterrows():
    sig = "Yes *" if not (row.ci_lo < 0 < row.ci_hi) else "No"
    print(f"  {row.display_name:<30} {row.AME_pp:>+8.2f}pp"
          f"   [{row.ci_lo_pp:+.2f}, {row.ci_hi_pp:+.2f}]   {sig}")

# ── SLIDE-READY PLOT ──────────────────────────────────────────────────────────
plot_df = results.sort_values("AME_pp", ascending=True).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor("white")

colors = ["#c0392b" if v > 0 else "#2471a3" for v in plot_df["AME_pp"]]

bars = ax.barh(
    plot_df["display_name"], plot_df["AME_pp"],
    color=colors, alpha=0.88, height=0.55, zorder=3
)

err_lo = (plot_df["AME_pp"] - plot_df["ci_lo_pp"]).abs()
err_hi = (plot_df["ci_hi_pp"] - plot_df["AME_pp"]).abs()

ax.errorbar(
    plot_df["AME_pp"], plot_df["display_name"],
    xerr=[err_lo, err_hi],
    fmt="none", color="#222222", capsize=5, linewidth=1.4, zorder=4
)

ax.axvline(0, color="black", linewidth=1.1, linestyle="--", zorder=2)

# Value labels on each bar
for _, row in plot_df.iterrows():
    val   = row["AME_pp"]
    pad   = 0.15 if val >= 0 else -0.15
    ha    = "left" if val >= 0 else "right"
    label = f"{val:+.2f} pp"
    ax.text(val + pad, row["display_name"], label,
            va="center", ha=ha, fontsize=10, fontweight="bold", color="#111111")

# Significance stars on the y-axis labels
ytick_labels = []
for _, row in plot_df.iterrows():
    sig = "" if (row["ci_lo"] < 0 < row["ci_hi"]) else "  ✦"
    ytick_labels.append(row["display_name"] + sig)
ax.set_yticklabels(ytick_labels, fontsize=11)

ax.set_xlabel("Change in probability of post-grad outcome (percentage points)",
              fontsize=11, labelpad=10)
ax.set_title("Average Marginal Effects — Logit Model\n"
             "Outcome: Any Post-Graduation Activity",
             fontsize=14, fontweight="bold", pad=15)


# Footnote
fig.text(0.01, -0.04,
         "✦ Statistically meaningful (95% bootstrap CI does not cross zero).\n"
         "Dollar variables rescaled to $1,000 units. Model uses balanced class weights to correct for 93/7 outcome imbalance.",
         fontsize=8.5, color="#555555", va="top")

ax.set_facecolor("#f7f9fc")
ax.grid(axis="x", linestyle=":", alpha=0.5, zorder=1)
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
plt.savefig("ame_slide.png", dpi=180, bbox_inches="tight")
plt.show()
print("\nSaved: ame_slide.png")