# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    sale_order_ids = fields.One2many(
        'sale.order',
        'analytic_account_id',
        help='Campo tecnico para llegar del project a la SO'
    )


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    # este campo se muestra en el listado de partes de horas
    asignee_id = fields.Many2one(
        'res.users',
        related="task_id.user_id",
        readonly=True,
        store=True
    )
    # este campo se muestra en el listado de partes de horas
    work = fields.Char(
        related="task_id.project_id.work",
        readonly=True,
        help='work related to this piece of work'
    )
    project_code = fields.Char(
        related="task_id.project_id.project_code",
        readonly=True,
        help='campo tecnico para pasar el project_code a la oc'
    )
    description = fields.Char(
        related="task_id.project_id.description",
        readonly=True,
        help='campo tecnico para pasar la description a la oc'
    )
    # este campo se muestra en el listado de partes de horas y se completa
    # con la PO cuando se compran las horas.
    purchase_order_id = fields.Many2one(
        'purchase.order',
        help="Purchase order for this piece of work",
        readonly=True
    )
