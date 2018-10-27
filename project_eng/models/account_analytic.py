# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    asignee_id = fields.Many2one(
        'res.users',
        related="task_id.user_id"
    )

    name = fields.Char(
        required=False
    )

    @api.multi
    @api.depends('name')
    def name_get(self):
        result = []
        for aal in self:
            name = aal.task_id.name
            result.append((aal.id, name))
        return result
