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

        (
            product,
            analytic_account,
            price,
            priceht,
            currency_id,
            expense_description,
        ) = self._parse_expense_subject_ht(expense_description, currencies)

        vals = {
            "employee_id": employee.id,
            "name": expense_description,
            "unit_amount": price,
            "product_id": product.id if product else None,
            "product_uom_id": product.uom_id.id,
            "tax_ids": [
                (4, tax.id, False)
                for tax in product.supplier_taxes_id.filtered(
                    lambda r: r.company_id == company
                )
            ],
            "quantity": 1,
            "taxed_amount": priceht,
            "company_id": company.id,
            "currency_id": currency_id.id,
            "analytic_account_id": analytic_account.id,
        }

        account = product.product_tmpl_id._get_product_accounts()["expense"]
        if account:
            vals["account_id"] = account.id

        expense = super(HrExpense, self).message_new(
            msg_dict, dict(custom_values or {}, **vals)
        )
        expense.write(
            {
                "name": expense_description,
            }
        )
        return expense

    @api.model
    def _parse_expense_subject_ht(self, expense_description, currencies):
        """Fetch product, price and currency info from mail subject.
        Product can be identified based on product name or product code.
        It can be passed between [] or it can be placed at start.
        When parsing, only consider currencies passed as parameter.
        This will fetch currency in symbol($) or ISO name (USD).
        Some valid examples:
            Travel by Air [TICKET] USD 1205.91
            TICKET $1205.91 Travel by Air
            Extra expenses 29.10EUR [EXTRA]
        """
        analytic_account, expense_description = self._parse_analytic_account(
            expense_description
        )
        product, expense_description = self._parse_product(expense_description)
        priceht, expense_description = self._parse_price_ht(
            expense_description, currencies
        )
        price, currency_id, expense_description = self._parse_price(
            expense_description, currencies
        )
        return (
            product,
            analytic_account,
            price,
            priceht,
            currency_id,
            expense_description,
        )

    @api.model
    def _parse_price_ht(self, expense_description, currencies):
        """Return price, currency and updated description"""
        symbols, symbols_pattern, float_pattern = [], "", "[+-]?(\d+[.,]?\d*)"
        price = 0.0
        for currency in currencies:
            symbols.append(re.escape("HT"))
        symbols_pattern = "|".join(symbols)
        price_pattern = "((%s)?\s?%s\s?(%s)?)" % (
            symbols_pattern,
            float_pattern,
            symbols_pattern,
        )
        matches = re.findall(price_pattern, expense_description)
        if matches:
            match = max(
                matches, key=lambda match: len([group for group in match if group])
            )  # get the longuest match. e.g. "2 chairs 120$" -> the price is 120$, not 2
            full_str = match[0]
            price = match[2].replace(",", ".")
            expense_description = expense_description.replace(
                full_str, " "
            )  # remove price from description
            expense_description = re.sub(" +", " ", expense_description.strip())

        price = float(price)
        return price, expense_description
