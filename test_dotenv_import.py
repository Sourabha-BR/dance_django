import sys
print("--- sys.executable ---")
print(sys.executable)
print("--- sys.path ---")
for p in sys.path:
    print(p)
print("--- Attempting to import dotenv ---")
try:
    import dotenv
    print("--- dotenv imported successfully ---")
    print(f"dotenv version: {dotenv.__version__}")
    print(f"dotenv file location: {dotenv.__file__}")
except ImportError as e:
    print(f"--- Failed to import dotenv ---")
    print(e)
except Exception as e:
    print(f"--- An unexpected error occurred ---")
    print(e)
