# Copyright 2023 Alusage SAS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import logging
from odoo import api, models

_logger = logging.getLogger(__name__)


class PortalWizard(models.TransientModel):
    _inherit = "portal.wizard"


    def action_apply_and_force(self):
        self.ensure_one()
        self.user_ids.write({'in_portal': True})
        self.user_ids.action_apply()
        return {'type': 'ir.actions.act_window_close'}
