# -*- coding: utf-8 -*-

# Para ver print() en los logs en Docker
#import logging
#rom select import select

#_logger = logging.getLogger(__name__)
#_logger.info('Mensaje')
# ----------------------------------------


from email.policy import default
import string
from tokenize import group
from odoo import models, fields, api, exceptions
from datetime import *


def get_years():
    year_list = []
    for i in range(2022, 2050):
        year_list.append((str(i), str(i)))
    return year_list

class publicadores(models.Model):
     _name = 'secretary.publicadores'
     _description = 'Publicadores'
      


     name = fields.Char(string='Nombre completo', default="apellidos, nombre", required=True)
     fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
     fecha_bautismo = fields.Date(string='Fecha de bautismo')
     telefono = fields.Integer(string='Teléfono')
     genero = fields.Selection([('H','Hombre'), ('M','Mujer')], string='Género')
     direccion = fields.Char(string='Dirección')
     tipo = fields.Selection([('P','Publicador'), ('A', 'Auxiliar'), ('R','Regular')], string='Tipo', required=True)
     grupo = fields.Many2one(string='Grupo de Servicio', comodel_name="secretary.grupos")
     email = fields.Char(string='Email')
     image = fields.Binary(string='Imagen')
     activo = fields.Boolean(string='Activo', default='True', readonly=True)
     informe_id = fields.One2many("secretary.informes", "nombre", string="Mis Informes")





     def f_activo(self):
        self.activo = not self.activo




class grupos(models.Model):
    _name = 'secretary.grupos'
    _description = 'Grupos de Servicio'

    id = fields.Integer(string= 'Nombre', default=lambda self: self.env['ir.sequence'].next_by_code('increment_your_field'))
    name = fields.Integer(string='Nombre', related="id")
    responsable = fields.Many2one('secretary.publicadores', string="Superintendente de Grupo ")
    def name_get(self):
        result = []
        for g in self:
            name = 'Grupo #%s' % (g.name)
            result.append((g.id, name))
        return result
        





class informes(models.Model):
     _name = 'secretary.informes'
     _description = 'Informe de predicación'
     _rec_name = 'fecha'

     #current_year = fields.Integer(string="Año actual", default=datetime.now().year)
     #current_year = str(current_year)
      
     @api.onchange('mes')
     def _get_publicadores_por_informar(self):
        print("[*] Fecha-->", self.fecha, flush=True)
        pub_ya_informado = []
        if self.fecha != False:
            pub_con_informe = self.env['secretary.publicadores'].search([('informe_id.fecha','=',self.fecha)])
            for x in pub_con_informe:
                pub_ya_informado.append(x.id)
            print(pub_ya_informado, flush=True)
            return {'domain':{'nombre':[('id','!=',pub_ya_informado)]}}
        else:
            pass

     
     nombre = fields.Many2one("secretary.publicadores", string='Publicador')
     tipo_publicador = fields.Selection(string= "Tipo de publicador", related='nombre.tipo')
     mes = fields.Selection([('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'),('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'),('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'), ], string='Mes', default=lambda self: str((date.today().month)-1))
     current_year = datetime.strftime(datetime.today(),'%Y')
     fecha = fields.Char(compute="_compute_date", store=True)
     año = fields.Selection(get_years(), string='Año', default=current_year)
     horas = fields.Integer(string='Horas', required=True)
     revisitas = fields.Integer(string="Revisitas")
     cursos = fields.Integer(string="Cursos Bíblicos")
     publicaciones = fields.Integer(string="Publicaciones")
     videos = fields.Integer(string="Videos")
     revisitas = fields.Integer(string="Revisitas")
     notas = fields.Text(string='Notas:')
     este_mes_aux = fields.Boolean(string = "Aux. 30/50 horas", readonly=True) #TODO: Integrarlo cuadno se filtre campos para mayor comodida y estetica
     tipo_informe = fields.Selection([('P','Publicador'), ('A', 'Auxiliar'), ('R','Regular')], string= "Tipo de Informe", default='P')

                 
     def este_mes_aux_activo(self):
        self.este_mes_aux = not self.este_mes_aux     

     @api.depends("mes")
     def _compute_date(self):
        for record in self:
            record.fecha = "%s-%s" %(record.mes,record.año)

     @api.onchange('nombre')
     def _set_tipo_informe(self):
        print("Toc,toc", self.nombre.tipo, flush=True)
        if self.nombre.tipo != False:
            self.tipo_informe = "%s" %(self.nombre.tipo)
        else:
            pass

     @api.constrains('horas')
     def _validate_horas(self):
        if self.horas <= 0:
            raise exceptions.ValidationError('¡CUIDADO: EL valor de las HORAS no debe de ser menor a 0!')

   
     _sql_constraints = [
        ('nombre_unique', 'unique(nombre, mes, año)', '¡Solo puede introducir un informe por publicador!')
    ]

