# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    work = fields.Char(
        readonly=True,
        compute="_compute_work"
    )
    project_code = fields.Char(
        compute='_compute_project_code'
    )
    description = fields.Char(
        compute='_compute_description'
    )

    """ Quitar la analytic account para bajarla a la linea
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        readonly=True,
        states={'draft': [('readonly', False)],
                'sent': [('readonly', False)]},
        help="The analytic account related to a purchase order.",
        copy=False
    )
    """

    @api.depends('order_line')
    def _compute_project_code(self):
        for po in self:

            import wdb;wdb.set_trace()



            aa_ids = po.order_line.mapped('account_analytic_id')
            project_codes = aa_ids.mapped('')

            if po.analytic_account_id:
                project_code = []
                sos = po.analytic_account_id.get_so()
                for so in sos:
                    if so.project_code:
                        project_code.append(so.project_code)
                po.project_code = ', '.join(project_code) if project_code \
                    else False


    """ ya no hay analytic en la po
    @api.depends('analytic_account_id')
    def _compute_work(self):
        for po in self:
            if po.analytic_account_id:
                work = []
                sos = po.analytic_account_id.get_so()
                for so in sos:
                    if so.work:
                        work.append(so.work)
                po.work = ', '.join(work) if work else False
    """

    """ ya no hay analytic en la po
    @api.depends('analytic_account_id')
    def _compute_description(self):
        for po in self:
            if po.analytic_account_id:
                description = []
                sos = po.analytic_account_id.get_so()
                for so in sos:
                    if so.description:
                        description.append(so.description)
                po.description = ', '.join(description) if description \
                    else False
    """


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    """ Esto esta re mal, ya hay una analitica en la pol
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        related='order_id.analytic_account_id',
        store=True,
        readonly=True
    )
    """
    price_task_total = fields.Float(
        digits=dp.get_precision('Product Price')
    )
