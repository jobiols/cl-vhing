# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProjectTaskInvoiceWizard(models.TransientModel):
    _name = 'project.task.invoice.wizard'

    aal_ids = fields.Many2many(
        'account.analytic.line',
        string="Tasks to Invoice",
        required=True
    )

    @api.multi
    def invoice_tasks(self):
        purchase_order_obj = self.env['purchase.order']
        purchase_orders = []

        # buscar tuplas distintas que son las oc a generar
        # la tupla se forma con el asignado y la cuenta analitica
        for task in self.aal_ids:
            po_tuple = (task.asignee_id, task.project_id.analytic_account_id)
            if po_tuple not in purchase_orders:
                purchase_orders.append(po_tuple)

        # generar las ordenes de compra
        for po_data in purchase_orders:
            # obtener las tareas que van en cada oc
            _aals = self.aal_ids.filtered(lambda r: r.asignee_id == po_data[
                0] and r.project_id.analytic_account_id == po_data[1])

            # crear la oc, hay que cambiar el usuario por el partner asociado
            po = purchase_order_obj.create({
                'partner_id': po_data[0].partner_id.id,
                'analytic_account_id': po_data[1].id})

            # crear los productos
            for aal in _aals:
                if not aal.task_id.product_id:
                    raise UserError(_('Task %s does not have an associated '
                                      'product.') % aal.task_id.name)
                po.order_line.create(
                    {'product_id': aal.task_id.product_id.id,
                     'product_qty': aal.unit_amount,
                     'price_unit': aal.task_id.product_id.standard_price,
                     'name': aal.task_id.name,
                     'date_planned': aal.date,
                     'product_uom': 1, 'order_id': po.id})
                # enlazar la orden de compra con la linea analitica
                aal.purchase_order_id = po.id

    @api.model
    def default_get(self, fields):
        ret = super(ProjectTaskInvoiceWizard, self).default_get(fields)
        selected_aals = self.env['account.analytic.line'].browse(
            self.env.context.get('active_ids', False))
        ret.update({'aal_ids': selected_aals.ids})
        return ret
