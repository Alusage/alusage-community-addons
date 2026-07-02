from odoo import _, fields, models
from odoo.exceptions import UserError


class Partner(models.Model):
    _inherit = "res.partner"

    rocketchat_users = fields.One2many(
        "rocketchat.user", "partner_id", string=_("Rocketchat Users")
    )

    def send_rc_direct_message(self):
        rocket = self.env.user._connect()
        if self.rocketchat_users:
            if len(self.rocketchat_users) > 1:
                # TODO: create a wizard to select the rocketchat_user the user wants to discuss with
                # For now, only consider the first user of the list
                rc_user = self.rocketchat_users[0]
            else:
                rc_user = self.rocketchat_users[0]
            res = rocket.im_create(rc_user.username).json()
            room = res.get("room", False)
            if room:
                room_id = room.get("rid", False)
                if room_id:
                    url = self.env.user.rc_server.server_url + "/direct/" + room_id
                    return {
                        "type": "ir.actions.act_url",
                        "target": "blank",
                        "url": url,
                    }
        else:
            raise UserError(
                _(
                    "This contact has no Rocketchat user attached.\nPlease contact him by an other way or contact your administrator."
                )
            )

    def link_partner(self):
        return {
            "name": "Link to rocketchat user",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "rocketchat.link.partner.wizard",
            "context": {"default_partner_id": self.id},
            "target": "new",
        }
