# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from datetime import date


class PartnerMatchingWizard(models.TransientModel):
    _name = 'matching.wizard'

    feh_account_id = fields.Float(
        default=lambda self: self._get_account_feh(),
        readonly=True
    )
    jav_account_id = fields.Float(
        default=lambda self: self._get_account_jav(),
        readonly=True
    )
    difference = fields.Float(
        default=lambda self: self._get_difference(),
        readonly=True,
        string="FEH - JAV"
    )

    @api.multi
    def _get_difference(self):
        return self._get_account_feh() - self._get_account_jav()

    @api.multi
    def _get_balance(self, account_id):

        date_today = date.today().strftime('%Y-%m-%d')
        trial_balance = self.env['report.account.report_trialbalance']
        trial = trial_balance.with_context(date_to=date_today)
        account_res = trial._get_accounts(account_id, 'movement')
        cash = 0
        for account in account_res:
            cash += account['balance']

        return cash

    @api.multi
    def _get_account_feh(self):
        domain = [('code', '=', '1.2.02.01.040')]
        feh_id = self.env['account.account'].search(domain)

        return self._get_balance(feh_id)

    @api.multi
    def _get_account_jav(self):
        domain = [('code', '=', '1.2.02.01.041')]
        jav_id = self.env['account.account'].search(domain)

        return self._get_balance(jav_id)
