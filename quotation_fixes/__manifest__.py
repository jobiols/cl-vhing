# Copyright 2020 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Quotation Fixes",
    "summary": "Cambia la vista web de presupuesto",
    "version": "11.0.1.0.0",
    "development_status": "Production",
    "category": "UX, Fix",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "depends": [
        "project",
        #'project_eng_uy' no entiendo porque le habia puesto esto
    ],
    "data": [
        "views/website_quote_templates.xml",
    ],
    "application": False,
    "installable": True,
}
