# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, api, models
from odoo.addons import decimal_precision as dp


class AccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    code = fields.Char(
        readonly=True,
        string="Work",
        compute="_compute_project_code",
        store=True
    )

    project_code = fields.Char(
        compute="_compute_project_code",
        readonly=True
    )
    work = fields.Char(
        compute="_compute_project_code",
        readonly=True
    )
    description = fields.Char(

    )
    sale_order_ids = fields.One2many(
        'sale.order',
        'analytic_account_id',
        help='Campo tecnico para llegar del project a la SO'
    )

    @api.multi
    def _compute_project_code(self):
        for aa in self:
            project_obj = self.env['project.project']
            proj = project_obj.search([('analytic_account_id.id', '=', aa.id)])
            if len(proj) != 1:
                aa.work = '??'
                aa.code = '??'
                aa.project_code = '??'
            else:
                aa.work = proj.work
                aa.code = proj.work
                aa.project_code = proj.project_code

    @api.multi
    def name_get(self):
        """ Redefinir el nombre de la cuenta analitica
        """
        result = []
        for rec in self:
            name = '[{}] {} -- {}'.format(rec.project_code,
                                          rec.work,
                                          rec.partner_id.name)
            result.append((rec.id, name))
        return result


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
    # este campo se muestra en el listado de partes de horas,
    task_cost = fields.Float(
        digits=dp.get_precision('Product Price'),
        compute="_compute_task_cost",
        readonly=True,
        store=True,
        help='Total to pay for this task'
    )

    @api.depends('unit_amount', 'task_id.cost_price', 'task_id.planned_hours')
    def _compute_task_cost(self):
        """ costo=Costo tarea / horas planificadas x horas del parte de horas
        """
        for aal in self:
            cost = aal.task_id.cost_price
            plan = aal.task_id.planned_hours
            labor = aal.unit_amount
            aal.task_cost = cost / plan * labor if plan else 0
