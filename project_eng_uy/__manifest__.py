# -----------------------------------------------------------------------------
#
#    Copyright (C) 2020  jeo Software  (http://www.jeosoft.com.ar)
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
    "name": "Project Eng uy",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Project enhacements for engineering",
    "development_status": "Production/Stable",
    "author": "jeo Software",
    "depends": [
        "sale",
        "account_cancel",
        "common_eng",
        'quotation_fixes',
        "report_aeroo",  # dependencia para el reporte po modificado
        "project_timeline",  # Vista gantt de las tareas
        'common_eng',
    ],
    "data": [
        "views/sale_views.xml",
        "views/account_invoice_view.xml",
    ],
    "demo": [],
    "test": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": [],
}
