# from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class SaleOrderTemplateOption(models.Model):
    _inherit = "sale.order.template.option"
    _order = 'sequence'

    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of sale quote lines.",
                              default=10)
    hotel = fields.Many2one('model.hotel', string="Hotel")
    inventory = fields.Float(string="Inventory", default=100)
    stock = fields.Float(string="Stock", compute="_compute_stock", )
    available = fields.Float(string="Available", compute="_compute_available")
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    template_name = fields.Char(related='sale_order_template_id.name', store=True)
    product_category_custom = fields.Selection([('room', 'Room'), ('visa', 'Visa'), ('program', 'Program'),
                                                ('domestic', 'Domestic'), ('international', 'International')],
                                               compute='compute_type', )
    price_unit = fields.Float()

    # @api.one
    def compute_type(self):
        for rec in self:
            rec.product_category_custom = rec.product_id.product_category_custom

    @api.depends('product_id', 'inventory', 'stock')
    def _compute_stock(self):
        for rec in self:
            sale_order_domain = [('product_id', '=', rec.product_id.id), ('state', 'not in', (['draft', 'waiting',
                                                                                               'sent', 'expired']))]
            sale_order_line_ids = self.env['sale.order.line'].sudo().search(sale_order_domain).filtered(
                lambda x: x.order_id.sale_order_template_id.id == rec.sale_order_template_id.id)
            rec.stock = sum(sale_order_line_ids.mapped('product_uom_qty'))

    def create_sale_order_option(self, sale_order):
        order_options = self.env['sale.order.option']
        for option in self:
            order_options |= order_options.create({
                'sale_order_id': sale_order.id,
                'product_id': option.product_id.id,
                'name': option.name,
                'price_extra': option.price_extra,
                'price_unit': option.price_unit,  # Pass the value of the new field to sale.order.option
            })
        return order_options

    @api.depends('stock', 'inventory')
    def _compute_available(self):
        for rec in self:
            if not rec.product_category_custom == 'room':
                rec.available = rec.inventory - rec.stock
            else:
                if self.sale_order_template_id.available_rooms > rec.inventory:
                    rec.available = rec.inventory - rec.stock
                else:
                    rec.available = self.sale_order_template_id.available_rooms

