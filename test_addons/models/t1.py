from odoo import models, fields, api

class t1(models.Model):
    _name = 'test.t1'
    _description = 'test_addons.test_addons'

    name = fields.Char()
    user_id=fields.Many2one('res.users','姓名')

    @api.model
    def create(self,vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code('om.internal.bom.adjustment.update') or '/'
        result = super('t1', self).create(vals)
        return result

