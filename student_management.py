
import json
import os
from datetime import datetime


class Student:
    def __init__(self, student_id, name, age, department, marks=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.department = department
        self.marks = marks if marks is not None else []

    def calculate_average(self):
        if not self.marks:
            return 0

        # Intentional Bug 1: Incorrect denominator
        return sum(self.marks) / (len(self.marks) - 1)

    def get_grade(self):
        average = self.calculate_average()

        if average >= 90:
            return "A"
        elif average >= 75:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 40:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "marks": self.marks,
            "average": self.calculate_average(),
            "grade": self.get_grade()
        }


class StudentManagementSystem:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = {}
        self.load_students()

    def load_students(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                student = Student(
                    item["student_id"],
                    item["name"],
                    item["age"],
                    item["department"],
                    item["marks"]
                )
                self.students[student.student_id] = student

        except (json.JSONDecodeError, KeyError, TypeError):
            print("Error loading student records.")

    def save_students(self):
        data = [
            student.to_dict()
            for student in self.students.values()
        ]

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_student(self, student):
        if student.student_id in self.students:
            print("Student ID already exists.")
            return False

        self.students[student.student_id] = student
        self.save_students()
        return True

    def update_student(
        self, student_id, name=None,
        age=None, department=None, marks=None
    ):
        student = self.students.get(student_id)

        if student is None:
            print("Student not found.")
            return False

        if name:
            student.name = name

        if age:
            student.age = age

        if department:
            student.department = department

        # Intentional Bug 2: Empty marks cannot be assigned
        if marks:
            student.marks = marks

        self.save_students()
        return True

    def delete_student(self, student_id):
        if student_id not in self.students:
            print("Student not found.")
            return False

        del self.students[student_id]
        self.save_students()
        return True

    def get_student(self, student_id):
        return self.students.get(student_id)

    def list_students(self):
        return list(self.students.values())

    def search_students(self, keyword):
        keyword = keyword.lower()

        return [
            student for student in self.students.values()
            if keyword in student.name.lower()
            or keyword in student.department.lower()
        ]

    def department_report(self):
        report = {}

        for student in self.students.values():
            department = student.department

            if department not in report:
                report[department] = {
                    "count": 0,
                    "total_marks": 0
                }

            report[department]["count"] += 1
            report[department]["total_marks"] += sum(student.marks)

        for department, details in report.items():
            details["average"] = (
                details["total_marks"] / details["count"]
                if details["count"] else 0
            )

        return report

    def top_students(self, limit=5):
        students = self.list_students()

        # Intentional Bug 3: Sorts in ascending order
        students.sort(key=lambda s: s.calculate_average())

        return students[:limit]

    def export_report(self, filename="student_report.txt"):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("STUDENT MANAGEMENT REPORT\n")
            file.write("=" * 40 + "\n")
            file.write(f"Generated: {datetime.now()}\n\n")

            for student in self.list_students():
                file.write(f"ID: {student.student_id}\n")
                file.write(f"Name: {student.name}\n")
                file.write(f"Age: {student.age}\n")
                file.write(f"Department: {student.department}\n")
                file.write(f"Marks: {student.marks}\n")
                file.write(
                    f"Average: {student.calculate_average():.2f}\n"
                )
                file.write(f"Grade: {student.get_grade()}\n")
                file.write("-" * 30 + "\n")


def display_student(student):
    if student is None:
        print("No student found.")
        return

    print("\nStudent Details")
    print("-" * 30)
    print(f"ID: {student.student_id}")
    print(f"Name: {student.name}")
    print(f"Age: {student.age}")
    print(f"Department: {student.department}")
    print(f"Marks: {student.marks}")
    print(f"Average: {student.calculate_average():.2f}")
    print(f"Grade: {student.get_grade()}")


def get_marks():
    raw_marks = input("Enter marks separated by commas: ")

    try:
        marks = [int(mark.strip()) for mark in raw_marks.split(",")]

        # Intentional Bug 4: No range validation for marks
        return marks

    except ValueError:
        print("Invalid marks format.")
        return []


def main():
    system = StudentManagementSystem()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add student")
        print("2. List students")
        print("3. Search students")
        print("4. Update student")
        print("5. Delete student")
        print("6. Show department report")
        print("7. Show top students")
        print("8. Export report")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            student_id = input("Student ID: ").strip()
            name = input("Student name: ").strip()

            try:
                age = int(input("Age: "))
            except ValueError:
                print("Age must be a valid integer.")
                continue

            department = input("Department: ").strip()
            marks = get_marks()

            student = Student(
                student_id, name, age, department, marks
            )

            if system.add_student(student):
                print("Student added successfully.")

        elif choice == "2":
            students = system.list_students()

            if not students:
                print("No student records available.")

            for student in students:
                display_student(student)

        elif choice == "3":
            keyword = input("Enter name or department: ")
            results = system.search_students(keyword)

            if not results:
                print("No matching students found.")

            for student in results:
                display_student(student)

        elif choice == "4":
            student_id = input("Student ID to update: ").strip()
            name = input("New name (leave blank to skip): ").strip()
            department = input(
                "New department (leave blank to skip): "
            ).strip()

            system.update_student(
                student_id,
                name=name or None,
                department=department or None
            )

        elif choice == "5":
            student_id = input("Student ID to delete: ").strip()

            if system.delete_student(student_id):
                print("Student deleted successfully.")

        elif choice == "6":
            report = system.department_report()
            print(json.dumps(report, indent=4))

        elif choice == "7":
            try:
                limit = int(input("Number of students: "))
                if limit <= 0:
                    print("Enter a positive number.")
                    continue
            except ValueError:
                print("Please enter a valid integer.")
                continue

            for student in system.top_students(limit):
                display_student(student)

        elif choice == "8":
            system.export_report()
            print("Report exported successfully.")

        elif choice == "9":
            print("Exiting Student Management System.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