class informes_dashboard(models.Model):
    _name = 'secretary.informes_dashboard'
    _inherits = {'secretary.informes': 'mes_id'}

    mes_id = fields.Many2one('secretary.informes', ondelete='cascade', string= 'Mes')




# MODELO PARA REPORTE REGISTRO DE PUBLICADOR (S-21).    
class RegistroPublicador(models.TransientModel):
    _name = 'secretary.registro_publicador_report'
    _description = 'Formularios de Registro de publicador de la congregación (S-21)'
   # _inherit = 'secretary.informes'
   # _auto = False
   # _rec_name = 'id'
    def _año_servicio_sort(self):
        informes = self.env['secretary.informes'].search([])
        informes_sorted = informes.sorted(key= lambda i : i.año ,reverse=True)
        menu_año = []
        for informe in informes_sorted:
            menu_año.append((informe.año, informe.año))
        menu_año = list(dict.fromkeys(menu_año))
        print(menu_año, flush=True)
        return menu_año

    año_servicio = fields.Selection(_año_servicio_sort, string= "Seleccione año de servicio a generar reporte")
   
    def print_report_formularios_registro_publicador(self):
        return self.env.ref('secretary.action_registroPublicador_report').report_action(self)

    def get_publicadores_por_año(self):
        lista_por_año = self.env['secretary.publicadores'].search([('informe_id.año','=',self.año_servicio),])
        print("Debug: lista_por_año_____________",lista_por_año, flush=True)
        #for publicador in lista_por_año:
        #    print("Debug: nombre______", publicador.grupo[0]['name'], flush=True)
        return lista_por_año

    def lista_meses_con_informes(self):
        meses = self.env['secretary.informes'].search([('año','=',self.año_servicio)])
        print("meses---->",meses,flush=True)
        meses_sorted = meses.sorted(key= lambda i : i.mes ,reverse=True)
        lista_meses_con_informes = []
        for mes in meses_sorted:
            lista_meses_con_informes.append(int(mes.mes))
        lista_meses_con_informes = list(dict.fromkeys(lista_meses_con_informes))
        lista_meses_con_informes.sort()
        print(lista_meses_con_informes, flush=True)
        return lista_meses_con_informes

    def test(self):
        lista = [8,9,10,11]
        for l in lista:
            self.get_informes_por_tipo(l)
            
    def get_informes_por_tipo(self,x):
        mes=x
        grouped = self.env['secretary.informes'].read_group(
                [('fecha', '=', '%s-%s' %(mes,self.año_servicio)),],# WHERE
                [('horas:sum'),('publicaciones:sum'),('videos:sum'),('revisitas:sum'),('cursos:sum')], # FUNCTION IN SELECT; SELECT SUM (cv) AS total
                ['tipo_informe'] # GROUPBY
            )
        print("mes es --->",mes, flush=True)
        print("totales por mes--->",grouped, flush=True)
            
        return grouped # devuelve array de tuplas




