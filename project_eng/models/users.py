# For copyright and license notices, see __manifest__.py file in module root


from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    initials = fields.Char(
        compute="_compute_initials",
        readonly=True,
        help="Iniciales del usuario"
    )

    @api.depends('name')
    def _compute_initials(self):
        for user in self:
            name_list = user.name.split()
            initials = ""
            for name in name_list:
                initials += name[0].upper()
            user.initials = initials
