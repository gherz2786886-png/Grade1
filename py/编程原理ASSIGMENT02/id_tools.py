def digit_sum(id_string):
    """Returns the sum of all numeric characters in the string."""
    return sum(int(c) for c in id_string if c.isdigit())

def digit_parity(id_string):
    """Returns 'even' or 'odd' based on the final digit."""
    return "even" if int(id_string[-1]) % 2 == 0 else "odd"

if __name__ == "__main__":
    # Test block strictly executed only when running this module directly
    test_id = "2202502924"
    print(f"[id_tools Test] Sum: {digit_sum(test_id)}, Parity: {digit_parity(test_id)}")
