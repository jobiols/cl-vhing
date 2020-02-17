# Part of Odoo. See LICENSE file for full copyright and licensing details.
from __future__ import division

from openerp.tests.common import TransactionCase


#   Forma de correr el test
#   -----------------------
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben empezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos no importa el nombre (por ejemplo
#   bulonfer_test) vacia y con el modulo que se va a testear instalado
#   (por ejemplo product_autoload).
#
#   El usuario admin tiene que tener password admin, Language English, Country
#   United States.
#
#   Correr el test con:
#
#   oe -Q project_eng -c vhing -d vhing_test
#


class TestProjectEng(TransactionCase):
    """ Cada metodo de test corre en su propia transacción y se hace rollback
        despues de cada uno.
    """

    def setUp(self):
        """ Este setup corre antes de cada método ---------------------------00
        """
        super(TestProjectEng, self).setUp()

        project_obj = self.env['project.project']
        project_task_obj = self.env['project.task']
        aal_obj = self.env['account.analytic.line']

        # confirmar las dos so
        def confirm_SO(name):
            so_obj = self.env['sale.order']
            so = so_obj.search([('name', '=', name)])
            so.action_confirm()

        confirm_SO('SO0001')
        confirm_SO('SO0002')

        # asignar las cuatro tareas y ponerle precio
        tasks = project_task_obj.search(
            [('project_id.name', 'in', ['32828-190102', '20367-180614'])])
        price = 10
        for task in tasks:
            task.user_id = self.env.ref('base.res_users2')
            price += 10
            task.cost_price = price

        def create_analitic_line(project, task, amount):

            # busco el project y la task
            project_id = project_obj.search([('name', '=', project)])
            task_id = project_task_obj.search([('name', '=', task)])

            # creo las horas en la analitica
            vals = {
                'project_id': project_id.id,
                'task_id': task_id.id,
                'unit_amount': amount
            }
            aal_obj.create(vals)

        create_analitic_line(
            '32828-190102',
            'SO0001:[IHA] Diseño y cálculo de la '
            'estructura de hormigón armado',
            30
        )
        create_analitic_line(
            '32828-190102',
            'SO0001:[IPV] Diseño de pavimentos',
            40
        )
        create_analitic_line(
            '20367-180614',
            'SO0002:[IME] Diseño y cálculo de la '
            'estructura metálica de cubierta',
            40
        )
        create_analitic_line(
            '20367-180614',
            'SO0002:[IHA] Diseño y cálculo de la '
            'estructura de hormigón armado',
            40
        )

    def test_01_crear_oc(self):
        """ crear ordenes de compra
        """
        # obtener la ultima orden de compra
        po_obj = self.env['purchase.order']
        last_po = po_obj.search([], limit=1, order='id desc')

        # obtener las aal para pasarle al wizard
        aal_obj = self.env['account.analytic.line']
        aal_ids = aal_obj.search([('task_id.name', 'like', 'SO000')])

        wizard = self.env['project.task.invoice.wizard']
        wiz = wizard.create({
            'aal_ids': [(6, 0, [aal.id for aal in aal_ids])]
        })
        wiz.invoice_tasks()

        # obtener las po agregadas
        po = po_obj.search([('id', '>', last_po.id)])
        self.assertEqual(len(po), 1)

        self.assertEqual(po.partner_id.name, 'Nicolas Francisco Diez')
