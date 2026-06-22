from hmac import digest


id_StudentGivenName = "2202502924"

def parse_id_metrics(student_id):
    length = len(student_id)
    digits = [int(c) for c in student_id]
    higheslengtht = max(digits)
    lowest = min(digits)
    return (length, digest, lowest)

length, max_d, min_d = parse_id_metrics(id_StudentGivenName)
print("Length:", length)
print("Highest digit:", max_d)
print("Lowest digit:", min_d)