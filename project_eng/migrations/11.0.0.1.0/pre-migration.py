# For copyright and license notices, see __manifest__.py file in module root
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    """ Recalcular todas las analiticas que vienen de las facturas.
    """
    aml_obj = env['account.move.line']
    amls = aml_obj.search([])
    for aml in amls:
        aml.create_analytic_lines()
