# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    work = fields.Char(
        compute="_compute_refs",
        readonly=True,
    )
    project_code = fields.Char(
        compute='_compute_refs',
        readonly=True,
    )
    description = fields.Char(
        compute='_compute_refs',
        readonly=True,
    )

    @api.depends('order_line.account_analytic_id.line_ids')
    def _compute_refs(self):
        for po in self:
            line_ids = po.mapped('order_line.account_analytic_id.line_ids')
            work = set(line_ids.mapped('work'))
            project_code = set(line_ids.mapped('project_code'))
            description = set(line_ids.mapped('description'))

            if False in work:
                work.remove(False)
            if False in project_code:
                project_code.remove(False)
            if False in description:
                description.remove(False)
            po.work = ', '.join(work)
            po.project_code = ', '.join(project_code)
            po.description = ', '.join(description)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    price_task_total = fields.Float(
        digits=dp.get_precision('Product Price')
    )
