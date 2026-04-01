import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    
    # a) Check if all scores are percentage based (0-100)
    invalid_scores = [item for item in data if not (0 <= item['score'] <= 100)]
    if invalid_scores:
        print("Error: Some scores are not between 0 and 100.")
        return
    
    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    total_weight = sum(item['weight'] for item in data)
    if total_weight != 100:
        print(f"Error: Total weight is {total_weight}, should be 100.")
        return
    
    formative = [item for item in data if item['group'] == 'Formative']
    summative = [item for item in data if item['group'] == 'Summative']
    
    formative_weight = sum(item['weight'] for item in formative)
    summative_weight = sum(item['weight'] for item in summative)
    
    if formative_weight != 60 or summative_weight != 40:
        print(f"Error: Formative weight {formative_weight} (should be 60), Summative {summative_weight} (should be 40).")
        return
    
    # c) Calculate the Final Grade and GPA
    final_grade = sum(item['score'] * item['weight'] / 100 for item in data)
    
    # GPA: assume standard scale
    if final_grade >= 90:
        gpa = 4.0
        letter = 'A'
    elif final_grade >= 80:
        gpa = 3.0
        letter = 'B'
    elif final_grade >= 70:
        gpa = 2.0
        letter = 'C'
    elif final_grade >= 60:
        gpa = 1.0
        letter = 'D'
    else:
        gpa = 0.0
        letter = 'F'
    
    # d) Determine Pass/Fail status (>= 50% in BOTH categories)
    formative_score = sum(item['score'] * item['weight'] / formative_weight for item in formative) if formative else 0
    summative_score = sum(item['score'] * item['weight'] / summative_weight for item in summative) if summative else 0
    
    pass_formative = formative_score >= 50
    pass_summative = summative_score >= 50
    passed = pass_formative and pass_summative
    
    # e) Check for failed formative assignments (< 50%)
    #     and determine which one(s) have the highest weight for resubmission.
    failed_formative = [item for item in formative if item['score'] < 50]
    if failed_formative:
        max_weight = max(item['weight'] for item in failed_formative)
        resubmission = [item for item in failed_formative if item['weight'] == max_weight]
    else:
        resubmission = []
    
    # f) Print the final decision (PASSED / FAILED) and resubmission options
    print(f"Final Grade: {final_grade:.2f}%")
    print(f"Letter Grade: {letter}")
    print(f"GPA: {gpa}")
    print(f"Formative Score: {formative_score:.2f}%")
    print(f"Summative Score: {summative_score:.2f}%")
    print(f"Status: {'PASSED' if passed else 'FAILED'}")
    if not passed:
        if not pass_formative:
            print("Failed Formative")
        if not pass_summative:
            print("Failed Summative")
    if resubmission:
        print("Resubmission options:")
        for item in resubmission:
            print(f"  {item['assignment']} (weight: {item['weight']})")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
