# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root


def migrate(cr, version):
    cr.execute(
        """
            ALTER TABLE project_project
            DROP COLUMN work;
        """)
