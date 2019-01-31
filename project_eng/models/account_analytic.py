# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, api, models
from odoo.addons import decimal_precision as dp


class AccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    code = fields.Char(
        compute="_compute_code",
        readonly=True,
        string="Work"
    )

    sale_order_ids = fields.One2many(
        'sale.order',
        'analytic_account_id',
        help='Campo tecnico para llegar del project a la SO'
    )

    @api.depends('line_ids')
    def _compute_code(self):
        for analytic in self:
            work = set(analytic.line_ids.mapped('work'))
            if False in work:
                work.remove(False)
            analytic.code = ', '.join(work)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    # no queremos usar este campo lo ponemos como no requerido
    name = fields.Char(
        required=False
    )

    # este campo se muestra en el listado de partes de horas y se usa para
    # filtrar las timesheets
    asignee_id = fields.Many2one(
        'res.users',
        related="task_id.user_id",
        readonly=True,
        store=True
    )
    # este campo se muestra en el listado de partes de horas y se usa para
    # filtrar las timesheets
    work = fields.Char(
        related="task_id.project_id.work",
        readonly=True,
        store=True,
        help='work related to this analytic line'
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
    # este campo se muestra en el listado de partes de horas
    amount = fields.Float(
        digits=dp.get_precision('Product Price'),
        compute="_compute_amount",
        readonly=True,
    )

    def _compute_amount(self):
        for aal in self:
            aal.amount = aal.unit_amount * aal.task_id.cost_price / 100
