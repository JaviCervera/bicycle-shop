"""
Marcus Sports Equipment Store - Main program
============================================

App usage:
To run the application as a monolith (with the backend embedded in the app),
just run:

$ python3 main.py

To run with a split backend / frontend architecture, first start the server by running:

$ python3 server.py

And then, on a separate terminal session, do:

$ python3 main.py --url http://localhost:8080

"""

from cli_app import create_catalog, display_order_summary, print_welcome_message, \
    select_options, select_product, server_url


def main() -> None:
    # Uncomment the following lines to enable logging to stdout
    # import logging
    # logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    url = server_url()
    print_welcome_message(url)
    with create_catalog(url) as catalog:
        product = select_product(catalog.products())
        parts = catalog.product_parts(product.id)
        options = select_options(parts, catalog.part_options)
        display_order_summary(
            product,
            parts,
            options,
            catalog.part_options_price(options))

if __name__ == '__main__':
    main()
