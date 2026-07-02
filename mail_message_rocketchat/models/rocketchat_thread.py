from odoo import fields, models

class RockchatThread(models.AbstractModel):
    # make odoo model mixin for rocketchat_thread
    _name = "rocketchat.thread.mixin"
    _description = "Rocketchat Thread"

    # add tmid field
    tmid = fields.Char(string="Thread ID", required=True)
    tshow = fields.Boolean(string="Show Thread", default=False)
    utf8_icon = fields.Char(string="UTF8 Icon", default="☑")
    rocketchat_thread = fields.Boolean(string="Threaded Message", default=True)
