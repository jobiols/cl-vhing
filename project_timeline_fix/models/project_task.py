# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as FMT
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def adjust_task_start(self):
        for rec in self:
            for task in rec.task_ids:
                task.adjust_task_start()


class ProjectTask(models.Model):
    _inherit = 'project.task'

    level = fields.Integer(
        compute='_compute_level',
        help='Representa el nivel de la tarea',
        # store=True no funciona la recursion con store
    )

    def get_level(self, level):
        """ Funcion recursiva que calcula el nivel de una tarea
        """
        if not self.parent_id:
            return level
        else:
            return self.parent_id.get_level(level+1)

    @api.multi
    def _compute_level(self):
        for rec in self:
            rec.level = rec.get_level(0)

    @api.multi
    def adjust_task_start(self):
        """ funcion recursiva que ajusta todas las tareas a cualquier nivel
        """
        for rec in self:
            for dep in rec.dependency_task_ids:
                if not dep.date_end:
                    raise UserError(_('La tarea %s no tiene fecha de '
                                     'finalizacion' % dep.name))
                if not rec.date_start:
                    raise UserError(_('La tarea %s no tiene fecha de inicio'
                                     '' % rec.name))
                if dep.date_end > rec.date_start:
                    # dep es la tarea de la cual dependemos.
                    # rec es la tarea por la que pasa el bucle
                    # hay que correr rec para ponerla despues de dep

                    # calcular el corrimiento
                    dts = datetime.strptime(rec.date_start, FMT)
                    dte = datetime.strptime(dep.date_end, FMT)
                    shift = (dte-dts)

                    # calcular start y end de rec en datetime (el dts ya esta)
                    # dts = datetime.strptime(rec.date_start, FMT)
                    dte = datetime.strptime(rec.date_end, FMT)

                    # correr rec en shift segundos a la derecha
                    dts += timedelta(seconds=shift.total_seconds())
                    dte += timedelta(seconds=shift.total_seconds())

                    # verificar que dte > dts
                    if dte < dts:
                        dte = dts + timedelta(seconds=3600)

                    # pasar a texto
                    rec_start = datetime.strftime(dts, FMT)
                    rec_end = datetime.strftime(dte, FMT)

                    rec.write({
                        'date_start': rec_start,
                        'date_end': rec_end
                    })
                dep.adjust_task_start()
        else:
            return
