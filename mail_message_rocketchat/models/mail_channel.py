import logging
from markdownify import markdownify as md

from odoo import fields, models


_logger = logging.getLogger(__name__)


class MailChannel(models.Model):
    _inherit = "mail.channel"

    rocketchat_chan = fields.Many2one("rocketchat.channel", string="Canal Principal")

    def action_test_channel(self):
        rocket = self.rocketchat_chan.server_id._connect()
        res = rocket.chat_post_message(
            "Odoobot is here!", channel=self.rocketchat_chan.channel_id
        ).json()
        return res

    def _build_message_to_post(self, notification,notification_model, notification_record):
        """Build the content of the message sent in Rocketchat channel.
        Te be inherited to modify the message content
        """
        message_to_post = notification[1].get("body", False)
        author_id = notification[1].get("author_id", False)
        tracking_fields = notification[1].get("tracking_value_ids")
        subtype_id = notification[1].get("subtype_id")
        if message_to_post:
            message_to_post = "[%s] -> %s" % (
                author_id[1] if author_id else "",
                md(
                    message_to_post,
                    convert=["b", "i", "p", "a"],
                    heading_style="ATX",
                ),
            )
        elif tracking_fields:
            message_to_post = "[%s] ☑ **%s**:\n" % (
                notification_model,
                notification_record.name,
            )
            for field in tracking_fields:
                message_to_post += "%s : %s -> %s\n" % (
                    field.get("changed_field", ""),
                    field.get("old_value", ""),
                    field.get("new_value", ""),
                )
        elif subtype_id:
            message_to_post = "[%s] ☑ **%s**:\n %s\n" % (
                notification_model,
                notification_record.name,
                subtype_id[1],
            )
        if message_to_post:
            message_to_post += "**📫 Send from Odoo notification**: %s/mail/view?model=%s&res_id=%s" % (
                self.env["ir.config_parameter"].sudo().get_param("web.base.url"),
                notification[1].get("model"),
                notification[1].get("res_id"),
            )
        return message_to_post

    def _channel_message_notifications(self, message, message_format):
        """Generate the bus notifications for the given message
        :param message : the mail.message to sent
        :returns list of bus notifications (tuple (bus_channe, message_content))

        notification: ['7a8e39d9-2439-4575-a0f7-cd6bd49f6cac',
                       {
                          'id': 27,
                          'body': '',
                          'date': datetime.datetime(2022, 6, 27, 17, 7, 55),
                          'author_id': (3, 'Administrator'),
                          'email_from': '"Administrator" <admin@example.com>',
                          'message_type': 'notification',
                          'subtype_id': (24, 'Tâche créée'),
                          'subject': False,
                          'model': 'project.task',
                          'res_id': 13,
                          'record_name': 'test rocket1',
                          'channel_ids': [4],
                          'partner_ids': [],
                          'starred_partner_ids': [],
                          'moderation_status': False,
                          'customer_email_status': 'sent',
                          'customer_email_data': [],
                          'attachment_ids': [],
                          'tracking_value_ids': [{'id': 79,
                                                  'changed_field': 'Titre',
                                                  'old_value': False,
                                                  'new_value':
                                                  'test rocket1',
                                                  'field_type': 'char'},
                                                 {'id': 80,
                                                  'changed_field': 'Étape',
                                                  'old_value': '', 'new_value':
                                                  'test', 'field_type': 'many2one'},
                                                 {'id': 81,
                                                  'changed_field': "Étiquette d'état Kanban",
                                                  'old_value': False,
                                                  'new_value': 'En cours',
                                                  'field_type': 'char'},
                                                 {'id': 82,
                                                  'changed_field': 'Projet',
                                                  'old_value': '',
                                                  'new_value': 'TEST',
                                                  'field_type': 'many2one'},
                                                 {'id': 83,
                                                  'changed_field':'Assigné à',
                                                  'old_value': '',
                                                  'new_value': 'Administrator',
                                                  'field_type': 'many2one'},
                                                 {'id': 84,
                                                  'changed_field': 'Responsable',
                                                  'old_value': '',
                                                  'new_value': 'Administrator',
                                                  'field_type': 'many2one'}],
                          'needaction_partner_ids': [],
                          'is_note': False,
                          'is_discussion': False,
                          'is_notification': False,
                          'subtype_description': 'Tâche créée',
                          'module_icon': '/project/static/description/icon.png'}]



        """
        notifications = super(MailChannel, self)._channel_message_notifications(
            message=message, message_format=message_format
        )

        for notification in notifications:
            notification_model = notification[1].get("model")
            notification_res_id = notification[1].get("res_id")
            notification_record = self.env[notification_model].search(
                [("id", "=", int(notification_res_id))], limit=1
            )

            rocketchat_chan = False
            message_to_post = False
            if notification[0][1]:
                # if mail.channel notification notification[0] is like ('dbname', 'mail.channel', channel_id)
                rocketchat_chans = self.env["mail.channel"].search(
                    [
                        ("id", "=", notification[0][2]),
                        ("rocketchat_chan", "!=", False),
                    ],
                )
                for rocketchat_chan in rocketchat_chans.mapped("rocketchat_chan"):
                    if rocketchat_chan.server_id.enable_rocketchat_notification:
                        rocket = rocketchat_chan.server_id._connect()
                        message_to_post = self._build_message_to_post(notification, notification_model, notification_record)

                        if message_to_post:
                            if notification_record.rocketchat_thread:
                                if notification_record.tmid:
                                    message = rocket.chat_post_message(
                                        message_to_post,
                                        channel=rocketchat_chan.channel_id,
                                        tmid=notification_record.tmid,
                                        tshow=notification_record.tshow,
                                        thread_id=notification_record.rocketchat_thread,
                                    ).json()
                                else:
                                    message = rocket.chat_post_message(
                                        message_to_post,
                                        channel=rocketchat_chan.channel_id,
                                        thread_id=notification_record.rocketchat_thread,
                                    ).json()
                                    _logger.debug(
                                        "ROCKET: tmid %s" % message["message"]
                                    )
                                    notification_record.write(
                                        {"tmid": message["message"].get("_id")}
                                    )
                            else:
                                message = rocket.chat_post_message(
                                    message_to_post,
                                    channel=rocketchat_chan.channel_id,
                                ).json()

        return notifications
