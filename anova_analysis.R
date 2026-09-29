# ==============================================================================
# R PROGRAM: ONE-WAY ANOVA STATISTICAL FEATURE SELECTION & VISUALIZATION
# Challenge 17: AI-Assisted Farmer Disease Diagnostic and Reporting (SIH 1673)
# Round 1 - Feature Relevance Analysis using One-Way ANOVA
# ==============================================================================

cat("=========================================================\n")
cat("       RUNNING ONE-WAY ANOVA ANALYSIS IN R\n")
cat("=========================================================\n\n")

# Set Working Directory
work_dir <- "d:/DS Classs Hackathon 2026"
setwd(work_dir)

# Create Output Directory for Plots
vis_dir <- file.path(work_dir, "r_visualizations")
if (!dir.exists(vis_dir)) {
  dir.create(vis_dir, recursive = TRUE)
}

# 1. Load Dataset
data_path <- file.path(work_dir, "farmer_disease_cleaned_dataset.csv")

if (file.exists(data_path)) {
  cat("Loading cleaned dataset from:", data_path, "\n")
  df <- read.csv(data_path, stringsAsFactors = FALSE)
} else {
  cat("Cleaned dataset CSV not found. Generating sample data for ANOVA...\n")
  set.seed(42)
  n <- 1200
  classes <- c("Corn_Common_Rust", "Corn_Northern_Leaf_Blight", 
               "Potato_Early_Blight", "Potato_Late_Blight", 
               "Tomato_Bacterial_Spot", "Tomato_Healthy")
  target <- sample(classes, n, replace = TRUE)
  
  leaf_spot <- ifelse(target == "Tomato_Healthy", rnorm(n, 1, 0.5),
               ifelse(target == "Potato_Late_Blight", rnorm(n, 35, 6),
               ifelse(target == "Potato_Early_Blight", rnorm(n, 22, 5),
               rnorm(n, 18, 4))))
  
  red_mean <- ifelse(target == "Corn_Common_Rust", rnorm(n, 155, 12),
              ifelse(target == "Tomato_Healthy", rnorm(n, 70, 8),
              rnorm(n, 120, 15)))
  
  green_mean <- ifelse(target == "Tomato_Healthy", rnorm(n, 160, 12), rnorm(n, 110, 10))
  humidity <- ifelse(target == "Potato_Late_Blight", rnorm(n, 90, 4), rnorm(n, 75, 8))
  temp <- ifelse(target == "Potato_Late_Blight", rnorm(n, 19, 3), rnorm(n, 26, 4))
  
  df <- data.frame(
    Crop_Disease_Class = target,
    Leaf_Spot_Coverage_Pct = pmax(0, leaf_spot),
    Red_Mean = red_mean,
    Green_Mean = green_mean,
    Humidity_Pct = humidity,
    Temperature_C = temp,
    Soil_pH = rnorm(n, 6.3, 0.4),
    Crop_Age_Days = rnorm(n, 50, 10)
  )
}

# Ensure Target is Factor
df$Crop_Disease_Class <- as.factor(df$Crop_Disease_Class)
cat("Dataset Loaded successfully. Records:", nrow(df), "Columns:", ncol(df), "\n\n")

# 2. Identify Numerical Features for ANOVA
num_cols <- c("Leaf_Spot_Coverage_Pct", "Red_Mean", "Green_Mean", "Blue_Mean", 
              "Color_Variance", "Texture_Contrast", "Temperature_C", 
              "Humidity_Pct", "Soil_pH", "Rainfall_mm", "Crop_Age_Days")
num_cols <- intersect(num_cols, names(df))

cat("Target Class Levels:", levels(df$Crop_Disease_Class), "\n")
cat("Numerical Features Evaluated:", paste(num_cols, collapse = ", "), "\n\n")

# 3. Perform One-Way ANOVA across all features
cat("--- PERFORMING ONE-WAY ANOVA TESTS ---\n")

results <- data.frame(
  Feature = character(),
  F_Statistic = numeric(),
  p_Value = numeric(),
  DF_Group = numeric(),
  DF_Residuals = numeric(),
  Eta_Squared = numeric(),
  Significance = character(),
  stringsAsFactors = FALSE
)

for (col in num_cols) {
  formula_obj <- as.formula(paste(col, "~ Crop_Disease_Class"))
  fit <- aov(formula_obj, data = df)
  fit_summary <- summary(fit)[[1]]
  
  f_val <- fit_summary["Crop_Disease_Class", "F value"]
  p_val <- fit_summary["Crop_Disease_Class", "Pr(>F)"]
  df_group <- fit_summary["Crop_Disease_Class", "Df"]
  df_res <- fit_summary["Residuals", "Df"]
  
  # Calculate Eta-Squared Effect Size: SS_between / SS_total
  ss_between <- fit_summary["Crop_Disease_Class", "Sum Sq"]
  ss_res <- fit_summary["Residuals", "Sum Sq"]
  eta_sq <- ss_between / (ss_between + ss_res)
  
  sig <- ifelse(p_val < 0.001, "*** Extremely Significant",
         ifelse(p_val < 0.01, "** Highly Significant",
         ifelse(p_val < 0.05, "* Significant", "Not Significant")))
  
  results <- rbind(results, data.frame(
    Feature = col,
    F_Statistic = round(f_val, 2),
    p_Value = p_val,
    DF_Group = df_group,
    DF_Residuals = df_res,
    Eta_Squared = round(eta_sq, 4),
    Significance = sig,
    stringsAsFactors = FALSE
  ))
}

