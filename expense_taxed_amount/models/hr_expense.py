import base64
import re
import logging

from odoo import _, api, fields, models
from odoo.tools import email_split, float_is_zero

_logger = logging.getLogger(__name__)


class HrExpense(models.Model):
    _inherit = "hr.expense"

    taxed_amount = fields.Monetary(
        "Taxed amount",
        digits="Product Price",
        currency_field="currency_id",
    )

    @api.model
    def _parse_analytic_account(self, expense_description):
        """
        Parse the subject to find the analytic account.
        Product code should be the first word of expense_description
        Return product.product and updated description
        """
        analytic_account_code = expense_description.split(" ")[0]
        analytic_account = self.env["account.analytic.account"].search(
            [("code", "=ilike", analytic_account_code)], limit=1
        )
        if analytic_account:
            expense_description = expense_description.replace(
                analytic_account_code, "", 1
            )

        return analytic_account, expense_description

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        email_address = email_split(msg_dict.get("email_from", False))[0]
        vals = {}
        employee = self.env["hr.employee"].search(
            [
                "|",
                ("work_email", "ilike", email_address),
                ("user_id.email", "ilike", email_address),
            ],
            limit=1,
        )

        expense_description = msg_dict.get("subject", "")

        if employee.user_id:
            company = employee.user_id.company_id
            currencies = company.currency_id | employee.user_id.company_ids.mapped(
                "currency_id"
            )
        else:
            company = employee.company_id
            currencies = company.currency_id

        if not company:  # ultimate fallback, since company_id is required on expense
            company = self.env.company

        # The expenses alias is the same for all companies, we need to set the proper context
        # To select the product account
        self = self.with_company(company)
        # Add . or , to the amount detection
        m = re.match(
            "^\s*(?P<aa>[A-Za-z]{1,2})\s+(?P<ttc>[0-9]+(,[0-9]+)?)\s+[Hh][Tt](?P<ht>[0-9]+(,[0-9]+)?)\s+(?P<libelle>.*)$",
            expense_description,
        )
        product, expense_description = self._parse_product(expense_description)
        _logger.debug("produit: %s" % product)

        if not product:
            # If no product found, select default one.
            product = self.env["product.product"].search(
                [("can_be_expensed", "=", True)], limit=1
            )
            _logger.debug("produit2: %s" % product)
        if m:
            data = m.groupdict()
            analytic_account = self.env["account.analytic.account"].search(
                [("code", "=ilike", data["aa"].upper())], limit=1
            )
            vals = {
                "employee_id": employee.id,
                "name": data["libelle"],
                "unit_amount": data["ttc"].replace(",", "."),
                "product_id": product.id if product else None,
                "product_uom_id": product.uom_id.id,
                "tax_ids": [
                    (4, tax.id, False)
                    for tax in product.supplier_taxes_id.filtered(
                        lambda r: r.company_id == company
                    )
                ],
                "quantity": 1,
                "taxed_amount": data["ht"].replace(",", "."),
                "company_id": company.id,
                "currency_id": currencies.id,
                "analytic_account_id": analytic_account.id,
            }

        expense = super(HrExpense, self).message_new(
            msg_dict, dict(custom_values or {}, **vals)
        )

        account = product.product_tmpl_id._get_product_accounts()["expense"]
        vals["account_id"] = account.id
        vals["product_id"] = product.id if product else None
        vals["product_uom_id"] = product.uom_id.id
        if vals:
            expense.write(vals)

        return expense
