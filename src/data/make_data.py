from src.data.get_raw import get_raw
from src.data.get_external import get_external
from src.data.get_interim import get_interim


if __name__ == "__main__":
    # Download raw datasets
    get_raw()
    # Download external datasets
    get_external()
    # Create interim's datasets
    get_interim()
    # Create external's datasets
    get_external()
