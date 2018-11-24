# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    work = fields.Char(
        readonly=True,
        compute="_compute_work"
    )

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        readonly=True,
        states={'draft': [('readonly', False)],
                'sent': [('readonly', False)]},
        help="The analytic account related to a purchase order.",
        copy=False
    )

    @api.depends('analytic_account_id')
    def _compute_work(self):
        for po in self:
            if po.analytic_account_id:
                work = []
                sos = po.analytic_account_id.get_work()
                for so in sos:
                    if so.work:
                        work.append(so.work)
                po.work = ', '.join(work) if work else False


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        related='order_id.analytic_account_id',
        store=True,
        readonly=True
    )
