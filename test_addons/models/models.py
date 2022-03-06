from odoo import models, fields, api


class test_addons(models.Model):
    _name = 'test_addons.test_addons'
    _description = 'test_addons.test_addons'

    name = fields.Char()

    def action_approve(self):
        view_name = 't1_form_view'
        module = 'test_addons'
        view = self.env['ir.model.data'].search([('name', '=', view_name), ('module', '=', module)])
        view_id = view.res_id
        r = self.env['test.t1'].sudo().search([('name', '=', self.name)])
        print('111111', '\n', r)
        return {
            'name': '工资相关费用明细',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'flags': {'initial_mode': 'view', 'action_buttons': False},
            'res_model': 'test.t1',
            'res_id': r.id,
        }
