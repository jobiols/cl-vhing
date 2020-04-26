# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    work = fields.Char(

    )
    project_code = fields.Char(

    )
    partner_contact_id = fields.Many2one(
        'res.partner'
    )
    description = fields.Char(

    )
    user_initials = fields.Char(
        related="user_id.initials",
        readonly=True,
        help="Iniciales del nombre del usuario responsable"
    )
    stage = fields.Integer(
        help="Porcentaje de avance",
        related="project_ids.stage",
        readonly=True
    )
    amount_paid_percent = fields.Float(
        help="Porcentaje cobrado del total facturado",
        compute="_compute_percentages",
        readonly=True
    )
    amount_invoiced_percent = fields.Float(
        help="Porcentaje de la orden de venta que ha sido facturado",
        compute="_compute_percentages",
        readonly=True
    )
    amount_due = fields.Float(
        help="Lo que resta cobrar del total facturado",
        compute="_compute_percentages",
        readonly=True
    )

    _sql_constraints = [('project_code_unique', 'unique(project_code)',
                         'The project code must be unique.')]

    @api.depends()
    def _compute_percentages(self):
        for so in self:
            # inicializar variables
            amount_invoiced = 0
            residual = 0

            # total de la orden de venta
            amount_total = so.amount_total

            # sumar total y residual de todas las facturas
            for invoice in so.invoice_ids:
                amount_invoiced += invoice.amount_total
                residual += invoice.residual

            # calcular el cobrado como facturado menos residual
            amount_paid = amount_invoiced - residual

            # porcentaje facturado sobre el total de la ov
            _ = 100 * amount_invoiced / amount_total if amount_total else 0
            so.amount_invoiced_percent = _

            # porcentaje cobrado del total facturado
            _ = 100 * amount_paid / amount_invoiced if amount_invoiced else 0
            so.amount_paid_percent = _

            # total que queda por cobrar en pesos
            so.amount_due = residual

    @api.multi
    def _create_analytic_account(self, prefix=None):
        """ metodo heredado para pasarle los tres parametros al crear la
            analitica: project_code, work y description
            se dispara al confirmar la venta.
        """
        for order in self:
            analytic = self.env['account.analytic.account'].create({
                'name': order.project_code,
                'code': order.client_order_ref,
                'company_id': order.company_id.id,
                'partner_id': order.partner_id.id,
                'description': order.description,
                'work': order.work,
                'project_code': order.project_code
            })
            order.analytic_account_id = analytic


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    project_code = fields.Char(
        related='order_id.project_code',
        readonly=True
    )

    @api.model
    def _timesheet_create_task_prepare_values(self):
        """ Sobreescribo esto para pasarle a las tasks:
            - los precios
            - el producto asociado a la tarea
            - el codigo de proyecto
            - la obra
        """
        ret = super(SaleOrderLine,
                    self)._timesheet_create_task_prepare_values()
        ret['sale_price'] = self.product_id.list_price
        ret['product_id'] = self.product_id.id
        ret['cost_price'] = self.product_id.standard_price
        ret['work'] = self.order_id.work
        ret['description'] = self.order_id.description
        ret['project_code'] = self.order_id.project_code

        return ret
