jsonxplode
Efficient JSON flattening for complex nested structures

Python 3.6+ | MIT License | Zero Dependencies

jsonxplode converts nested JSON structures into flat tabular format while preserving all data, including complex nested arrays and objects with arbitrary depth.

Installation
BASH
pip install jsonxplode
Usage
PYTHON
from jsonxplode import flatten

# Handles any JSON structure
data = {
    "users": [
        {"profile": {"name": "John", "settings": {"theme": "dark"}}},
        {"profile": {"name": "Jane", "settings": {"theme": "light"}}}
    ]
}

flattened_data = flatten(data)
# Returns: [{'users.profile.name': 'John', 'users.profile.settings.theme': 'dark'}, 
#           {'users.profile.name': 'Jane', 'users.profile.settings.theme': 'light'}]
Optional: DataFrame Output
PYTHON
from jsonxplode import to_dataframe

# Requires pandas to be installed separately
df = to_dataframe(data)
Note: to_dataframe requires pandas (pip install pandas) but the core flatten function has zero dependencies.

Features
Arbitrary nesting depth - handles deeply nested objects and arrays
Conflict resolution - automatically manages key path conflicts
Memory efficient - processes large datasets with minimal overhead
Zero dependencies - pure Python implementation (core function)
Array expansion - properly handles nested arrays with row duplication
Performance
7,900 rows with 23 column processed in 0.146 seconds
Memory usage: ~46MB for previously mentioned workload
