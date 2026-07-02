import logging
from rocketchat_API.rocketchat import RocketChat

from odoo import fields, models


_logger = logging.getLogger(__name__)


class RocketChatChannel(models.Model):
    _name = "rocketchat.channel"
    _description = "RocketChatChannel"

    name = fields.Char(string="Name")
    active = fields.Boolean(default=True)
    channel_id = fields.Char(string="Channel ID")
    users_count = fields.Integer(string="Nb Users")
    server_id = fields.Many2one("rocketchat.server", string="Server")


class RocketChatUser(models.Model):
    _name = "rocketchat.user"
    _description = "RocketChatUser"

    name = fields.Char(string="Name")
    active = fields.Boolean(default=True)
    username = fields.Char(string="Username")
    user_id = fields.Char(string="User ID")
    server_id = fields.Many2one("rocketchat.server", string="Server")
    partner_id = fields.Many2one("res.partner", string="Linked Contact")


class RocketChatServer(models.Model):
    _name = "rocketchat.server"
    _description = "RochetChat Server"

    name = fields.Char(string="Nom")
    active = fields.Boolean(default=True)
    login = fields.Char(string="Login")
    password = fields.Char(string="Password")
    server_url = fields.Char(string="URL")
    channel_ids = fields.One2many("rocketchat.channel", "server_id", string="Channels")
    user_ids = fields.One2many("rocketchat.user", "server_id", string="Users")
    enable_rocketchat_notification = fields.Boolean(
        "Active notifications on Rocketchat", default=True
    )

    def _connect(self):
        rocket = RocketChat(
            self.login,
            self.password,
            server_url=self.server_url,
        )
        return rocket

    def _fetch_partner(self, rocketchat, rc_user):
        user_info = rocketchat.users_info(rc_user.user_id).json().get("user", False)
        if user_info:
            emails = user_info.get("emails", False)
            if emails:
                for email in emails:
                    address = email.get("address", False)
                    if address:
                        partners = self.env["res.partner"].search(
                            [("email", "=", address)]
                        )
                        if partners and (len(partners) == 1):
                            ## We have a matching partner
                            rc_user.partner_id = partners[0]

    def action_populate(self):
        rocket = self._connect()
        self.action_populate_channels(rocket)
        self.action_populate_users(rocket)
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def action_populate_channels(self, rocketchat):
        for channel in (
            rocketchat.channels_list(count=1000).json().get("channels", False)
        ):
            _logger.debug(channel)
            existing_channel = self.channel_ids.filtered(
                lambda f: f.channel_id == channel["_id"]
            )
            if not existing_channel:
                self.env["rocketchat.channel"].create(
                    {
                        "channel_id": channel["_id"],
                        "name": channel["name"],
                        "server_id": self.id,
                        "users_count": channel["usersCount"],
                    }
                )
            else:
                existing_channel.write(
                    {
                        "name": channel["name"],
                        "users_count": channel["usersCount"],
                    }
                )

    def action_populate_users(self, rocketchat):
        for user in rocketchat.users_list().json().get("users", False):
            existing_user = self.user_ids.filtered(lambda f: f.user_id == user["_id"])
            if not existing_user:
                rc_user = self.env["rocketchat.user"].create(
                    {
                        "user_id": user["_id"],
                        "name": user["name"],
                        "username": user.get("username", ""),
                        "server_id": self.id,
                    }
                )
                self._fetch_partner(rocketchat, rc_user)
            else:
                existing_user.write(
                    {
                        "name": user["name"],
                        "username": user.get("username", ""),
                    }
                )
                self._fetch_partner(rocketchat, existing_user)

    def action_test_channels(self):
        rocket = self._connect()
        for channel in self.channel_ids[0]:
            res = rocket.chat_post_message(
                "Odoobot is here!", channel=channel.channel_id
            ).json()
            _logger.debug("ROCKETCHAT RES (%s): %s" % (channel.channel_id, res))
