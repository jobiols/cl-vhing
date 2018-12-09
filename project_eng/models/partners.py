# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root


from odoo import api, fields, models


class ResPartners(models.Model):
    _inherit = 'res.partners'

    initials = fields.Char(
        compute="_compute_initials",
        readonly=True,
        help="Iniciales del partner"
    )

    @api.depends('name')
    def _compute_initials(self):
        for partner in self:
            name_list = partner.name.split()
            initials = ""
            for name in name_list:
                initials += name[0].upper()
            partner.initials = initials
