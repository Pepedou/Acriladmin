from inventories.models import Product


class ScrapsToProductsConverter:
    """
    Converts a Product's scraps after a subproduct has been
    created from it into new, smaller Products.
    """

    def __init__(self, subproduct_length, subproduct_width, subproduct_thickness, product: Product):
        self.subproduct_length = subproduct_length
        self.subproduct_width = subproduct_width
        self.subproduct_thickness = subproduct_thickness
        self.product = product

    def get_products_params_from_scraps(self):
        """
        Returns a list of dictionaries with Product parameters
        generated from the given scraps.
        :return: A list of dictionaries.
        """
        products = []
        scraps_measurements = self._get_scraps_measurements()

        for measurement in scraps_measurements:
            products.append({
                'sku': self.product.sku + "_{0}*{1}*{2}PED".format(measurement['width'], measurement['length'],
                                                                   self.subproduct_thickness),
                'description': self.product.description + " [PEDACERÍA]",
                'search_description': self.product.search_description + " [PEDACERÍA]",
                'line': self.product.line,
                'engraving': self.product.engraving,
                'color': self.product.color,
                'length': measurement['length'],
                'width': measurement['width'],
                'thickness': self.subproduct_thickness,
                'is_composite': self.product.is_composite,
            })

        return products

    def _get_scraps_measurements(self):
        """
        Returns a list of dictionaries with the lengths and widths
        of the scraps. For reference on how this works, see
        docs/Scraps products calculation.peg.
        :return: A list of dictionaries.
        """
        original_length = self.product.length
        original_width = self.product.width

        remaining_length = original_length - self.subproduct_length
        remaining_width = original_width - self.subproduct_width

        scraps = []

        if remaining_width > 0:
            scraps.append({
                'length': original_length if original_length >= remaining_width else remaining_width,
                'width': remaining_width if remaining_width < original_length else original_length
            })

        if remaining_length > 0:
            scraps.append({
                'length': remaining_length if remaining_length >= self.subproduct_width else self.subproduct_width,
                'width': self.subproduct_width if self.subproduct_width < remaining_length else remaining_length
            })

        return scraps
