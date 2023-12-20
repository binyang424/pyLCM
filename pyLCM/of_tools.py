import numpy as np


def read_flow_rate(file_path):
    """
    Read flow rate data from a file generated by "#includeFunc flowRatePatch"
    function in OpenFOAM and return a dictionary consisting of area and flow rate data.
    TODO : Add a file template and link to the documentation

    Parameters
    ----------
    file_path : str
        Path to the file containing flow rate data

    Returns
    -------
    data : dict
        Dictionary containing area and flow rate data.
    """
    # Create an empty dictionary to store data
    data = {"area": None, "flow rate": None}

    # Create empty lists to store time and flow rate data
    time_values = []
    flow_rate_values = []

    # Open the file and read its content
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Ignore comment lines
            if line.startswith('#'):
                if "Area" in line:
                    # Extract area information
                    data["area"] = float(line.split(":")[1].strip())
                continue

            # Extract time and flow rate information
            values = [float(value) for value in line.split()]
            time_values.append(values[0])
            flow_rate_values.append(values[1])

    # Convert time and flow rate data to NumPy arrays
    time_array = np.array(time_values)
    flow_rate_array = np.array(flow_rate_values)

    # stack time and flow rate data
    time_flow_rate = np.column_stack((time_array, flow_rate_array))

    # Store in the dictionary
    data["flow rate"] = time_flow_rate[1:-1:2, :]

    return data