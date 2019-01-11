# -----------------------------------------------------------------------------
#
#    Copyright (C) 2018  jeo Software  (http://www.jeosoft.com.ar)
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
    'name': 'vhing',
    'version': '11.0.0.0.0',
    'license': 'Other OSI approved licence',
    'category': 'Tools',
    'summary': 'Customizacion para VH Ingenieria',
    'author': 'jeo Software',
    'depends': [
        'sale_management',
        'account_invoicing',
        'purchase',
        'project',

        # desarrollados
        'project_eng',

        # para la localizacion argentina
        'l10n_ar_base',  # esto se instala solo
        'l10n_ar_account',  # esto se instala solo
        'l10n_ar_afipws_fe',  # Factura Electrónica Argentina
        'l10n_ar_aeroo_einvoice',  # impresion de factura electronica aeroo
        'l10n_ar_account_vat_ledger_citi',
        'account_debt_management',
        'l10n_ar_aeroo_payment_group',

        # utilitarios
        'auto_backup',  # poner el backup en: /var/odoo/backups/
        'backend_theme',
        'due_payments_argentina_fix'
    ],
    'data': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],

    'port': '8069',
    'repos': [
        {'usr': 'jobiols', 'repo': 'cl-vhing', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'rafi16jan-backend-theme', 'branch': '11.0'},

        {'usr': 'jobiols', 'repo': 'adhoc-odoo-argentina', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-argentina-sale', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-account-financial-tools',
         'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-account-payment', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-miscellaneous', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-argentina-reporting',
         'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-reporting-engine', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'adhoc-aeroo_reports', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'oca-partner-contact', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'oca-web', 'branch': '11.0'},
        {'usr': 'jobiols', 'repo': 'oca-server-tools', 'branch': '11.0'},
    ],
    'docker': [
        {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-jeo', 'ver': '11.0'},
        {'name': 'postgres', 'usr': 'postgres', 'ver': '9.6'},
        {'name': 'nginx', 'usr': 'nginx', 'ver': 'latest'},
        {'name': 'aeroo', 'usr': 'adhoc', 'img': 'aeroo-docs'},
    ]
}
