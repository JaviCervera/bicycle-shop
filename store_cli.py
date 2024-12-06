from cli_app import create_app, display_order_summary, print_welcome_message, \
    select_options, select_product, server_url


def main() -> None:
    # Uncomment the following lines to enable logging to stdout
    # import logging
    # logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    url = server_url()
    print_welcome_message(url)
    with create_app(url) as app:
        product = select_product(app.products())
        parts = app.product_parts(product.id)
        options = select_options(parts, app.part_options)
        display_order_summary(
            product,
            parts,
            options,
            app.part_options_price(options))

if __name__ == '__main__':
    main()
