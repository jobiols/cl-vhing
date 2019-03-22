# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root


def migrate(cr, version):
    cr.execute(
        """
          ALTER TABLE account_analytic_line
          DROP column amount;

          UPDATE account_analytic_line
          SET name = cast(id as VARCHAR)
          WHERE name is NULL;
        """)
