# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    work = fields.Char(

    )
    partner_contact_id = fields.Many2one(
        'res.partner'
    )

    project_code = fields.Char(
        required=True
    )

    description = fields.Char(

    )


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
