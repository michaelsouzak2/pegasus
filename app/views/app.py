from app.services.copernicus_service import get_bounding_boxes
from app.services.map_generator_service import generate_map


def main():
    products = get_bounding_boxes()
    generate_map(products)  


if __name__ == "__main__":
    main()