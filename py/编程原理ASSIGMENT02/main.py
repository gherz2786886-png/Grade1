import sys
import os
import numpy as np
import id_tools  # QUestion8 Import requirement

# ==========================================
# Question 1: Environment Setup
# ==========================================
id_Hanzhi = "2202502924"
name_Hanzhi = "Hanzhi"

print(f"Hello, my name is {name_Hanzhi} and my 1811ICT student ID is {id_Hanzhi}.")
digits_list = [int(char) for char in id_Hanzhi]
print(f"digits_list: {digits_list}")

# ==========================================
# Question 2: ID-Based Text File Creation
# ==========================================
last4 = id_Hanzhi[-4:]
profile_filename = f"profile_{last4}.txt"

with open(profile_filename, "w") as f:
    f.write(f"name={name_Hanzhi}\n")
    f.write(f"id={id_Hanzhi}\n")
    f.write(f"first={digits_list[0]}\n")
    f.write(f"last={digits_list[-1]}\n")
    f.write(f"sum={sum(digits_list)}\n")
    f.write(f"maximum={max(digits_list)}\n")
print(f"Created file: {profile_filename}")

# ==========================================
# Question 3: Line-by-Line File Reading
# ==========================================
extracted_sum = 0
extracted_max = 0

with open(profile_filename, "r") as f:
    for line_num, line in enumerate(f, start=1):
        clean_line = line.strip()
        print(f"Line {line_num}: {clean_line}")
        if clean_line.startswith("sum="):
            extracted_sum = int(clean_line.split("=")[1])
        elif clean_line.startswith("maximum="):
            extracted_max = int(clean_line.split("=")[1])
            
print(f"Product of sum and maximum: {extracted_sum * extracted_max}")

# ==========================================
# Question 4: Configuration Validator
# ==========================================
profile_dict = {}
error_log = f"error_log_{last4}.txt"
invalid_count = 0

with open(profile_filename, "r") as f:
    for line in f:
        clean_line = line.strip()
        if not clean_line: continue
        
        if clean_line.count("=") == 1:
            key, val = clean_line.split("=")
            profile_dict[key.strip()] = val.strip()
        else:
            invalid_count += 1
            with open(error_log, "a") as ef:
                ef.write(f"Invalid format: {clean_line}\n")

if invalid_count == 0:
    print("Profile file is valid")
else:
    print(f"Detected {invalid_count} invalid lines.")

# ==========================================
# Question 5: Unique Digit Set Analyzer
# ==========================================
unique_digits = set(digits_list)
print(f"Sorted unique_digits: {sorted(list(unique_digits))}")

last_digit = digits_list[-1]
# last_digit for 2202502924 is 4 (even)
benchmark_digits = {0, 2, 4, 6, 8} if last_digit % 2 == 0 else {1, 3, 5, 7, 9}

print(f"Union: {sorted(list(unique_digits | benchmark_digits))}")
print(f"Intersection: {sorted(list(unique_digits & benchmark_digits))}")
print(f"Difference (unique - benchmark): {sorted(list(unique_digits - benchmark_digits))}")

# ==========================================
# Question 6: Dictionary Profile
# ==========================================
digit_profile = {
    "first": digits_list[0],
    "last": digits_list[-1],
    "sum": sum(digits_list),
    "minimum": min(digits_list),
    "maximum": max(digits_list),
    "parity": "even" if digits_list[-1] % 2 == 0 else "odd"
}

middle_val = digit_profile.get("middle", "not available")
print(f"Full digit_profile: {digit_profile}")
print(f"Safe lookup for 'middle': {middle_val}")

# ==========================================
# Question 7: Digit Frequency Dictionary
# ==========================================
frequency = {}
for d in digits_list:
    frequency[d] = frequency.get(d, 0) + 1

for d in sorted(frequency.keys()):
    print(f"Digit {d}: {frequency[d]} times")

max_freq = max(frequency.values())
tied_digits = [k for k, v in frequency.items() if v == max_freq]
highest_freq_digit = min(tied_digits)
print(f"Digit with highest frequency (tie-broken): {highest_freq_digit}")

once_set = {k for k, v in frequency.items() if v == 1}
multiple_set = {k for k, v in frequency.items() if v > 1}
print(f"Digits appearing once: {sorted(list(once_set))}")
print(f"Digits appearing >once: {sorted(list(multiple_set))}")

# ==========================================
# Question 8: Custom Module Runner
# ==========================================
# Imports id_tools at the top of the file
print(f"Module Q8 Sum: {id_tools.digit_sum(id_Hanzhi)}, Parity: {id_tools.digit_parity(id_Hanzhi)}")

# ==========================================
# Question 9 & 10: Class-Based System & Registry
# ==========================================
class StudentIdentity:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        
    def masked_id(self):
        if len(self.student_id) <= 4: return self.student_id
        return f"{self.student_id[:2]}{'*' * (len(self.student_id)-4)}{self.student_id[-2:]}"
        
    def checksum(self):
        return sum(int(c) for c in self.student_id)
        
    def __str__(self):
        return f"[{self.name} | ID: {self.masked_id()} | Checksum: {self.checksum()}]"

