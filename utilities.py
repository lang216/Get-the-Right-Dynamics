from fractions import Fraction
import re

# Read the content of a text file
def read_txt_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def om_to_python(om_list_str):
    # Initialize an empty list to store the parsed elements
    python_list = []

    # Define a regular expression to match digits and fractions in the input string
    pattern = r"(\d+/\d+|\d+)"

    # Find all matches of the pattern in the input string
    matches = re.findall(pattern, om_list_str)

    for match in matches:
        # If the match is a fraction (e.g., '1/2'), convert it to a Python Fraction
        if '/' in match:
            numerator, denominator = map(int, match.split('/'))
            element = Fraction(numerator, denominator)
        else:
            # If the match is an integer, convert it to an integer
            element = int(match)

        # Append the parsed element to the Python list
        python_list.append(element)

    return python_list

def convert_to_om(data):
    if isinstance(data, list):
        return list_to_om(data)
    elif isinstance(data, tuple):
        return tuple_to_om(data)
    elif isinstance(data, Fraction):
        return fraction_to_om(data)
    elif isinstance(data, int):
        # Handle integer data by converting it to a string representation
        return str(data)
    elif isinstance(data, float):
        # Handle float data by converting it to a string representation
        return str(data)
    else:
        # For unsupported data types, convert to a string representation
        return str(data)

def list_to_om(lst):
    # Helper function to convert elements of the list recursively
    def convert_element(element):
        if isinstance(element, list):
            # If the element is a nested list, recursively convert it
            return list_to_om(element)
        elif isinstance(element, tuple):
            # If the element is a tuple, recursively convert it
            return tuple_to_om(element)
        elif isinstance(element, Fraction):
            # If the element is a Fraction, convert it to the OpenMusic format
            return fraction_to_om(element)
        else:
            # For other data types (int, float), convert to a string representation
            return str(element)

    # Use the helper function to convert each element of the list
    om_elements = [convert_element(element) for element in lst]
    # Join the converted elements and format the list as OpenMusic text format
    return "(" + " ".join(om_elements) + ")"

def tuple_to_om(tpl):
    # Helper function to convert elements of the tuple recursively
    def convert_element(element):
        if isinstance(element, list):
            # If the element is a nested list, recursively convert it
            return list_to_om(element)
        elif isinstance(element, tuple):
            # If the element is a nested tuple, recursively convert it
            return tuple_to_om(element)
        elif isinstance(element, Fraction):
            # If the element is a Fraction, convert it to the OpenMusic format
            return fraction_to_om(element)
        else:
            # For other data types (int, float), convert to a string representation
            return str(element)

    # Use the helper function to convert each element of the tuple
    om_elements = [convert_element(element) for element in tpl]
    # Join the converted elements and format the tuple as OpenMusic text format
    return "(" + " ".join(om_elements) + ")"

def fraction_to_om(fraction):
    return f"{fraction.numerator}/{fraction.denominator}"

