import requests
import logging
import base64
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class IrActions(models.Model):
    _inherit = 'ir.actions.actions'


    @api.model
    def _get_eval_context(self, action=None):
        context = super(IrActions, self)._get_eval_context().copy()
        def request_get(*args, **kwargs):
            return requests.get(*args, **kwargs)
        def request_post(*args, **kwargs):
            return requests.post(*args, **kwargs)
        
        context.update(
            {
                "encodestring": base64.encodestring,
                "request_post": request_post,
                "request_get": request_get,
                "b64encode": base64.b64encode,
                "b64decode": base64.b64decode,
            }
        )
        return context