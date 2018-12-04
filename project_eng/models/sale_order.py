# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pelotas = fields.Char(
        required=True
    )
    work = fields.Char(

    )
    project_code = fields.Char(

    )
    partner_contact_id = fields.Many2one(
        'res.partner'
    )
    description = fields.Char(

    )
    user_initials = fields.Char(
        compute="_compute_user_initials"
    )
    stage_percent = fields.Float(
        help="Porcentaje de avance"
    )
    amount_paid_percent = fields.Float(
        help="Porcentaje cobrado del total facturado"
    )
    amount_invoiced_percent = fields.Float(
        help="Porcentaje de la orden de venta que ha sido facturado"
    )
    amount_due = fields.Float(
        help="Lo que resta cobrar del total facturado"
    )

    _sql_constraints = [('project_code_unique', 'unique(project_code)',
                         'The project code must be unique.')]

    @api.depends('user_id')
    def _compute_user_initials(self):
        for so in self:
            name_list = so.user_id.name.split()
            initials = ""
            for name in name_list:
                initials += name[0].upper()
            so.user_initials = initials


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _timesheet_create_task_prepare_values(self):
        ret = super(SaleOrderLine,
                    self)._timesheet_create_task_prepare_values()  # noqa

        ret['sale_price'] = self.product_id.list_price
        ret['product_id'] = self.product_id.id
        ret['cost_price'] = self.product_id.standard_price

        return ret
