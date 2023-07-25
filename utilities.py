from fractions import Fraction
import re

# Read the content of a text file
def read_txt_file(filename):
    with open(filename, 'r') as f:
        return f.read()

import re
from fractions import Fraction

def om_to_python(om_list_str):
    # Initialize an empty list to store the parsed elements
    python_list = []

    # Define a regular expression to match individual lists in the input string
    list_pattern = r'\((.*?)\)'

    # Find all matches of lists in the input string
    list_matches = re.findall(list_pattern, om_list_str)

    for sublist_str in list_matches:
        # Define a regular expression to match digits and fractions in the sublist string
        pattern = r"(\d+\.\d+|\d+/\d+|\d+)"

        # Find all matches of the pattern in the sublist string
        matches = re.findall(pattern, sublist_str)

        sublist = []
        for match in matches:
            # If the match is a float (e.g., '1.5'), convert it to a float
            if '.' in match:
                element = float(match)
            # If the match is a fraction (e.g., '1/2'), convert it to a Python Fraction
            elif '/' in match:
                numerator, denominator = map(int, match.split('/'))
                element = Fraction(numerator, denominator)
            else:
                # If the match is an integer, convert it to an integer
                element = int(match)

            # Append the parsed element to the sublist
            sublist.append(element)

        # Append the sublist to the Python list
        python_list.append(sublist)

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

def convert_ms_2_s(l):
    l_in_s = []
    for e in l:
        l_in_s.append(e/1000)
    return l_in_s

def make_lol(l):
    lol = []
    for e in l:
        lol.append([e])
    return lol

def db_to_midi_velocity(amplitudes, max_dB, min_dB):
    """
    Map a list (or list of lists) of dB values to MIDI velocities without considering psychoacoustics.

    Parameters:
        amplitudes (list or list of lists): The list of dB values to map to MIDI velocities.
        max_dB (float): The maximum dB value in the input range.
        min_dB (float): The minimum dB value in the input range.

    Returns:
        list or list of lists: The mapped MIDI velocities corresponding to the input dB values.
    """
    # Function to map a single dB value to MIDI velocity
    def map_single_db_to_midi_velocity(dB_value):
        return int((dB_value - min_dB) / (max_dB - min_dB) * 127)

    # Check if the input is a list or list of lists
    if isinstance(amplitudes[0], list):
        # Input is a list of lists
        velocities = []
        for amplitude_list in amplitudes:
            velocity_list = [map_single_db_to_midi_velocity(dB_value) for dB_value in amplitude_list]
            velocities.append(velocity_list)
    else:
        # Input is a flat list
        velocities = [map_single_db_to_midi_velocity(dB_value) for dB_value in amplitudes]

    return velocities


def midi_velocity_to_dynamic(velocities):
    """
    Map MIDI velocities to musical dynamics represented as strings.

    Parameters:
        velocities (int or list or list of lists): The MIDI velocities to map to musical dynamics.

    Returns:
        str or list or list of lists: The musical dynamics represented as strings.
    """
    # Function to map a single MIDI velocity to musical dynamic
    def map_single_velocity_to_dynamic(velocity):
        dynamic_levels = ["ppp", "pp", "p", "mp", "mf", "f", "ff", "fff"]
        return dynamic_levels[min((velocity * (len(dynamic_levels) - 1)) // 127, len(dynamic_levels) - 1)]

    # Check if the input is a single value or a list of lists
    if isinstance(velocities, list):
        if isinstance(velocities[0], list):
            # Input is a list of lists
            return [[map_single_velocity_to_dynamic(velocity) for velocity in velocity_list] for velocity_list in velocities]
        else:
            # Input is a flat list
            return [map_single_velocity_to_dynamic(velocity) for velocity in velocities]
    else:
        # Input is a single value
        return map_single_velocity_to_dynamic(velocities)
