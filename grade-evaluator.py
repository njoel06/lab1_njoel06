import csv
import sys
import os

def load_csv_data():
    """Loads the CSV file into a list of dictionaries."""
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print("Error: The file '" + filename + "' was not found.")
        sys.exit(1)
    
    # Check if file is empty before trying to read
    if os.path.getsize(filename) == 0:
        print("Error: The file '" + filename + "' is empty.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Check if file has no rows (header only or completely empty)
            rows = list(reader)
            if len(rows) == 0:
                print("Error: The file '" + filename + "' has no data (header only or empty).")
                sys.exit(1)
                
            for row in rows:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except KeyError as e:
        print("Error: Missing column in CSV file - " + str(e))
        print("Make sure the CSV has columns: assignment, group, score, weight")
        sys.exit(1)
    except ValueError as e:
        print("Error: Invalid data in CSV file - " + str(e))
        print("Make sure score and weight are numbers")
        sys.exit(1)
    except Exception as e:
        print("Error reading file: " + str(e))
        sys.exit(1)

def evaluate_grades(data):
    """Processes grades and prints results."""
    print("\n--- Grade Evaluation ---\n")
    
    # Task 1: Validate scores (0-100)
    print("Task 1: Score Validation")
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print("  WARNING: " + item['assignment'] + " has invalid score " + str(item['score']))
        else:
            print("  [OK] " + item['assignment'] + ": " + str(item['score']) + "%")
    
    # Task 2: Validate weights
    print("\nTask 2: Weight Validation")
    total_w = sum(item['weight'] for item in data)
    form_w = sum(item['weight'] for item in data if item['group'] == 'Formative')
    sum_w = sum(item['weight'] for item in data if item['group'] == 'Summative')
    
    print("  Total weight: " + str(total_w) + "% (should be 100)")
    print("  Formative: " + str(form_w) + "% (should be 60)")
    print("  Summative: " + str(sum_w) + "% (should be 40)")
    
    # Task 3: Calculate GPA
    print("\nTask 3: GPA Calculation")
    final_grade = sum(item['score'] * (item['weight'] / 100) for item in data)
    gpa = (final_grade / 100) * 5.0
    print("  Final Grade: {:.1f}%".format(final_grade))
    print("  GPA: {:.1f}/5.0".format(gpa))
    
    # Task 4: Pass/Fail (need 50% in BOTH categories)
    print("\nTask 4: Pass/Fail Status")
    form_grade = sum(item['score'] * (item['weight'] / 100) for item in data if item['group'] == 'Formative')
    sum_grade = sum(item['score'] * (item['weight'] / 100) for item in data if item['group'] == 'Summative')
    
    print("  Formative score: {:.1f}%".format(form_grade))
    print("  Summative score: {:.1f}%".format(sum_grade))
    
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
                print("  Eligible for resubmission: " + eligible[0])
            else:
                print("  Eligible for resubmission: " + ', '.join(eligible))

if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
