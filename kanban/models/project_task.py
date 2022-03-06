from odoo import models, fields, api


class ProjectTask(models.Model):
    _name = 'project.task'
    _description = 'kanban.project.task'

    name = fields.Char(string='名称')
    stage_id=fields.Selection([('sup','厂家'),('cou','用户'),('zjs','中间商')],default='sup',string='角色')