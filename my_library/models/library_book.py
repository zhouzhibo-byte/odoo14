from odoo import models,fields,api
from datetime import  timedelta

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = "Library Book"
    _order="date_release desc,name"
    _rec_name = 'short_name'

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be unique.'),
        ('positive_page','CHECK(pages>0)','pages must be positive'),
    ]

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title', required=True)
    notes=fields.Text('Internal Notes')
    state=fields.Selection([('draft','Not Available'),('available','Available'),('lost','Lost')],string='State', default='draft')
    description=fields.Html('Description',sanitize=True,strip_style=False)
    cover=fields.Binary('Book Cover')
    out_of_print=fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated=fields.Datetime('Last Updated')
    pages=fields.Integer('Number of Pages',groups='base.group_user',states={'lost':[('readonly',True)]},help='Total book page count',company_dependent=False)
    reader_rating=fields.Float('Reader Average Rating',digits=(14,4))

    # author_ids = fields.Many2many('res.partner.me',string='Authors')
    author_ids = fields.Char(string='Authors')

    currency_id=fields.Many2one('res.currency',string='Currency')
    retail_price=fields.Monetary('Retail_price')

    publisher_id=fields.Many2one('res.partner.me',string='Publisher',ondelete='set null',context={},domain=[],)
    publisher_city=fields.Char('Publisher  City',related='publisher_id.city',readonly=True)

    category_id=fields.Many2one('library.book.category')

    age_days=fields.Float(string='Day Since Release',compute="_compute_age",inverse='_inverse_age',search='_search_age',store=False,compute_sudo=False)

    ref_doc_id=fields.Reference(selection='_referencable_models',string='Reference Document')

    states = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        'States', default="draft")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    @api.model
    def _referencable_models(self):
        models=self.env['ir.model'].search([('model','like','%library%')])
        return [(x.model,x.name) for x in models]

    @api.depends('date_release')
    def _compute_age(self):
        today=fields.Date.today()
        for book in self.filtered('date_release'):
            delta=today-book.date_release
            book.age_days=delta.days

    def _inverse_age(self):
        today=fields.Date.today()
        for book in self.filtered('date_release'):
            d=today-timedelta(days=book.age_days)
            book.date_release=d

    def _search_age(self,operator,value):
        today=fields.Date.today()
        value_days=timedelta(days=value)
        value_date=today-value_days
        operator_map={
            '>':'<','>=':'<=',
            '<':'>','<=':'>=',
        }
        new_op=operator_map.get(operator,operator)
        return [('date_release',new_op,value_date)]

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release>fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

    def change_update_data(self):
        print("11111111111")
        print(self)
        # print(self.date_updated)
        # 为什么这里是一条记录
        a=self.ensure_one()
        # self.date_updated=fields.Datetime.now()
        self.update({'date_updated':fields.Datetime.now()})
        print(a)
        print("222222222222")


class LibraryMember(models.Model):
    _name = 'library.member'
    # 为什么写在这里报错
    # _inherits = {'res.partner.me': 'partner_id'}
    partner_id = fields.Many2one('res.partner.me', ondelete='cascade',delegate=True)
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')

    @api.model
    def get_all_library_member(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])

