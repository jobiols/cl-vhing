# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    work = fields.Char(

    )
