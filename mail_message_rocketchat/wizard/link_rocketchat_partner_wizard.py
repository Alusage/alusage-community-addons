from odoo import models, fields


class RocketChatLinkWizard(models.TransientModel):
    _name = "rocketchat.link.partner.wizard"
    _description = "Link to partner"

    server_id = fields.Many2one("rocketchat.server", string="Server")
    rocket_user_id = fields.Many2one(
        "rocketchat.user", string="User", domain='[("partner_id", "=", False)]'
    )
    partner_id = fields.Many2one("res.partner", string="Partner")

    def action_link(self):
        self.rocket_user_id.write({"partner_id": self.partner_id})
        return {"type": "ir.actions.act_window_close"}
