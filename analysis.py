import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === 1. LOAD DATA ===
try:
    df = pd.read_csv('students.csv')
except FileNotFoundError:
    print("❌ Error: 'students.csv' not found.")
    print("Please run 'create_dataset.py' first to generate the data.")
    exit()

# === 2. CALCULATE TOTAL, AVERAGE, AND GRADE ===

# Calculate Total and Average
df['Total'] = df[['Math', 'Science', 'English']].sum(axis=1)
df['Average'] = df[['Math', 'Science', 'English']].mean(axis=1)

# Define a function to assign grades
def assign_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 75:
        return 'B'
    elif average >= 60:
        return 'C'
    else:
        return 'F'

# Apply the function to create a new 'Grade' column
df['Grade'] = df['Average'].apply(assign_grade)

# Display the final DataFrame
print("--- 📊 Student Performance Report ---")
print(df)
print("\n" + "="*40 + "\n")


# === 3. FIND TOPPERS AND WEAK STUDENTS ===

print("--- 🏆 Analysis Report ---")

# Find Subject-wise Toppers
math_topper = df.loc[df['Math'].idxmax()]
science_topper = df.loc[df['Science'].idxmax()]
english_topper = df.loc[df['English'].idxmax()]
overall_topper = df.loc[df['Total'].idxmax()]

print(f"🥇 Math Topper:    {math_topper['Name']} (Score: {math_topper['Math']})")
print(f"🥇 Science Topper: {science_topper['Name']} (Score: {science_topper['Science']})")
print(f"🥇 English Topper: {english_topper['Name']} (Score: {english_topper['English']})")
print(f"🏆 Overall Topper: {overall_topper['Name']} (Total: {overall_topper['Total']}, Avg: {overall_topper['Average']:.2f})")

# Find Weak Students (Grade 'F')
weak_students = df[df['Grade'] == 'F']

print("\n--- 🚩 Students Needing Attention (Grade F) ---")
if weak_students.empty:
    print("No students received an 'F' grade. Well done!")
else:
    # Show just their name, average, and grade
    print(weak_students[['Name', 'Average', 'Grade']])

print("\n" + "="*40 + "\n")


# === 4. VISUALIZE DATA ===

print("Generating visualizations... (Close each plot window to see the next one)")

# Visualization 1: Bar Chart (Average Score per Student)
plt.figure(figsize=(12, 6))
plt.bar(df['Name'], df['Average'], color='skyblue')
plt.xlabel('Student Name')
plt.ylabel('Average Score')
plt.title('Average Score per Student')
plt.xticks(rotation=45, ha='right') # Rotate names for readability
plt.tight_layout() # Adjust plot to prevent label overlap
plt.grid(axis='y', linestyle='--', alpha=0.7)

print("Displaying Bar Chart (Average Scores)...")
plt.show()


# Visualization 2: Pie Chart (Grade Distribution)
grade_counts = df['Grade'].value_counts().sort_index()
colors = {'A': 'gold', 'B': 'lightgreen', 'C': 'lightskyblue', 'F': 'lightcoral'}

# Ensure we only use colors for grades that actually exist in the data
pie_colors = [colors[grade] for grade in grade_counts.index if grade in colors]

plt.figure(figsize=(7, 7))
plt.pie(
    grade_counts,
    labels=grade_counts.index,
    autopct='%1.1f%%', # Show percentage
    startangle=140,
    colors=pie_colors
)
plt.title('Distribution of Student Grades')
plt.axis('equal') # Ensures the pie chart is a circle

print("Displaying Pie Chart (Grade Distribution)...")
plt.show()

print("\n--- ✅ Analysis Complete ---")