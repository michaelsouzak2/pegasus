from copernicus_api_client import get_bounding_boxes
from copernicus_map_generator import generate_map


def main():
    products = get_bounding_boxes()
    generate_map(products)  


if __name__ == "__main__":
    main()