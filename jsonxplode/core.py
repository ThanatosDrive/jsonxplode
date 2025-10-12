class FlattenJson:
    def __init__(self):
        """
        Initialize a JSON flattener instance.

        Attributes:
        complete_data : list
            Contains the flattened format of the JSON data as list of dictionaries
        """
        self.complete_data = []

    def flatten_json(self, data, column_data: dict = None, value_name: str = '', key_counter:dict = None):
        """
        Recursively flattens nested JSON structures (dicts and lists) into flat dictionaries.

        This method processes complex JSON data by traversing through nested dictionaries
        and lists, creating flattened key-value pairs where nested keys are combined using
        dot notation (e.g., 'parent.child.grandchild').

        The method uses a recursive approach with state tracking to prevent duplicate
        or partial records by monitoring when data has been saved at deeper recursion levels.

        Parameters:
        -----------
        data : any
            The JSON data to flatten. Can be a dict, list, or primitive value.

        column_data : dict, optional
            Accumulator dictionary for flattened key-value pairs during recursion.
            Should be None when called externally (default: None).

        value_name : str, optional
            Current key path prefix for nested structures. Used internally during
            recursion to build dot-separated key paths (default: '').

        Returns:
        --------
        tuple (dict, bool)
            - dict: The accumulated flattened data up to this recursion level
            - bool: Flag indicating if data was saved at this or deeper levels

        Internal State:
        ---------------
        Modifies self.complete_data by appending complete flattened records when
        appropriate recursion levels are reached.

        Examples:
        ---------
        >>> flattener = FlattenJson()
        >>> flattener.flatten_json({'a': 1, 'b': {'c': 2}})
        >>> flattened_dict = flattener.complete_data
        >>> print(flattened_dict)
        {'a': 1, 'b.c': 2}

        Notes:
        ------
        - Uses depth-first traversal with special handling for lists
        - Prevents duplicate records using saved_above tracking
        - Empty lists and dicts may result in empty records being added
        - Primitive values in lists create individual records with list context
        """
        saved_above = False
        saved_data = False
        already_incremented_key_counter = False
        first_iteration = False
        if column_data is None:
            column_data = {}
            self.complete_data = []
            key_counter = {}
            first_iteration = True

        if isinstance(data, list):
            for row in data:
                if isinstance(row, (dict, list)):
                    result, saved_above, temp_key_counter = self.flatten_json(row, column_data=column_data.copy(), value_name=value_name, key_counter=key_counter.copy())
                    if result and not saved_above:
                        self.complete_data.append(result)
                        saved_data = True
                else:
                    temp_value_name = value_name

                    if value_name in key_counter:
                        if not already_incremented_key_counter:
                            key_counter[value_name] += 1
                        if key_counter[value_name] != 0:
                            temp_value_name = f"{value_name}_{key_counter[value_name]}"
                    else:
                        key_counter[value_name] = 0
                    already_incremented_key_counter = True

                    column_data[temp_value_name] = row
                    if column_data:
                        self.complete_data.append(column_data.copy())
                        saved_data = True
            if saved_data:
                saved_above = True

        elif isinstance(data, dict):
            if value_name:
                temp_value_name = f"{value_name}."
            else:
                temp_value_name = ""
            # Ensures simple results are unpacked first and list items are unpacked last
            for key, value in data.items():
                if not isinstance(value, dict) and not isinstance(value, list):
                    current_key_name = f"{temp_value_name}{key}"
                    temp_key_name = current_key_name
                    if current_key_name in key_counter:
                        if not already_incremented_key_counter:
                            key_counter[current_key_name] += 1
                        if key_counter[current_key_name] != 0:
                            temp_key_name = f"{current_key_name}_{key_counter[current_key_name]}"
                    else:
                        key_counter[f"{temp_value_name}{key}"] = 0
                    already_incremented_key_counter = True
                    column_data[temp_key_name] = value

            for key, value in data.items():
                if isinstance(value, dict):
                    temporary_column_data, saved_above, temp_key_counter = self.flatten_json(value, column_data=column_data.copy(), value_name=f"{temp_value_name}{key}", key_counter=key_counter.copy())
                    if temporary_column_data:
                        key_counter = temp_key_counter
                        column_data = temporary_column_data
            for key, value in data.items():
                if isinstance(value, list):
                    temporary_column_data, saved_above, temp_key_counter = self.flatten_json(value, column_data=column_data.copy(), value_name=f"{temp_value_name}{key}", key_counter=key_counter.copy())
                    if temporary_column_data:
                        key_counter = temp_key_counter
                        column_data = temporary_column_data
            if first_iteration and not self.complete_data and column_data:
                self.complete_data.append(column_data)
            return column_data, saved_above, key_counter
        else:
            temp_value_name = value_name
            if value_name in key_counter:
                temp_value_name = f"{value_name}_{key_counter[value_name]}"
                key_counter[value_name] += 1
            else:
                key_counter[value_name] = 1
            column_data[temp_value_name] = data
            if first_iteration and not self.complete_data and column_data:
                self.complete_data.append(column_data)
            return column_data, saved_above, key_counter

        if first_iteration and not self.complete_data and column_data:
            self.complete_data.append(column_data)

        return {}, saved_above, {}


def to_dataframe(data):
    """
    Convert JSON data to a pandas DataFrame with flattened structure.

    This is a convenience function that combines flattening and DataFrame conversion.

    Parameters:
    -----------
    data : any
        JSON data to flatten and convert to DataFrame

    Returns:
    --------
    pandas.DataFrame
        DataFrame with flattened JSON structure where nested keys are
        represented as dot-separated column names

    Raises:
    -------
    ImportError
        If pandas is not installed

    Examples:
    ---------
    >>> data_frame = to_dataframe({'a': 1, 'b': {'c': 2}})
    >>> print(data_frame.shape)
    (1, 2)
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas required: pip install pandas")
    df = pd.DataFrame(flatten(data))
    return df


def flatten(data):
    """
    Flatten JSON data and return as list of dictionaries.

    This is the main entry point for most users who want flattened data
    without DataFrame conversion.

    Parameters:
    -----------
    data : any
        JSON data to flatten

    Returns:
    --------
    list of dict
        Flattened data where nested structures are converted to dot-separated keys

    Examples:
    ---------
    >>> json_data = flatten({'a': 1, 'b': {'c': 2}})
    >>> print(json_data)
    [{'a': 1, 'b.c': 2}]
    """
    flattener = FlattenJson()
    flattener.flatten_json(data)
    return flattener.complete_data