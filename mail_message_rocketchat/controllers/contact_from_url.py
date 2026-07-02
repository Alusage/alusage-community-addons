import logging
import werkzeug

from odoo import http
from odoo.http import request


class SendMessageFromURL(http.Controller):
    @http.route(
        "/partner/<partner_id>/send_rockechat_direct_message",
        type="http",
        csrf=False,
        auth="user",
        website=True,
    )
    def send_rockechat_direct_message(self, partner_id):
        if not request.session.uid:
            return werkzeug.utils.redirect(
                "/web/login?redirect=/partner/%s/send_rockechat_direct_message"
                % int(partner_id),
                303,
            )
        partner = request.env["res.partner"].browse(int(partner_id))
        return request.redirect(partner.send_rc_direct_message()["url"])
