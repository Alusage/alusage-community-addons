from rocketchat_API.rocketchat import RocketChat

from odoo import _, fields, models
from odoo.exceptions import UserError


class Users(models.Model):
    _inherit = "res.users"

    rc_server = fields.Many2one("rocketchat.server", string="Rocketchat server")
    rc_login = fields.Char(string=_("Login"))
    rc_password = fields.Char(string=_("Password"))

    def _connect(self):
        if not self.rc_login:
            raise UserError(_("RocketChat login for user %s is not set.", self.name))
        if not self.rc_password:
            raise UserError(_("RocketChat password for user %s is not set.", self.name))
        if not self.rc_server:
            raise UserError(_("RocketChat Server for user %s is not set.", self.name))
        rocket = RocketChat(
            # Connection with Odoo user's rocketchat credentials
            self.rc_login,
            self.rc_password,
            server_url=self.rc_server.server_url,
        )
        return rocket
