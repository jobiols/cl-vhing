# For copyright and license notices, see __manifest__.py file in module root


def migrate(cr, version):
    cr.execute(
        """
          ALTER TABLE account_analytic_line
          DROP COLUMN amount;
        """)
