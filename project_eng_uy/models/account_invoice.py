# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    work = fields.Char(
        string='Obra',
        compute='_compute_work',
        help='Obra que se factura\n'
             'Si en la obra figura N/D es porque la factura no tiene cargada '
             'la SO correspondiente en el documento origen.'
    )

    @api.multi
    @api.depends('origin')
    def _compute_work(self):
        for rec in self:
            so = rec.origin
            so_id = self.env['sale.order'].search([('name', '=', so)])
            rec.work = so_id.work if so_id else 'N/D'
