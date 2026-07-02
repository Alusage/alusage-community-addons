import base64
import re
import json
import logging
from rocketchat_API.rocketchat import RocketChat
from markdownify import markdownify as md

from odoo import _, api, fields, models
from odoo.tools import email_split, float_is_zero

_logger = logging.getLogger(__name__)


class RockchatThread(models.AbstractModel):
    # make odoo model mixin for rocketchat_thread
    _name = "rocketchat.thread.mixin"
    _description = "Rocketchat Thread"

    # add tmid field
    tmid = fields.Char(string="Thread ID", required=True)
    tshow = fields.Boolean(string="Show Thread", default=False)
    utf8_icon = fields.Char(string="UTF8 Icon", default="☑")
    rocketchat_thread = fields.Boolean(string="Threaded Message", default=True)
