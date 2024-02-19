from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp


class InventoryCustom(models.Model):
    _inherit = 'product.product'

    product_category_custom = fields.Selection([('room', 'Room'), ('visa', 'Visa'), ('program', 'Program'),
                                         ('domestic', 'Domestic'), ('international', 'International')], track_visibility='always',)


class PurchaseCustom(models.Model):
    _inherit = 'purchase.order'

    def unlink(self):
        if not self.env.user.has_group('details.group_sale_super_manager'):
            raise ValidationError("Sorry you can not delete")
        super(PurchaseCustom, self).unlink()


class SaleOrderTemplateCust(models.Model):
    _inherit = 'sale.order.template'

    # number_sales = fields.Integer(compute='number_of_sales')
    # change = fields.Integer()

    stock_rooms = fields.Float(compute="_compute_stock",)
    stock_visa = fields.Float(compute="_compute_stock",)
    stock_program = fields.Float(compute="_compute_stock",)
    stock_domestic = fields.Float(compute="_compute_stock",)
    stock_international = fields.Float(compute="_compute_stock",)

    total_rooms = fields.Float()
    total_visa = fields.Float()
    total_program = fields.Float()
    total_domestic = fields.Float()
    total_international = fields.Float()

    available_rooms = fields.Float(compute="_compute_available",)
    available_visa = fields.Float(compute="_compute_available",)
    available_program = fields.Float(compute="_compute_available",)
    available_domestic = fields.Float(compute="_compute_available",)
    available_international = fields.Float(compute="_compute_available",)

    total_amount = fields.Float(compute='_compute_total', store=True)
    total_paid = fields.Float(compute='_compute_total', store=True)
    total_due = fields.Float(compute='_compute_total', store=True)

    total_adults = fields.Integer(compute='_compute_numbers', store=True)
    total_children = fields.Integer(compute='_compute_numbers', store=True)
    total_infants = fields.Integer(compute='_compute_numbers', store=True)

    def _compute_numbers(self):
        sale_order_domain = [('sale_order_template_id', '=', self.name),
                             ('state', 'not in', (['draft', 'waiting', 'sent', 'expired']))]
        sale_order_total = self.env['sale.order'].sudo().search(sale_order_domain)
        for x in range(len(sale_order_total)):
            self.total_adults += sale_order_total[x].adult
            self.total_children += sale_order_total[x].child
            self.total_infants += sale_order_total[x].infant

    def _compute_total(self):
        sale_order_domain = [('sale_order_template_id', '=', self.name),
                             ('state', 'not in', (['draft', 'waiting', 'sent', 'expired']))]
        sale_order_total = self.env['sale.order'].sudo().search(sale_order_domain)
        if sale_order_total:
            for x in range(len(sale_order_total)):
                self.total_amount += sale_order_total[x].amount_total
                self.total_paid += sale_order_total[x].total_payments
                self.total_due += sale_order_total[x].total_due

    # @api.depends('total_rooms',)
    def _compute_stock(self):

        for rec in self:
            rec.stock_rooms = 0
            rec.stock_visa = 0
            rec.stock_program = 0
            rec.stock_domestic = 0
            rec.stock_international = 0
            sale_order_domain = [('template_name', '=', rec.name),
                                 ('state', 'not in', (['draft', 'waiting', 'sent', 'expired']))]
            sale_order_lines = rec.env['sale.order.line'].sudo().search(sale_order_domain)

            sale_order_line_ids_rooms = sale_order_lines.filtered(lambda x: x.product_category_custom == "room")
            print(len(sale_order_line_ids_rooms))
            for line in sale_order_line_ids_rooms:
                rec.stock_rooms += line.product_uom_qty
            # sale_order_line_ids_visa = rec.env['sale.order.line'].sudo().search(sale_order_domain).
            # filtered(lambda x: x.product_category == 'visa')
            # sale_order_line_ids_program = rec.env['sale.order.line'].sudo().
            # search(sale_order_domain).filtered(lambda x: x.product_category == 'program')
            # sale_order_line_ids_domestic = rec.env['sale.order.line'].sudo().
            # search(sale_order_domain).filtered(lambda x: x.product_category == 'domestic')
            # sale_order_line_ids_int = rec.env['sale.order.line'].sudo().
            # search(sale_order_domain).filtered(lambda x: x.product_category == 'international')

            # if sale_order_line_ids_visa:
            #     for y in range(len(sale_order_line_ids_visa)):
            #         rec.stock_visa += sale_order_line_ids_visa[y].product_uom_qty
            # if sale_order_line_ids_program:
            #     for y in range(len(sale_order_line_ids_program)):
            #         rec.stock_program += sale_order_line_ids_program[y].product_uom_qty
            # if sale_order_line_ids_domestic:
            #     for y in range(len(sale_order_line_ids_domestic)):
            #         rec.stock_domestic += sale_order_line_ids_domestic[y].product_uom_qty
            # if sale_order_line_ids_int:
            #     for y in range(len(sale_order_line_ids_int)):
            #         rec.stock_international += sale_order_line_ids_int[y].product_uom_qty

    # @api.one
    @api.depends('total_rooms', 'duration',)
    def _compute_available(self):
        self.available_rooms = self.total_rooms - self.stock_rooms
        self.available_visa = self.total_visa - self.stock_visa
        self.available_program = self.total_program - self.stock_program
        self.available_domestic = self.total_domestic - self.stock_domestic
        self.available_international = self.total_international - self.stock_international

    # def search_stock(self, operator, value):
    #     print(operator)
    #     print(value)

    # @api.one
    # def number_of_sales(self):
    #     num = self.env['sale.order'].search([('sale_order_template_id', '=', self.name),])
    #     self.number_sales = num


