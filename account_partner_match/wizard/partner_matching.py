# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PartnerMatchingWizard(models.TransientModel):
    _name = 'matching.wizard'

    FEH_account_id = fields.Many2one(
        default="_get_account_feh"
    )
    JAV_account_id = fields.Many2one(
        default="_get_account_jav"

    )

    def _get_account_feh(self):
        domain = ['name', '=', '1.2.02.01.041']
        feh_id = self.env['account.account'].search(domain)
        return feh_id

    def _get_account_jav(self):
        domain = ['name', '=', '1.2.02.01.040']
        jav_id = self.env['account.account'].search(domain)
        return jav_id
