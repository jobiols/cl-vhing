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
        """ Factura las tareas seleccionadas en el wizard, agrupando por
            el asignee
        """
        purchase_order_obj = self.env['purchase.order']

        # buscar asignados para determinar las oc a generar
        asignee_ids = self.aal_ids.mapped('asignee_id')

        # generar las ordenes de compra
        for po_asignee in asignee_ids:
            # obtener las tareas que van en cada oc
            _aal_ids = self.aal_ids.filtered(
                lambda r: r.asignee_id == po_asignee)

            # crear la oc, hay que cambiar el usuario por el partner asociado
            po = purchase_order_obj.create({
                'partner_id': po_asignee.partner_id.id,
                'partner_ref': po_asignee.partner_id.ref})

            # crear las lineas de la oc que son los productos (tareas)
            for aal in _aal_ids:
                if not aal.task_id.product_id:
                    raise UserError(_('Task %s does not have an associated '
                                      'product. I need a product to create '
                                      'the invoice line') % aal.task_id.name)

                # traemos el costo cargado en la tarea.
                task = aal.task_id
                price_task = task.cost_price
                planned_hours = task.planned_hours
                taxes = [x.id for x in task.product_id.supplier_taxes_id]
                po.order_line.create(
                    {'product_id': aal.task_id.product_id.id,
                     'product_qty': aal.unit_amount,
                     'price_unit': price_task / planned_hours,
                     'price_task_total': price_task,
                     'name': aal.task_id.name,
                     'date_planned': aal.date,
                     'product_uom': 1,
                     'order_id': po.id,
                     'account_analytic_id':
                         aal.project_id.analytic_account_id.id,
                     'taxes_id': [(6, 0, taxes)]
                     })
                # enlazar la orden de compra con la linea analitica
                aal.purchase_order_id = po.id

    @api.model
    def default_get(self, fields):
        """ Obtiene las aal tildadas para facturar
        """
        ret = super(ProjectTaskInvoiceWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', False)
        if active_ids:
            selected_aal_ids = self.env['account.analytic.line'].browse(
                active_ids)
            ret.update({'aal_ids': selected_aal_ids.ids})
        return ret
