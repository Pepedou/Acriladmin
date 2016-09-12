from decimal import Decimal

from django.template.loader_tags import register

from inventories.models import ProductInventoryItem


@register.filter
def subtract(value, arg):
    return value - arg


class Surface:
    """
    Represents the surface of an object.
    """
    STANDARDS = [
        {'width': 1, 'length': 12},
        {'width': 0.6, 'length': 1},
        {'width': 8, 'length': 13},
    ]

    @property
    def area(self):
        return self.width * self.length

    def __init__(self, width=0.0, length=0.0):
        self.width = Decimal(width)
        self.length = Decimal(length)

    def __str__(self):
        return "{:.2f} X {:.2f}".format(self.width, self.length)

    def get_closest_standard(self):
        """
        Returns the Surface Area Standard that is closest to this
        Surface Area.
        :return: A dictionary with the standard and the sum of the
        difference between this area and the standard.
        """
        deltas_to_standards = []

        for standard_dict in Surface.STANDARDS:
            standard = Surface(width=standard_dict['width'], length=standard_dict['length'])
            delta_width = standard.width - self.width
            delta_length = standard.length - self.length

            if delta_width < 0 or delta_length < 0:
                continue

            deltas_sum = delta_width + delta_length

            deltas_to_standards.append(
                {
                    'standard': standard,
                    'deltas_sum': deltas_sum,
                }
            )

        return min(deltas_to_standards, key=lambda item: item['deltas_sum'])


class ProductCutOptimizer:
    """
    Optimizes product cuts by obtaining the best suited candidates
    for a specific surface area.
    """

    def __init__(self, inventory, surface_area, product_lines, quantity=1):
        self.surface = Surface(width=surface_area.width, length=surface_area.length)
        self.product_lines = product_lines
        self.quantity = quantity
        self.inventory = inventory
        self.available_inventory_items = None

    def get_candidate_products_for_surface(self):
        """
        Returns an array of dictionaries with the best suited product inventory
        items, the remaining quantities and residues. The best products are
        the ones for which the distance to any one standard is shortest and are
        scrap.
        :return: A list of dictionaries and the amount remaining.
        """
        candidate_products = []

        self.available_inventory_items = ProductInventoryItem.objects.filter(
            product__width__gte=self.surface.width,
            product__length__gte=self.surface.length,
            product__line__in=self.product_lines,
            quantity__gte=1,
            inventory=self.inventory
        )

        if self.available_inventory_items.count() == 0:
            return [], self.quantity

        results = self._get_results()

        remaining = self.quantity

        while remaining > 0:
            try:
                result = results.pop(0)
                min_product = result['product_item']

                if min_product.quantity >= remaining:
                    result['product_remaining'] = min_product.quantity - remaining
                    remaining = 0
                else:
                    result['product_remaining'] = 0
                    remaining -= min_product.quantity

                candidate_products.append(result)
            except IndexError:
                break

        candidate_products.sort(key=lambda x: -x['product_item'].product.is_scrap)

        return candidate_products, remaining

    def _get_results(self):
        """
        Returns a sorted set of product inventory items for which the residue
        to any one standard is shortest.
        :return: List of dictionaries with the product item, closest standard, vertical or horizontal
        configuration and product residue.
        """
        results = []

        for inventory_item in self.available_inventory_items.all():
            vertical_conf_residue = Surface()
            horizontal_conf_residue = Surface()
            product = inventory_item.product

            conf1_delta1 = product.width - self.surface.width
            conf1_delta2 = product.length - self.surface.length

            vertical_conf_residue.width = conf1_delta1 if conf1_delta1 < conf1_delta2 else conf1_delta2
            vertical_conf_residue.length = conf1_delta2 if conf1_delta1 < conf1_delta2 else conf1_delta2

            try:
                vertical_conf_closest_standard = vertical_conf_residue.get_closest_standard()
            except ValueError:
                continue

            conf2_delta1 = product.length - self.surface.width
            conf2_delta2 = product.width - self.surface.length

            horizontal_conf_residue.width = conf2_delta1 if conf2_delta1 < conf2_delta2 else conf2_delta2
            horizontal_conf_residue.length = conf2_delta2 if conf2_delta1 < conf2_delta2 else conf2_delta1

            conf = 'Vertical'
            closest_standard = vertical_conf_closest_standard
            residue = vertical_conf_residue

            if horizontal_conf_residue.width >= 0 and horizontal_conf_residue.length >= 0:
                try:
                    horizontal_conf_closest_standard = horizontal_conf_residue.get_closest_standard()

                    if vertical_conf_closest_standard['deltas_sum'] > horizontal_conf_closest_standard['deltas_sum']:
                        conf = 'Horizontal'
                        closest_standard = horizontal_conf_closest_standard
                        residue = horizontal_conf_residue
                except ValueError:
                    pass

            results.append({
                'product_item': inventory_item,
                'closest_standard': closest_standard,
                'conf': conf,
                'residue': residue
            })

        return sorted(results, key=lambda item: item['closest_standard']['deltas_sum'])
