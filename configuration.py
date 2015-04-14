# Contains all environment configurations.
import jinja2
import os
import filters

from types import FunctionType

jinja_env = jinja2.Environment(
    autoescape=True,
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')
    )
)

# Auto imports all functions in filters.py to be jinja filters
for func_name in dir(filters):
  func = getattr(filters, func_name, None)
  if isinstance(func, FunctionType):
    jinja_env.filters[func_name] = func
