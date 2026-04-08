import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

# Data
df = pd.read_csv("student_data.csv")
print("Raw Data: ")
print(df)

# Basic Calculation
# Calculate average score per student
df['Average'] = df[["Math","Science","English"]].mean(axis=1)
# Rank students by average
df["Rank"] = df["Average"].rank(ascending=False)

print("\nWith Averages and Ranks:")
print(df)

print("\nSubject-wise Mean Scores:")
print(df[["Math","Science","English"]].mean())

print("\nCorrelation between subjects:")
print(df[["Math","Science","English"]].corr())

# Visualization 
# Bar plot of average scores per student
plt.figure(figsize=(6,4))
sns.barplot(x="Student", y="Average", data=df, palette="viridis")
plt.title("Average Score per Student")
plt.show()

# Distribution of scores in each subject
plt.figure(figsize=(8,5))
sns.boxplot(data=df[["Math", "Science", "English"]])
plt.title("Score Distribution by Subject")
plt.show()