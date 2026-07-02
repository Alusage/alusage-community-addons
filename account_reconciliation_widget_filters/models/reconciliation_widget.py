import logging

from odoo import api, fields, models, _
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class AccountReconciliation(models.AbstractModel):
    _inherit = "account.reconciliation.widget"


    @api.model
    def _domain_move_lines_for_reconciliation(
        self,
        st_line,
        aml_accounts,
        partner_id,
        excluded_ids=None,
        search_str=False,
        mode="rp",
    ):
        domain = super(AccountReconciliation, self)._domain_move_lines_for_reconciliation(
            st_line=st_line,
            aml_accounts=aml_accounts,
            partner_id=partner_id,
            excluded_ids=excluded_ids,
            search_str=search_str,
            mode=mode,
        )
        domain = expression.AND([domain, [("account_id.exclude_from_bank_reconcile", "!=", True)]])
        return domain