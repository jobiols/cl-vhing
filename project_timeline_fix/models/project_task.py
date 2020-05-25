# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    level = fields.Integer(
        compute='_compute_level',
        help='Representa el nivel de la tarea',
    )

    def get_level(self, level):
        if not self.parent_id:
            return level
        else:
            return self.parent_id.get_level(level+1)

    @api.multi
    def _compute_level(self):
        for rec in self:
            rec.level = rec.get_level(0)
