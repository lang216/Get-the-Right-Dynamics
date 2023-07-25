# Get-the-Right-Dynamics

## Introduction
Welcome to the "Get-the-Right-Dynamics" project! This tool is designed to assist myself in finding the corresponding loudness of specific frequencies at given locations in an audio file. It provides valuable insights into the dynamics of your audio composition. The tool returns the loudness measured in dB (B-Weighting Applied), MIDI values, and conventional music notations. This project is created as an assistive tool for my doctoral dissertation, a large-scale orchestral piece scheduled to be completed in 2023.

## Project Overview
- Frequency Loudness Analysis: Analyze an audio file to extract amplitude data and frequencies.
- Loudness Calculation: Calculate loudness (weighted with B-Weighting) at specific timepoints and frequencies using linear interpolation.
- Musical Notations: Map loudness values to MIDI values and conventional music notations (e.g., "ppp", "pp", "p", "mp", "mf", "f", "ff", "fff").

## How to Use
- The list of required packages will be provided in the 'requirements.txt' file (to be released).
- Prepare your audio file and specify its path in the 'audio_file' variable within the 'main.py' script.
- Customize the list of frequencies and timepoints in the 'input_frequencies.txt' and 'input_timepoints.txt' files, respectively, to match your desired analysis points.
- Run the 'main.py' script to process the audio and generate the dynamics data.
- View the results in the 'output.txt' file, which includes loudness measured in dB (B-Weighting Applied), MIDI values, and corresponding conventional music notations.

## Note
This tool is specifically designed for compositional use and tailored to work seamlessly with OpenMusic (LISP), a music composition environment. As a result, all input data (and output data) should be formatted in accordance with OpenMusic's specific data format. You can format your input data using the provided functions in the 'utilities.py' script. These functions are specifically designed to convert data between Python and OpenMusic formats, ensuring smooth compatibility with this tool.

## Contribute
Your contributions to improve and expand this tool are highly valued. If you have any ideas, feature requests, or bug fixes, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the GPL-3.0 License. You are free to use, modify, and distribute the code under the terms of this license.
