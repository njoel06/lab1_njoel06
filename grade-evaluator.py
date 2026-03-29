import csv
import sys
import os

def load_csv_data():
    """Loads the CSV file into a list of dictionaries."""
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """Processes grades and prints results."""
    print("\n--- Grade Evaluation ---\n")
    
    # Task 1: Validate scores (0-100)
    print("Task 1: Score Validation")
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"  WARNING: {item['assignment']} has invalid score {item['score']}")
        else:
            print(f"  ✓ {item['assignment']}: {item['score']}%")
    
    # Task 2: Validate weights
    print("\nTask 2: Weight Validation")
    total_w = sum(item['weight'] for item in data)
    form_w = sum(item['weight'] for item in data if item['group'] == 'Formative')
    sum_w = sum(item['weight'] for item in data if item['group'] == 'Summative')
    
    print(f"  Total weight: {total_w}% (should be 100)")
    print(f"  Formative: {form_w}% (should be 60)")
    print(f"  Summative: {sum_w}% (should be 40)")
    
    # Task 3: Calculate GPA
    print("\nTask 3: GPA Calculation")
    final_grade = sum(item['score'] * (item['weight'] / 100) for item in data)
    gpa = (final_grade / 100) * 5.0
    print(f"  Final Grade: {final_grade:.1f}%")
    print(f"  GPA: {gpa:.1f}/5.0")
    
    # Task 4: Pass/Fail (need 50% in BOTH categories)
    print("\nTask 4: Pass/Fail Status")
    form_grade = sum(item['score'] * (item['weight'] / 100) for item in data if item['group'] == 'Formative')
    sum_grade = sum(item['score'] * (item['weight'] / 100) for item in data if item['group'] == 'Summative')
    
    print(f"  Formative score: {form_grade:.1f}%")
    print(f"  Summative score: {sum_grade:.1f}%")
    
    if form_grade >= 50 and sum_grade >= 50:
        print("  STATUS: PASSED")
    else:
        print("  STATUS: FAILED")
        
        # Task 5: Find resubmission candidates
        print("\nTask 5: Resubmission Eligibility")
        failed = [item for item in data if item['group'] == 'Formative' and item['score'] < 50]
        
        if failed:
            max_weight = max(item['weight'] for item in failed)
            eligible = [item['assignment'] for item in failed if item['weight'] == max_weight]
            
            if len(eligible) == 1:
                print(f"  Eligible for resubmission: {eligible[0]}")
            else:
                print(f"  Eligible for resubmission: {', '.join(eligible)}")

if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
