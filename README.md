<h1 align="center">jsonxplode</h1>
<h3 align="center">Efficient JSON flattening for complex nested structures</h3>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="Python Version" height="40rem">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" height="40rem">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen.svg" alt="Dependencies" height="40rem">
</p>

<p align="center">
  jsonxplode converts nested JSON structures into flat tabular format while preserving all data, including complex nested arrays and objects with arbitrary depth.
</p>

<h2>Version Update: v1.1.0</h2>

<h3>Bug fix</h3>

<p><strong>Relational Array Flattening</strong> - Arrays of the same length are now flattened relationally by default, preserving positional relationships:</p>

<h2>Control Relational Array Flattening</h2>

<p>Control how arrays are flattened with the <code>relational_array</code> parameter:</p>

<pre><code class="language-python"># Default - preserves relationships between arrays
flattener = FlattenJson(relational_array=True)

# Independent flattening of arrays  
flattener = FlattenJson(relational_array=False)</code></pre>

<h3>Example with Relational Flattening (Default)</h3>

<pre><code class="language-python">data = {
    "name": "John",
    "a": [1, 2, 3],
    "b": [1, 2, 3]
}
result = flattener.flatten(data)</code></pre>

<p>Returns:</p>
<pre><code class="language-python">[
    {"name": "John", "a": 1, "b": 1},
    {"name": "John", "a": 2, "b": 2},
    {"name": "John", "a": 3, "b": 3}
]</code></pre>

<h2>Installation</h2>

<pre><code class="language-bash">pip install jsonxplode</code></pre>

<h2>Usage</h2>

<pre><code class="language-python">from jsonxplode import flatten

# Handles any JSON structure
data = {
    "users": [
        {"profile": {"name": "John", "settings": {"theme": "dark"}, "location": ["city1", "city2"]}},
        {"profile": {"name": "Jane", "settings": {"theme": "light"}}}
    ]
}

flattened_data = flatten(data)</code></pre>

<p>Returns:</p>
<pre><code class="language-python">[
    {'users.profile.name': 'John', 'users.profile.settings.theme': 'dark', 'user.profile.location': 'city1'},
    {'users.profile.name': 'John', 'users.profile.settings.theme': 'dark', 'user.profile.location': 'city2'},
    {'users.profile.name': 'Jane', 'users.profile.settings.theme': 'light'}
]</code></pre>

<h2>DataFrame Output (Optional)</h2>

<pre><code class="language-python">from jsonxplode import to_dataframe

# Requires pandas to be installed separately
df = to_dataframe(data)</code></pre>

<p><strong>Note:</strong> <code>to_dataframe</code> requires pandas (<code>pip install pandas</code>) but the core <code>flatten</code> function has zero dependencies.</p>

<h2>Features</h2>

<ul>
<li><strong>Arbitrary nesting depth</strong> - handles deeply nested objects and arrays</li>
<li><strong>Conflict resolution</strong> - automatically manages key path conflicts</li>
<li><strong>Memory efficient</strong> - processes large datasets with minimal overhead</li>
<li><strong>Zero dependencies</strong> - pure Python implementation (core function)</li>
<li><strong>Array expansion</strong> - properly handles nested arrays with row duplication</li>
</ul>

<h2>Performance</h2>

<ul>
<li>7,900 rows with 23 columns processed in 0.146 seconds</li>
<li>Memory usage: ~16MB for above mentioned workload</li>
<li>Consistent performance across varying data structures</li>
</ul>