class SaleOrderCust(models.Model):
    _inherit = 'sale.order'

    total_rooms = fields.Float(related='sale_order_template_id.total_rooms')


class SaleOrderOption(models.Model):
    _inherit = 'sale.order.option'

    transfer = fields.Boolean("Transfer", default=False)
    hotel = fields.Many2one('model.hotel', string="Hotel")
    inventory = fields.Float(string="Inventory")
    analytic_tag_id = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    available = fields.Float(string="Available", compute="_compute_available")
    product_category_custom = fields.Selection([('room', 'Room'), ('visa', 'Visa'), ('program', 'Program'), ('domestic', 'Domestic'), ('international', 'International')])
    price_usd = fields.Float()

    def compute_is_room(self):
        for rec in self:
            print("Processing record:", rec)
            rec.product_category_custom = rec.product_id.product_category_custom
            print("Updated product_category_custom:", rec.product_category_custom)

    @api.depends('product_id', 'quantity')
    def _compute_available(self):
        for rec in self:
            rec.available = 0
            sale_order_template_option_id = self.env['sale.order.template.option'].sudo().search(
                [('product_id', '=', rec.product_id.id),
                 ('template_name', '=', self.order_id.sale_order_template_id.name)], limit=1)
            if sale_order_template_option_id:
                rec.price_unit = sale_order_template_option_id.price_unit
                rec.price_usd = sale_order_template_option_id.price_usd
                rec.available = sale_order_template_option_id.available
                rec.analytic_tag_id = sale_order_template_option_id.analytic_tag_ids


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    location_id = fields.Many2one('stock.location', "Location")
    cost = fields.Float('Cost', related="product_id.standard_price", store=True, readonly=False)
    available = fields.Float(string="Available", compute="_compute_available")
    reserved = fields.Float()
    product_category_custom = fields.Selection([('room', 'Room'), ('visa', 'Visa'), ('program', 'Program'), ('domestic', 'Domestic'),
                                   ('international', 'International')], compute='compute_is_room', store=True)
    template_name = fields.Char(related='order_id.sale_order_template_id.name')
    price_usd = fields.Float()
    total_usd = fields.Float(string='Total in USD', compute='total_usd_def')

    def total_usd_def(self):
        for rec in self:
            rec.total_usd = rec.product_uom_qty * rec.price_usd

    # product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'),
    #                                required=True, default=1.0)

    # @api.depends('cost')
    # @api.onchange('product_uom_qty')
    # def update_rooms(self):
    #     if self.is_room:
    #         print('change')
    #         changee = self.env['sale.order.template'].search([('name', '=', self.template_name)])
    #         print(changee)
    #         print(changee.change)
    #         changee.change = 1

    @api.depends('product_id')
    def compute_is_room(self):
        for rec in self:
            print("Processing record:", rec)
            rec.product_category_custom = rec.product_id.product_category_custom
            print("Updated product_category_custom:", rec.product_category_custom)

    # @api.one
    @api.depends('product_id', 'product_uom_qty')
    def _compute_available(self):
        for rec in self:
            rec.available = 0
            if rec.product_id:
                sale_order_template_option_id = self.env['sale.order.template.option'].sudo().search(
                    [('product_id', '=', rec.product_id.id),
                     ('template_name', '=', self.order_id.sale_order_template_id.name)], limit=1)
                if sale_order_template_option_id:
                    rec.available = sale_order_template_option_id.available



