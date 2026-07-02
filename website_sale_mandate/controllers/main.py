# -*- coding: utf-8 -*-
import json
import logging

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import WebsiteSaleForm
from odoo.addons.base_iban.models.res_partner_bank import validate_iban

_logger = logging.getLogger(__name__)

class WebsiteSaleCustom(WebsiteSale):
    @http.route(['/shop/extra_info'], type='http', auth="public", website=True, sitemap=False)
    def extra_info(self, **post):
        """ On extra info step, if SEPA mandate already exists, pass this step, and go directly to payment
        """
        order = request.website.sale_get_order()
        mandate_obj = request.env["account.banking.mandate"]
        mandate = mandate_obj.sudo().search(
                [
                    ("partner_id", "=", order.partner_id.id),
                    ("state", "=", "valid"),
                ]
            )
        if mandate:
            return request.redirect("/shop/payment")
        else:
            return super(WebsiteSaleCustom,self).extra_info(**post)
        

class WebsiteSaleFormCustom(WebsiteSaleForm):
    @http.route(
        "/website_form/shop.sale.order",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def website_form_saleorder(self, **kwargs):
        error = {}
        error_message = []
        custom_data = {}
        # TODO: properly inherit with super()
        # response = super(WebsiteSaleFormCustom, self).website_form_saleorder(**post)
        model_record = request.env.ref("sale.model_sale_order")
        # TODO: test iban number
        try:
            data = self.extract_data(model_record, kwargs)
        except ValidationError as e:
            return json.dumps({"error_fields": e.args[0]})

        for keys in data["custom"].split("\n"):
            value, value_data = keys.split(":")
            custom_data[value.strip()] = value_data.strip()

        order = request.website.sale_get_order()
        if data["record"]:
            order.write(data["record"])

        if custom_data:
            if custom_data.get('iban', False):
                try:
                    validate_iban(custom_data['iban'])
                except ValidationError as e:
                    values = kwargs
                    error_message.append(e.args[0])
                    error["iban"] = 'error'
                    render_values = {
                        'website_sale_order': order,
                        'checkout': values,
                        'error': error,
                        'callback': kwargs.get('callback'),
                        'only_services': order and order.only_services,
                        "error_message": error_message
                    }
                    _logger.debug('iban error: %s' % custom_data['iban'])
                    #return request.render("website_sale.extra_info", render_values)
                    # return json.dumps(render_values)
                    #return request.redirect("/shop/extra_info", render_values)
                custom_data['authorize_iban_direct_debit'] = True
            order.write(custom_data)

        if data["custom"]:
            values = {
                "body": nl2br(data["custom"]),
                "model": "sale.order",
                "message_type": "comment",
                "no_auto_thread": False,
                "res_id": order.id,
            }
            request.env["mail.message"].sudo().create(values)

        if data["attachments"]:
            self.insert_attachment(model_record, order.id, data["attachments"])

        return json.dumps({"id": order.id})
