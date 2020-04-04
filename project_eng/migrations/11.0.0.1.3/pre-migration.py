# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root


def migrate(cr, version):
    """ Eliminar la columna para que recalcule el campo calculado
    """
    cr.execute(
        """
            ALTER TABLE account_analytic_line
            DROP COLUMN task_cost;
        """)
