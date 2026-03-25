# run.py
import sys
import os

# Add project root to Python path (so `import app` works)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == "__main__":
    app.run(debug=True)