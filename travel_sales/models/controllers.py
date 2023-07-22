from odoo import http

class PortalQuotationTemplatesController(http.Controller):
    @http.route('/portal/quotation_templates', type='http', auth='user', website=True)
    def portal_quotation_templates(self, **kwargs):
        QuotationTemplate = http.request.env['sale.order.template']
        quotation_templates = QuotationTemplate.search([])
        return http.request.render('your_module.portal_quotation_templates', {
            'quotation_templates': quotation_templates,
        })
