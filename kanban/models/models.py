

from odoo import models, fields, api


class kanban(models.Model):
    _name = 'kanban.kanban'
    _description = 'kanban.kanban'

    name = fields.Char()
    supplier = fields.Integer()
    customer= fields.Float()
    description = fields.Text()