registry = {
    "me": StudentIdentity(name_Hanzhi, id_Hanzhi),
    "peer1": StudentIdentity("Alice", "9" + id_Hanzhi[1:]),
    "peer2": StudentIdentity("Bob", id_Hanzhi[:-1] + "1")
}

for label, obj in registry.items():
    print(f"{label}: {obj}")

highest_label = min([lbl for lbl, obj in registry.items() if obj.checksum() == max(o.checksum() for o in registry.values())])
print(f"Highest checksum label: {highest_label}")

# ==========================================
# Question 11: NumPy Array Construction
# ==========================================
digits_array = np.array(digits_list)
print(f"Array shape: {digits_array.shape}, size: {digits_array.size}, dtype: {digits_array.dtype}")

# Extract first 6 digits for 2x3 matrix mapping
matrix_2x3 = np.array(digits_list[:6]).reshape(2, 3)
print(f"2x3 Matrix:\n{matrix_2x3}")
print(f"Row sums: {matrix_2x3.sum(axis=1)}")
print(f"Col max: {matrix_2x3.max(axis=0)}")

# ==========================================
# Question 12: Broadcasting and File Output
# ==========================================
base_3x3 = np.arange(1, 10).reshape(3, 3)
vec_1d = np.array([digits_list[0], digits_list[-1], sum(digits_list) % 10])
broadcast_res = base_3x3 + vec_1d
print(f"Original Matrix:\n{base_3x3}")
print(f"ID-Derived Vector: {vec_1d}")
print(f"Broadcast Result:\n{broadcast_res}")

broadcast_file = f"broadcast_{last4}.txt"
np.savetxt(broadcast_file, broadcast_res, fmt='%d')
print(f"Broadcast result saved to: {broadcast_file}")

# ==========================================
# Question 13: NumPy Statistical Report
# ==========================================
float_arr = digits_array.astype(float)
print(f"Mean: {np.mean(float_arr):.2f}")
print(f"Standard Deviation: {np.std(float_arr):.2f}")
print(f"Minimum: {float_arr.min():.2f}")
print(f"Maximum: {float_arr.max():.2f}")
print(f"Square Root of (digit+1): {np.sqrt(float_arr + 1).round(2)}")

d_min, d_max = float_arr.min(), float_arr.max()
norm_arr = np.zeros_like(float_arr) if d_min == d_max else (float_arr - d_min) / (d_max - d_min)

report_file = f"numpy_report_{last4}.txt"
with open(report_file, "w") as f:
    for orig, norm in zip(float_arr, norm_arr):
        f.write(f"{orig:.1f},{norm:.2f}\n")

# ==========================================
# Question 14: Import Statement Scanner
# ==========================================
sample_script_name = f"sample_script_{last4}.py"
imported_modules = set()

# Safe fallback definition in case file isn't created manually
if not os.path.exists(sample_script_name):
    print(f"Warning: {sample_script_name} not found. Please create it first.")
else:
    with open(sample_script_name, "r") as f:
        for line in f:
            clean_line = line.strip()
            if clean_line.startswith("import "):
                # Handles "import math" -> extracts "math"
                module_name = clean_line.split(" ")[1].split(",")[0]
                imported_modules.add(module_name)
            elif clean_line.startswith("from "):
                # Handles "from random import randint" -> extracts "random"
                module_name = clean_line.split(" ")[1]
                imported_modules.add(module_name)

    print(f"Unique modules imported in sample script: {imported_modules}")

# ==========================================
# Question 15: Integrated Gradebook
# ==========================================
class GradeRecord:
    def __init__(self, label, mark):
        self.label = label
        self.mark = mark
    def grade_band(self):
        if self.mark >= 85: return "HD"
        if self.mark >= 75: return "D"
        if self.mark >= 65: return "C"
        if self.mark >= 50: return "P"
        return "F"

marks_file = f"marks_{last4}.txt"
# Initialize mock data as required
with open(marks_file, "w") as f:
    f.write(f"student_A,42\nstudent_B,91\nstudent_C,76\nstudent_D,55\nstudent_me,{sum(digits_list)}\n")

records = {}
with open(marks_file, "r") as f:
    for line in f:
        lbl, mk = line.strip().split(",")
        records[lbl] = GradeRecord(lbl, int(mk))

marks_array = np.array([r.mark for r in records.values()])
bands = {r.grade_band() for r in records.values()}

mean_mark = marks_array.mean()
max_mark = marks_array.max()
min_mark = marks_array.min()

print(f"Gradebook Mean: {mean_mark:.2f}")
print(f"Gradebook Max: {max_mark}")
print(f"Gradebook Min: {min_mark}")
print(f"Unique Grade Bands: {bands}")

band_counts = {band: 0 for band in ["HD", "D", "C", "P", "F"]}
for r in records.values():
    band_counts[r.grade_band()] += 1

summary_file = f"grade_summary_{last4}.txt"
with open(summary_file, "w") as f:
    f.write(f"Average Mark: {mean_mark:.2f}\n")
    f.write(f"Maximum Mark: {max_mark}\n")
    f.write(f"Minimum Mark: {min_mark}\n")
    f.write("Band Counts:\n")
    for b, count in band_counts.items():
        f.write(f"  {b}: {count}\n")
