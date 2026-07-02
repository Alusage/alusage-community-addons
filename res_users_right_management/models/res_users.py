from odoo import api, fields, models, SUPERUSER_ID, _

class ResUsers(models.Model):
    _inherit = "res.users"

    accesses_count = fields.Integer('# Access Rights', help='Number of access rights that apply to the current user',
                                    compute='_compute_accesses_count', compute_sudo=True)
    rules_count = fields.Integer('# Record Rules', help='Number of record rules that apply to the current user',
                                 compute='_compute_accesses_count', compute_sudo=True)
    groups_count = fields.Integer('# Groups', help='Number of groups that apply to the current user',
                                  compute='_compute_accesses_count', compute_sudo=True)

    @api.depends('groups_id')
    def _compute_accesses_count(self):
        for user in self:
            groups = user.groups_id
            accesses_count = self.env['ir.model.access']
            rules_count = self.env['ir.rule']
            for group in groups:
                accesses_count |= group.model_access
                rules_count |= group.rule_groups
            user.accesses_count = len(accesses_count)
            user.rules_count = len(rules_count)
            user.groups_count = len(groups)

    def action_show_groups(self):
        self.ensure_one()
        return {
            'name': _('Groups'),
            'view_mode': 'tree,form',
            'res_model': 'res.groups',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('id','in', self.groups_id.ids)],
            'target': 'current',
        }

    def action_show_accesses(self):
        self.ensure_one()
        model_access = self.env['ir.model.access']
        for group in self.groups_id:
            model_access |= group.model_access
        return {
            'name': _('Access Rights'),
            'view_mode': 'tree,form',
            'res_model': 'ir.model.access',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('id', 'in', model_access.ids)],
            'target': 'current',
        }

    def action_show_rules(self):
        self.ensure_one()
        ir_rules = self.env['ir.rule'].search([('global','=',True)])
        for group in self.groups_id:
            ir_rules |= group.rule_groups
        return {
            'name': _('Record Rules'),
            'view_mode': 'tree,form',
            'res_model': 'ir.rule',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('id', 'in', ir_rules.ids)],
            'target': 'current',
        }