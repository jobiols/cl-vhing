# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    asignee_id = fields.Many2one(
        'res.users',
        related="task_id.user_id",
        readonly=True
    )

    name = fields.Char(
        required=False
    )

    work = fields.Char(
        related="task_id.project_id.work",
        readonly=True
    )

    purchase_order_id = fields.Many2one(
        'purchase.order',
        help="Purchase order for this piece of work",
        readonly=True
    )

    @api.multi
    @api.depends('name')
    def name_get(self):
        result = []
        for aal in self:
            name = aal.task_id.name
            result.append((aal.id, name))
        return result
