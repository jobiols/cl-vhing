# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _timesheet_create_task_prepare_values(self):
        ret = super(SaleOrderLine,
                    self)._timesheet_create_task_prepare_values()  # noqa

        ret['sale_price'] = self.price_subtotal
        ret['product_id'] = self.product_id.id
        ret['cost_price'] = self.product_id.standard_price

        return ret
