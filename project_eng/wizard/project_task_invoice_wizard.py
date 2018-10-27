# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ProjectTaskInvoiceWizard(models.TransientModel):
    _name = 'project.task.invoice.wizard'

    task_ids = fields.Many2many('project.task', string="Tasks to Invoice",
                                required=True)
    target_task_name = fields.Char('New task name')

    @api.multi
    def invoice_tasks(self):
        purchase_order_obj = self.env['purchase.order']

        import wdb;        wdb.set_trace()

        purchase_orders = []

        # buscar tuplas distintas que son las oc a generar
        for task in self.task_ids:
            user_account = (task.user_id, task.project_id.analytic_account_id)
            if user_account not in purchase_orders:
                purchase_orders.append(user_account)

        # generar las ordenes de compra
        for po_data in purchase_orders:
            # obtener las tareas que van en cada oc
            _tasks = self.task_ids.filtered(
                lambda r: r.user_id == po_data[0] and
                          r.project_id.analytic_account_id == po_data[1])
            # crear la oc
            po = purchase_order_obj.create({
                'partner_id': po_data[0],
                'analytic_account_id': po_data[1]
            })

            # crear los productos
            for task in _tasks:
                po.order_line.create({
                    'product_id': task.product_id,
                    'product_qty': 1,
                    'price_unit': 100,
                })

    @api.model
    def default_get(self, fields):
        result = super(ProjectTaskInvoiceWizard, self).default_get(fields)
        selected_tasks = self.env['project.task'].browse(
            self.env.context.get('active_ids', False))
        # assigned_tasks = selected_tasks.filtered(lambda task: task.user_id)
        result.update({
            'task_ids': selected_tasks.ids,
        })
        return result
