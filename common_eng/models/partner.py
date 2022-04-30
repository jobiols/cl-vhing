# For copyright and license notices, see __manifest__.py file in module root


from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    initials = fields.Char(
        compute="_compute_initials",
        readonly=True,
        help="Iniciales del partner",
        store=True
    )
    """
    _sql_constraints = [('unique_initials',
                         'UNIQUE(initials)',
                         'Please check partner''s Name, the initials '
                         'must be unique. Is it a coincidence or is it '
                         'loading twice?')]
    """
    @api.depends('name')
    def _compute_initials(self):
        """ Calcula las iniciales basado en el nombre del partner
        """
        for partner in self:
            if not partner.name:
                return
            name_list = partner.name.split()
            initials = map(lambda x: x[0].upper(), name_list)
            partner.initials = ''.join(initials)
