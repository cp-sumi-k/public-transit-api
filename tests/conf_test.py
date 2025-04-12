import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_path = os.path.join(project_root, 'app')

sys.path.insert(0, app_path)
