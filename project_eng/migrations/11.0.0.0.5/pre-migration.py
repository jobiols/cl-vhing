# For copyright and license notices, see __manifest__.py file in module root


def migrate(cr, version):
    cr.execute(
        """
            UPDATE account_analytic_line
            SET name = concat('FIX_', id)
            WHERE name is null
        """)