# MODELO PARA REPORTE TOTALES DEL MES       
class TotalesMensuales(models.TransientModel):
    _name = 'secretary.totales_mensuales_report'
    _description = 'Totales mensuales de la predicación'
   # _inherit = 'secretary.informes'
   # _auto = False
   # _rec_name = 'id'

   
    def _informe_sort(self):
        informes = self.env['secretary.informes'].search([])
        informes_sorted = informes.sorted(key= lambda i : i.fecha ,reverse=True)
        menu_fecha = []
        for informe in informes_sorted:
            menu_fecha.append((informe.fecha, informe.fecha))
        menu_fecha = list(dict.fromkeys(menu_fecha))
        return menu_fecha

    mes_seleccionado = fields.Selection(_informe_sort, string = "Escoga mes para generar informe", required = True)
    
    def print_report_totales_mensuales(self):
        return self.env.ref('secretary.action_totalesMensuales_report').report_action(self)

    def get_sum_totales_mensuales(self):
        grouped = self.env['secretary.informes'].read_group(
            [('fecha', '=', self.mes_seleccionado),],# WHERE
            [('horas:sum'),('publicaciones:sum'),('videos:sum'),('revisitas:sum'),('cursos:sum')], # FUNCTION IN SELECT; SELECT SUM (cv) AS total
            ['tipo_informe'] # GROUPBY
        )
        print(grouped, flush=True)
        return grouped # devuelve array de tuplas

    def get_totales(self):
        total = self.env['secretary.informes'].read_group(
            [('fecha', '=', self.mes_seleccionado),],
            [('horas:sum'),('publicaciones:sum'),('videos:sum'),('revisitas:sum'),('cursos:sum')], 
            ['fecha']
        )
        return total

    def get_publicadores_activos(self):
        p_activos = self.env['secretary.informes'].read_group(
            [('horas', '>', 0),],
            [('nombre:array_agg')], 
            ['fecha']
        )
        print(p_activos, flush=True)
        return self.filtrar_ultimos_meses(p_activos)

    def filtrar_ultimos_meses(self, lista):
        count = []
        for i in range(-6, 0):
            try:
                valor = lista[i]['nombre']
            except IndexError:
                valor = None
            if valor != None:
                count.extend(valor)
        return len(set(count))

    def get_publicadores_irregulares(self):
        lista_conInforme = self.env['secretary.publicadores'].search([('informe_id.fecha','=',self.mes_seleccionado)])
        lista_total = self.env['secretary.publicadores'].search([])
        print("Debug: lista_conInforme_____________",lista_conInforme, flush=True)
        print("Debug: lista_total_____________",lista_total, flush=True)
        lista_irregulares = lista_total - lista_conInforme
        print("Debug: lista_irregulares_____________",lista_irregulares, flush=True)

        for publicador in lista_irregulares:
            print("Debug: nombre______", publicador.grupo[0]['name'], flush=True)
        return lista_irregulares
        

# MODELO PARA REPORTE TOTALES POR GRUPOS DE SERVICIO       
class TotalesMensuales(models.TransientModel):
    _name = 'secretary.totales_porgrupo_report'
    _description = 'Totales por grupo de servicio'
   # _inherit = 'secretary.informes'
   # _auto = False
   # _rec_name = 'id'

   
    def _grupo_sort(self):
        grupos = self.env['secretary.grupos'].search([])
        menu_grupo = []
        for grupo in grupos:
            menu_grupo.append((grupo.id, 'Grupo_'+ str(grupo.name)))
        return menu_grupo

    grupo_seleccionado = fields.Selection(_grupo_sort, string = "Escoga grupo para generar informe", required = True)
    
    def print_report_totales_porgrupo(self):
        return self.env.ref('secretary.action_totalesporGrupo_report').report_action(self)



    def get_publicadores_porgrupo(self):
        lista_porgrupos = self.env['secretary.publicadores'].search([('grupo','=',self.grupo_seleccionado),])
        print("Debug: lista_porgrupos_____________",lista_porgrupos, flush=True)
        #for publicador in lista_porgrupos:
        #    print("Debug: nombre______", publicador.grupo[0]['name'], flush=True)
        return lista_porgrupos
        
         
 
# MODELO PARA REPORTE TARJETA DE PUBLICADORES       
class InformesReport(models.AbstractModel):
    _name='report.secretary.informe_mensual'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('secretary.report_tarjeta_publicador')
        return {
            'doc_ids': docids,
            'doc_model': self.env['secretary.publicadores'],
            'docs': self.env['secretary.publicadores'].browse(docids)
        }




