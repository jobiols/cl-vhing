# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sale_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        help='precio de venta de la tarea'
    )
    cost_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        help='precio de costo de la tarea'
    )
    product_id = fields.Many2one(
        'product.product',
        help='producto que representa esta tarea',
        required=True
    )
    work = fields.Char(
        help='obra para la cual se trabaja en esta tarea',
        related='project_id.work',
        readonly=True
    )
    children_effective_hours = fields.Float(
        compute="_compute_new_task_hours",
        readonly=True,
        string="Sub-tasks Hours Spent",
        help="Total de horas dedicadas en las subtareas"
    )
    new_total_hours_spent = fields.Float(
        compute="_compute_new_task_hours",
        readonly=True,
        string="Total Spent"
    )
    children_planned_hours = fields.Float(
        compute="_compute_new_task_hours",
        readonly=True,
        string="Sub-task Planned Hours"
    )
    total_planned_hours = fields.Float(
        compute="_compute_new_task_hours",
        readonly=True
    )
    new_remaining_hours = fields.Float(
        compute="_compute_new_task_hours",
        readonly=True,
        string="Remaining Hours"
    )
    new_progress = fields.Float(
        compute="_compute_new_task_hours",
        readonly=True,
        string="Progress",
        help="Grado de avance calculado como:\n"
             "Total horas dedicadas / Total horas planificadas * 100"
    )

    @api.depends('stage_id', 'timesheet_ids.unit_amount', 'planned_hours',
                 'child_ids.stage_id', 'child_ids.planned_hours',
                 'child_ids.effective_hours', 'child_ids.children_hours',
                 'child_ids.timesheet_ids.unit_amount')
    def _compute_new_task_hours(self):
        for task in self.sorted(key='id', reverse=True):
            children_planned_hours = children_effective_hours = 0
            for child_task in task.child_ids:
                children_effective_hours += child_task.effective_hours
                children_planned_hours += child_task.planned_hours

            # horas dedicadas de las subtareas
            task.children_effective_hours = children_effective_hours
            # horas totales dedicadas subtareas mas tarea
            task.new_total_hours_spent = children_effective_hours + \
                                         task.effective_hours
            # horas planificadas de las subtareas
            task.children_planned_hours = children_planned_hours
            # horas planificadas subtareas + tarea
            task.total_planned_hours = task.planned_hours + \
                                       children_planned_hours
            # horas restantes
            task.new_remaining_hours = task.total_planned_hours - \
                                       task.new_total_hours_spent
            # progreso
            if task.stage_id and task.stage_id.fold:
                task.new_progress = 100.0
            elif task.planned_hours > 0.0:
                # formula de calculo anterior
                # task.new_progress = round(100.0 * (task.effective_hours + 
                # task.children_hours) / task.planned_hours, 2)
                task.new_progress = round(
                    100.0 * (task.new_total_hours_spent) /
                    task.total_planned_hours, 2)
            else:
                task.new_progress = 0.0


class Project(models.Model):
    _inherit = "project.project"

    purchase_count = fields.Integer(
        compute='_compute_count',
        readonly=True
    )
    sales_count = fields.Integer(
        compute='_compute_count',
        readonly=True
    )
    work = fields.Char(
        compute="_compute_refs",
        readonly=True,
        store=True
    )
    description = fields.Char(
        compute='_compute_refs',
        readonly=True
    )
    project_code = fields.Char(
        compute='_compute_refs',
        readonly=True,
        help='campo tecnico para pasar el project_code a aal'
    )

    stage = fields.Integer(
        compute='_compute_stage',
        readonly=True
    )
    total_sales = fields.Float(
        compute='_compute_total_sales',
        readonly=True
    )
    percent_vh = fields.Float(
        compute='_compute_percent',
        readonly=True,
        string="VH%"
    )
    percent_ing = fields.Float(
        compute='_compute_percent',
        readonly=True,
        string="ING%"
    )
    responsible_initials = fields.Char(
        related='user_id.initials',
        readonly=True,
        string="Resp."
    )

    @api.depends('analytic_account_id.sale_order_ids')
    def _compute_refs(self):
        for proj in self:
            so_ids = proj.mapped('analytic_account_id.sale_order_ids')
            proj.work = so_ids[0].work if so_ids \
                else False
            proj.description = so_ids[0].description if so_ids \
                else False
            # si no esta creado desde una so, entonces como codigo pongo el
            # nombre del proyecto, de esa forma puedo crear proyectos sin so
            proj.project_code = so_ids[0].project_code if so_ids \
                else proj.name

    @api.depends('tasks')
    def _compute_stage(self):
        for proj in self:
            # obtener la etapa como
            # Sum( % avance tarea * $ tarea ) / Sum($ tarea)
            total_price = progress = 0
            for task in proj.tasks:
                total_price += task.sale_price
                progress += task.progress * task.sale_price
            proj.stage = progress / total_price if total_price else 0

    @api.depends('tasks')
    def _compute_percent(self):
        for proj in self:
            # calcular ing como SUM(compra) / SUM(venta) * 100

            sale_price = cost_price = 0.0
            for task in proj.tasks:
                cost_price += task.cost_price
                sale_price += task.sale_price

            proj.percent_ing = 100 * cost_price / sale_price if \
                sale_price != 0 else 0

            # calcular VH como 100 - ing
            proj.percent_vh = 100 - proj.percent_ing

    @api.depends('analytic_account_id')
    def _compute_total_sales(self):
        for proj in self:
            analytic = proj.analytic_account_id
            domain = [('order_id.analytic_account_id.id', '=', analytic.id)]
            proj_sales = self.env['sale.order.line'].search(domain)
            total = 0.0
            for sale in proj_sales:
                total += sale.price_subtotal
            proj.total_sales = total

    @api.depends('analytic_account_id')
    def _compute_count(self):
        for proj in self:
            analytic = proj.analytic_account_id
            _obj_p = self.env['purchase.order.line']
            _obj_s = self.env['sale.order.line']

            domain_p = [('account_analytic_id.id', '=', analytic.id)]
            domain_s = [('order_id.analytic_account_id.id', '=', analytic.id)]

            # TODO no funcionan las purchases
            proj.purchase_count = _obj_p.search_count(domain_p)
            proj.sales_count = _obj_s.search_count(domain_s)

    @api.multi
    def action_view_sales(self):
        self.ensure_one()
        action = self.env.ref('sale.action_product_sale_list')
        analytic = self.analytic_account_id
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'res_model': action.res_model,
            'domain': [('order_id.analytic_account_id.id', '=', analytic.id)],
        }

    @api.multi
    def action_view_purchases(self):
        self.ensure_one()
        analytic = self.analytic_account_id
        return {
            'name': _('Purchase Order Lines'),
            'help': False,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'target': 'current',
            'res_model': 'purchase.order.line',
            'domain': [('account_analytic_id.id', '=', analytic.id)],
        }

    @api.model
    def create(self, vals):
        """ crear por defecto los estados de la lista de etapas.
        """
        res = super(Project, self).create(vals)
        tasks = self.env['project.task.type'].search([])
        for project in res:
            project.type_ids = tasks

        # el nombre del proyecto es el codigo, sin el parentesis con la ref
        # que le pone odoo
        res.name = res.project_code
        return res
