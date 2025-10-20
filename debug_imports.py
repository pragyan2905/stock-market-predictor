import sys
from pathlib import Path
import os

print("--- Python Path Information ---")
print(f"Current Python Executable: {sys.executable}")
print("\nsys.path contents:")
for p in sys.path:
    print(p)
print("-----------------------------\n")

print("--- Project Structure Check ---")
project_root = Path(__file__).resolve().parent
src_path = project_root / 'src'
package_path = src_path / 'stock_market_predictor'
components_path = package_path / 'components'
data_ingestion_path = components_path / 'data_ingestion.py'

print(f"Project Root exists: {project_root.exists()}")
print(f"Src Path exists: {src_path.exists()}")
print(f"Package Path exists: {package_path.exists()}")
print(f"Components Path exists: {components_path.exists()}")
print(f"Data Ingestion Script exists: {data_ingestion_path.exists()}")
print("-----------------------------\n")

print("--- Attempting Import ---")
# Manually add the src path
sys.path.insert(0, str(src_path))
print(f"Added '{src_path}' to sys.path")

try:
    from stock_market_predictor.components.data_ingestion import DataIngestion
    print("\nSUCCESS: 'DataIngestion' was imported successfully!")
except ImportError as e:
    print(f"\nFAILURE: The import failed with the following error:")
    print(e)
