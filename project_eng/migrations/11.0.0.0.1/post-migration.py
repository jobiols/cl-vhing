def migrate(cr, version):
    cr.execute(
        """
            UPDATE sale_order
            SET work = id
            WHERE work is null
        """)

    cr.execute(
        """
            UPDATE sale_order
            SET description = id
            WHERE description is null
        """)

    cr.execute(
        """
            UPDATE sale_order
            SET project_code = id
            WHERE project_code is null
        """)

    cr.execute(
        """
            UPDATE account_analytic_line
            SET name = id
            WHERE name is null
        """)

