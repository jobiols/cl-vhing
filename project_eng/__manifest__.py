# -----------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------
{
    'name': 'Project Eng',
    'version': '11.0.0.1.0',
    'license': 'AGPL-3',
    'category': 'Tools',
    'summary': 'Project enhacements for engineering',
    'author': 'jeo Software',
    'depends': [
        'hr_timesheet',
        'project',
        'purchase',
        'sale',
        'sale_timesheet',
        'analytic',

        'website_quote',  # dependencia para cargar demo data
    ],
    'data': [
        'views/project_view.xml',
        'views/purchase_view.xml',
        'views/timesheet_view.xml',
        'views/sale_views.xml',
        'wizard/project_task_invoice_wizard_views.xml',
        'views/custom_reports.xml',
        'views/project_view.xml',
        'views/res_partner.xml',
        'reports/purchase_order_templates.xml',
    ],
    'demo': [
        'demo/partner_demo.xml',
        'demo/product_data_demo.xml',
        'demo/sales_order_data_demo.xml',
    ],
    'test': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}
