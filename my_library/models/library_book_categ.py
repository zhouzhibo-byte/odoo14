from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = 'library.book.category'

    _parent_store = True
    _parent_name = "parent_id"  # optional if field is 'parent_id'

    name = fields.Char('Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one(
        'library.book.category',
        string='Parent Category',
        ondelete='restrict',
        index=True
    )
    child_ids = fields.One2many(
        'library.book.category', 'parent_id',
        string='Child Categories')
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')

    def create_categories(self):
        print("33333")
        print(self)
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1',
            'parent_path': '1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2',
            'parent_path': '1'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'parent_path':'1',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }

        print(parent_category_val)
        # Total 3 records (1 parent and 2 child) will be craeted in library.book.category model
        record = self.env['library.book.category'].sudo().create(parent_category_val)
        print(record)