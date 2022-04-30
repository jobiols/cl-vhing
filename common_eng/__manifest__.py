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
    "name": "Common Eng",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Project common featuers",
    "development_status": "Production/Stable",
    "author": "jeo Software",
    "depends": [
        "sale",
        "purchase",
        "project",

        "l10n_ar_aeroo_stock",
        "hr_timesheet",
        "sale_timesheet",
        "analytic",
        "website_quote",
        "project_timeline",  # Vista gantt de las tareas

    ],
    "data": [],
    "demo": [],
    "test": [],
    "installable": True,
    "application": False,
}
