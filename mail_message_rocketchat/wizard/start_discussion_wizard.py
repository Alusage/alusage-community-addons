from odoo import _, fields, models
from odoo.exceptions import UserError


class PartnerRCDiscussionWizard(models.TransientModel):
    _name = "partner.rc.discussion.wizard"
    _description = "Create a Rocketchat discussion"

    discussion_name = fields.Char(string="Discussion name", required=True)
    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="rc_discussion_wizard_partner",
        default=lambda self: self.env.context.get("active_ids"),
    )

    def create_open_rc_discussion(self):
        rocket = self.env.user._connect()
        partners = self.partner_ids
        discussion_users = []
        for partner in partners:
            if partner.rocketchat_users:
                if len(partner.rocketchat_users) > 1:
                    # TODO: create a wizard to select the rocketchat_user the user wants to discuss with
                    # For now, only consider the first user of the list
                    rc_user = partner.rocketchat_users[0]
                else:
                    rc_user = partner.rocketchat_users[0]
                discussion_users.append(rc_user.username)

        if len(discussion_users) == 0:
            raise UserError(_("None of selected partners with Rocketchat User"))

        discussion_users.append(self.env.user.rc_login)
        discussion_name = self.discussion_name.title().replace(" ", "")
        group = (
            rocket.groups_create(discussion_name, members=discussion_users)
            .json()
            .get("group", False)
        )
        if group:
            url = self.env.user.rc_server.server_url + "/group/" + group["name"]
            return {
                "type": "ir.actions.act_url",
                "target": "blank",
                "url": url,
            }
        else:
            error = (
                rocket.groups_create(discussion_name, members=discussion_users)
                .json()
                .get("error")
            )
            raise UserError(_(error))
