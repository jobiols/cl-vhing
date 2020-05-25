# Copyright 2020 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project timeline fix",
    "summary": "Mejora algunos issues de usabilidad en project timeline",
    "version": "11.0.0.0.0",
    "development_status": "Alpha",  # "Alpha|Beta|Production/Stable|Mature"
    "category": "UX, Fix",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "project",
        'project_eng'
    ],
    "data": [
        'views/project_views.xml',
        'views/project_task_view.xml',
    ],
}
