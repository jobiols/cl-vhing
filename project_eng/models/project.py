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
        help='producto que representa esta tarea'
    )
    project_code = fields.Char(
        help='codigo de proyecto que corresponde a esta tarea'
    )
    work = fields.Char(
        help='obra para la cual se trabaja en esta tarea'
    )
    description = fields.Char(
        help='descripcion que viene de la SO'
    )


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
        compute="_compute_work",
        readonly=True
    )
    description = fields.Char(
        compute='_compute_description',
        readonly=True
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

    @api.depends('tasks')
    def _compute_work(self):
        for proj in self:
            # lo paso a set para eliminar duplicados
            work = set(proj.tasks.mapped('work'))
            # si alguna viene en False la tengo que sacar
            if False in work:
                work.remove(False)
            proj.work = ', '.join(work) if work else False

    @api.depends('tasks')
    def _compute_description(self):
        for proj in self:
            import re
            desc_list = []
            description = False

            for task in proj.tasks:
                # le saco el html
                if task.description:
                    description = re.sub('<[^<]+?>', '', task.description)
                    if description not in desc_list:
                        desc_list.append(description)
            proj.description = ', '.join(desc_list) if desc_list else False

    @api.multi
    def _compute_stage(self):
        for proj in self:
            # obtener la etapa como
            # Sum( % avance tarea * $ tarea ) / Sum($ tarea)
            total_price = progress = 0
            for task in proj.tasks:
                total_price += task.sale_price
                progress += task.progress * task.sale_price
            proj.stage = progress / total_price if total_price else 0

    @api.multi
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

    @api.multi
    def _compute_total_sales(self):
        for proj in self:
            analytic = proj.analytic_account_id
            domain = [('order_id.analytic_account_id.id', '=', analytic.id)]
            proj_sales = self.env['sale.order.line'].search(domain)
            total = 0.0
            for sale in proj_sales:
                total += sale.price_subtotal
            proj.total_sales = total

    @api.multi
    def _compute_count(self):
        """ TODO Revisar
        """
        return

        for proj in self:
            analytic = proj.analytic_account_id
            _obj_p = self.env['purchase.order.line']
            _obj_s = self.env['sale.order.line']
            domain = [('order_id.analytic_account_id.id', '=', analytic.id)]

            proj.purchase_count = _obj_p.search_count(domain)
            proj.sales_count = _obj_s.search_count(domain)

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
            'domain': [('order_id.analytic_account_id.id', '=', analytic.id)],
        }

    @api.model
    def create(self, vals):
        """ crear por defecto los estados de la lista de etapas.
        """
        res = super(Project, self).create(vals)
        tasks = self.env['project.task.type'].search([])
        for project in res:
            project.type_ids = tasks

        return res
