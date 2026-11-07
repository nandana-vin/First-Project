def calculate_weighted_grade(grade, weight):
    return grade * weight / 100


def calculate_current_average(total_weighted_grade, total_weight):
    if total_weight <= 0:
        return 0

    return total_weighted_grade / total_weight * 100


def calculate_required_grade(target_grade, total_weighted_grade, total_weight):
    remaining_weight = 100 - total_weight

    if remaining_weight <= 0:
        return None

    return (target_grade - total_weighted_grade) / remaining_weight * 100