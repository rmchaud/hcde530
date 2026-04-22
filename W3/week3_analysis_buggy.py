import csv

# Load the survey data from a CSV file
filename = "week3_survey_messy.csv"
rows = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# Count responses by role
# Normalize role names so "ux researcher" and "UX Researcher" are counted together
role_counts = {}

for row in rows: #loops thruoug each row in the csv file
    role = row["role"].strip().title() #strips whitespace and converts to title case
    if role in role_counts: #if the role is already in the dictionary, increment the count
        role_counts[role] += 1
    else: #if the role is not in the dictionary, add it with a count of 1
        role_counts[role] = 1 #add the role to the dictionary with a count of 1

print("Responses by role:")
for role, count in sorted(role_counts.items()): #sorts the dictionary by role and prints the count
    print(f"  {role}: {count}")

# Calculate the average years of experience
total_experience = 0 #initializes the total experience to 0
valid_experience_count = 0 #initializes the valid experience count to 0
word_to_number = { #dictionary to convert words to numbers
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
}
for row in rows: #loops through each row in the csv file
    experience = row["experience_years"].strip().lower()
    if not experience: #if the experience is not a number, continue to the next row
        continue
    if experience.isdigit(): #if the experience is a number, add it to the total experience and increment the valid experience count
        total_experience += int(experience)
        valid_experience_count += 1
    elif experience in word_to_number: #if the experience is a word, add the corresponding number to the total experience and increment the valid experience count
        total_experience += word_to_number[experience]
        valid_experience_count += 1

if valid_experience_count > 0: #if the valid experience count is greater than 0, calculate the average experience
    avg_experience = total_experience / valid_experience_count
    print(f"\nAverage years of experience: {avg_experience:.1f}")
else: #if the valid experience count is 0, print that the average years of experience is not available
    print("\nAverage years of experience: N/A")

# Find the top 5 highest satisfaction scores
scored_rows = [] #initializes the scored rows list
for row in rows:
    if row["satisfaction_score"].strip(): #if the satisfaction score is not a number, continue to the next row
        scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

scored_rows.sort(key=lambda x: x[1], reverse=True) #sorts the scored rows list by the satisfaction score in descending order
top5 = scored_rows[:5] #gets the top 5 satisfaction scores

print("\nTop 5 satisfaction scores:")
for name, score in top5: #prints the top 5 satisfaction scores
    print(f"  {name}: {score}")
