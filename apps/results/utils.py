"""
GPA calculation utilities for KIU Result Management System
"""

class GPACalculator:
    """
    Handles GPA and CGPA calculations.
    KIU Grading Scale (5.0 System)
    """
    
    GRADING_SCALE = [
        {'grade': 'A', 'min_score': 80, 'max_score': 100, 'grade_point': 5.0, 'remark': 'Excellent'},
        {'grade': 'B+', 'min_score': 75, 'max_score': 79, 'grade_point': 4.5, 'remark': 'Very Good'},
        {'grade': 'B', 'min_score': 70, 'max_score': 74, 'grade_point': 4.0, 'remark': 'Good'},
        {'grade': 'C+', 'min_score': 65, 'max_score': 69, 'grade_point': 3.5, 'remark': 'Fairly Good'},
        {'grade': 'C', 'min_score': 60, 'max_score': 64, 'grade_point': 3.0, 'remark': 'Fair'},
        {'grade': 'D+', 'min_score': 55, 'max_score': 59, 'grade_point': 2.5, 'remark': 'Pass'},
        {'grade': 'D', 'min_score': 50, 'max_score': 54, 'grade_point': 2.0, 'remark': 'Pass'},
        {'grade': 'E', 'min_score': 45, 'max_score': 49, 'grade_point': 1.5, 'remark': 'Pass'},
        {'grade': 'F', 'min_score': 0, 'max_score': 44, 'grade_point': 0.0, 'remark': 'Fail'},
    ]
    
    @classmethod
    def get_grade_info(cls, score):
        """Get grade details for a given score"""
        if score is None:
            return {'grade': 'F', 'grade_point': 0.0, 'remark': 'Fail'}
        
        for grade_info in cls.GRADING_SCALE:
            if grade_info['min_score'] <= score <= grade_info['max_score']:
                return grade_info
        
        return cls.GRADING_SCALE[-1]
    
    @classmethod
    def calculate_semester_gpa(cls, results):
        """
        Calculate GPA for a semester
        GPA = Σ(Grade Point × Credit Units) / Σ(Credit Units)
        """
        total_grade_points = 0
        total_credit_units = 0
        
        for result in results:
            credit_units = result.course.credit_units
            grade_point = float(result.grade_point) if result.grade_point else 0
            total_grade_points += grade_point * credit_units
            total_credit_units += credit_units
        
        if total_credit_units == 0:
            return 0.0
        
        return round(total_grade_points / total_credit_units, 2)
    
    @classmethod
    def calculate_cgpa(cls, all_results):
        """Calculate CGPA across all semesters"""
        total_grade_points = 0
        total_credit_units = 0
        
        for result in all_results:
            credit_units = result.course.credit_units
            grade_point = float(result.grade_point) if result.grade_point else 0
            total_grade_points += grade_point * credit_units
            total_credit_units += credit_units
        
        if total_credit_units == 0:
            return 0.0
        
        return round(total_grade_points / total_credit_units, 2)
    
    @classmethod
    def get_gpa_classification(cls, gpa):
        """Get degree classification based on CGPA"""
        if gpa >= 4.5:
            return 'First Class Honours'
        elif gpa >= 3.5:
            return 'Second Class Honours (Upper Division)'
        elif gpa >= 2.5:
            return 'Second Class Honours (Lower Division)'
        elif gpa >= 1.5:
            return 'Pass'
        else:
            return 'Fail'