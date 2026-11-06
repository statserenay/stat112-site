# STAT 112 - Homework 1, Question 1(c)
# Box plot of daily phone screen time (example data, n = 7)

# 1. Enter the data (minutes per day, Monday to Sunday)
screen <- c(182, 205, 168, 224, 197, 310, 190)
days   <- c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

# 2. Quartiles with the lecture method: Q1 at position (n+1)/4, Q3 at 3(n+1)/4.
#    In R this is quantile(..., type = 6).
#    NOTE: R's default boxplot() uses a different method (Tukey's hinges)
#    and would draw the box from 186 to 214.5 instead of 182 to 224.
q  <- quantile(screen, probs = c(0.25, 0.50, 0.75), type = 6)
Q1 <- unname(q[1]); Med <- unname(q[2]); Q3 <- unname(q[3])
IQR_val <- Q3 - Q1

# 3. Fences and outliers
lower_fence <- Q1 - 1.5 * IQR_val
upper_fence <- Q3 + 1.5 * IQR_val
outliers    <- screen[screen < lower_fence | screen > upper_fence]

# 4. Whiskers end at the most extreme values that are NOT outliers
lower_whisker <- min(screen[screen >= lower_fence])
upper_whisker <- max(screen[screen <= upper_fence])

# Print the results
cat("Sorted data:   ", sort(screen), "\n")
cat("Five-number summary: Min =", min(screen), " Q1 =", Q1, " Median =", Med,
    " Q3 =", Q3, " Max =", max(screen), "\n")
cat("IQR =", IQR_val, "\n")
cat("Lower fence =", lower_fence, "  Upper fence =", upper_fence, "\n")
cat("Potential outlier(s):", outliers,
    "(", days[screen %in% outliers], ")\n")

# 5. Draw the box plot with these exact values using bxp()
stats <- list(
  stats = matrix(c(lower_whisker, Q1, Med, Q3, upper_whisker), ncol = 1),
  n     = length(screen),
  out   = outliers,
  group = rep(1, length(outliers)),
  names = ""
)

bxp(stats, horizontal = TRUE, boxfill = "lightblue", outpch = 19,
    outcol = "red", ylim = c(150, 320), axes = FALSE,
    main = "Box plot of daily screen time (n = 7)",
    xlab = "Daily phone screen time (minutes)")
axis(1, at = seq(160, 320, by = 20))

# 6. Mark the upper fence and label the five-number summary
abline(v = upper_fence, lty = 2, col = "red")
text(upper_fence, 1.45, paste("Upper fence =", upper_fence), col = "red", cex = 0.8, pos = 2)

text(min(screen), 1.25, paste("Min =", min(screen)), cex = 0.8)
text(Q1,          1.50, paste("Q1 =", Q1),           cex = 0.8)
text(Med,         0.55, paste("Median =", Med),      cex = 0.8, font = 2)
text(Q3,          1.50, paste("Q3 =", Q3),           cex = 0.8)
text(max(screen), 1.20, paste("Max =", max(screen), "(outlier)"),
     col = "red", cex = 0.8)
