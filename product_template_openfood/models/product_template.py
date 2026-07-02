from odoo import models, fields, api
import requests
import base64
import openfoodfacts
from ast import literal_eval
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def get_openfood_img(self):
        for product in self:
            url = False
            img = False
            if product.barcode:
                _logger.debug("OpenFood BARCODE %s" % product.barcode)
                openfood_product = openfoodfacts.get_product(self.barcode)
                if openfood_product['status_verbose'] != 'product not found':
                    url = openfood_product["product"].get("image_front_url", False)
                if url:
                    _logger.debug("OpenFood URL %s" % url)
                    response = requests.get(url)
                    if response.ok and response.content : 
                        img = base64.b64encode(response.content)
                    else :
                        img = False
                product.image = img