# Sort Results by F-Statistic
results <- results[order(-results$F_Statistic), ]
rownames(results) <- NULL

print(results)

# Save ANOVA Results CSV
csv_out <- file.path(work_dir, "r_anova_results.csv")
write.csv(results, csv_out, row.names = FALSE)
cat("\nANOVA Results exported to:", csv_out, "\n\n")


# 4. VISUALIZATIONS IN R

cat("--- GENERATING HIGH-QUALITY R VISUALIZATIONS ---\n")

# Plot 1: ANOVA F-Statistic Ranking Bar Plot
plot1_path <- file.path(vis_dir, "r_anova_f_scores.png")
png(plot1_path, width = 900, height = 550, res = 120)

par(mar = c(5, 12, 4, 2), bg = "#FAFAFA")
bar_colors <- colorRampPalette(c("#1B4D3E", "#2E8B57", "#48D1CC"))(nrow(results))

bp <- barplot(rev(results$F_Statistic), 
        names.arg = rev(results$Feature), 
        horiz = TRUE, 
        las = 1, 
        col = bar_colors, 
        border = "white",
        xlab = "ANOVA F-Statistic (Higher = Greater Class Separability)", 
        main = "R One-Way ANOVA: Feature Significance Ranking",
        col.main = "#102C57", cex.main = 1.2, font.main = 2,
        cex.names = 0.85, col.axis = "#333333")

grid(nx = NULL, ny = NA, col = "lightgray", lty = "dotted")
text(rev(results$F_Statistic) + max(results$F_Statistic)*0.02, bp, 
     labels = paste0("F=", rev(results$F_Statistic)), 
     pos = 4, cex = 0.75, font = 2, col = "#102C57")

dev.off()
cat("Created Plot 1:", plot1_path, "\n")


# Plot 2: Boxplot of Top Feature across Disease Classes
top_feature <- results$Feature[1]
top_f <- results$F_Statistic[1]
top_p <- results$p_Value[1]

plot2_path <- file.path(vis_dir, "r_anova_top_feature_boxplot.png")
png(plot2_path, width = 950, height = 600, res = 120)

par(mar = c(7, 5, 4, 2), bg = "#FAFAFA")
box_colors <- c("#E74C3C", "#E67E22", "#F1C40F", "#2ECC71", "#1ABC9C", "#3498DB")

boxplot(df[[top_feature]] ~ df$Crop_Disease_Class,
        col = box_colors[1:length(levels(df$Crop_Disease_Class))],
        border = "#2C3E50",
        las = 2,
        xlab = "",
        ylab = paste(top_feature, "Distribution"),
        main = paste("ANOVA Feature Distribution:", top_feature, "by Disease Class"),
        col.main = "#102C57", cex.main = 1.1, font.main = 2,
        outline = TRUE, pch = 20, col.point = "gray40")

grid(nx = NA, ny = NULL, col = "lightgray", lty = "dotted")
mtext(paste0("ANOVA Test: F = ", top_f, ", p < 0.001 (Eta-Squared = ", results$Eta_Squared[1], ")"), 
      side = 3, line = 0.5, cex = 0.9, col = "#27AE60", font = 2)

dev.off()
cat("Created Plot 2:", plot2_path, "\n")


# Plot 3: Tukey Honest Significant Difference (HSD) Post-Hoc Test
plot3_path <- file.path(vis_dir, "r_anova_tukey_hsd.png")
png(plot3_path, width = 1000, height = 750, res = 120)

par(mar = c(5, 15, 4, 2), bg = "#FAFAFA")
fit_top <- aov(as.formula(paste(top_feature, "~ Crop_Disease_Class")), data = df)
tukey_res <- TukeyHSD(fit_top)

plot(tukey_res, las = 1, col = "#2980B9", col.axis = "#333333")
title(main = paste("Tukey HSD 95% Confidence Intervals:", top_feature), col.main = "#102C57")
grid(nx = NULL, ny = NA, col = "lightgray", lty = "dotted")

dev.off()
cat("Created Plot 3:", plot3_path, "\n\n")

cat("=========================================================\n")
cat("   R ANOVA ANALYSIS & VISUALIZATION COMPLETE!\n")
cat("=========================================================\n")
