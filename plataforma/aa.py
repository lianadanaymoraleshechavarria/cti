
@method_decorator([login_required, pure_admin_required ], name='dispatch')
class Dashboard_Admin(LoginRequiredMixin, TemplateView):
    template_name = 'Plataforma/dashboard_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investigadores = Perfil.objects.all
        investigador_count = Usuario.objects.all

        # Calcula los totales para todo el sistema
        total_articulos = Articulo.objects.count()
        total_premios = Premio.objects.count()
        total_proyectos = Proyecto.objects.count()
        total_eventos = Evento.objects.count()

        data_grafica_investigadores = Perfil.objects.values('area').annotate(count=Count('id')).order_by('area')

        # Calcula los totales de estados pendientes para todos los modelos
        total_articulos_pendientes = Articulo.objects.filter(aprobacion='Pendiente').count()
        total_premios_pendientes = Premio.objects.filter(aprobacion='Pendiente').count()
        total_proyectos_pendientes = Proyecto.objects.filter(aprobacion='Pendiente').count()
        total_eventos_pendientes = Evento.objects.filter(aprobacion='Pendiente').count()
        total_programas_pendientes = Programa.objects.filter(aprobacion='Pendiente').count()

        # Calcula los premios aprobados por area
        premios_aprobados_por_area = Premio.objects.filter(aprobacion='Aprobado').count()

        # Agrega estos datos al contexto
        context['investigadores'] = investigadores
        context['investigador_count'] = investigador_count
        context['total_articulos'] = total_articulos
        context['total_premios'] = total_premios
        context['total_proyectos'] = total_proyectos
        context['total_eventos'] = total_eventos
        context['data_grafica_investigadores'] = list(data_grafica_investigadores)
        context['total_articulos_pendientes'] = total_articulos_pendientes
        context['total_premios_pendientes'] = total_premios_pendientes
        context['total_proyectos_pendientes'] = total_proyectos_pendientes
        context['total_eventos_pendientes'] = total_eventos_pendientes
        context['total_programas_pendientes'] = total_programas_pendientes

         # Datos para el gráfico de pastel
        context['datos_gráfico_pendientes'] = {
            'Artículos': total_articulos_pendientes,
            'Premios': total_premios_pendientes,
            'Proyectos': total_proyectos_pendientes,
            'Eventos': total_eventos_pendientes,
            'Programas': total_programas_pendientes,
        }
        context['total_usuarios'] = Usuario.objects.count()
         # Datos para el gráfico de barras
        context['premios_aprobados_por_area'] = premios_aprobados_por_area
      
        
        # Añadir información de notificaciones
        if hasattr(self.request.user, 'notificaciones'):
            context['tiene_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).exists()
            context['contador_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).count()
        else:
            context['tiene_notificaciones_no_leidas'] = False
            context['contador_notificaciones_no_leidas'] = 0
            
        return context


        @method_decorator([login_required, jefedepartamento_required], name='dispatch')
class Dashboard_JefeDepartamento(LoginRequiredMixin, TemplateView):
    template_name = 'JefeDepartamento/dashboard_jefedepartamento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el perfil y el departamento del usuario actual (Jefe de Departamento)
        perfil_JefeDepartamento = Perfil.objects.get(usuario=self.request.user)
        departamento_JefeDepartamento = perfil_JefeDepartamento.departamento

        # Filtrar investigadores del mismo departamento
        investigadores = Perfil.objects.filter(departamento=departamento_JefeDepartamento)

        # Filtrar artículos, premios, proyectos y eventos del mismo departamento
        total_articulos = Articulo.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').count()
        total_premios = Premio.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').count()
        total_proyectos = Proyecto.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').count()
        total_eventos = Evento.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').count()

        # Filtrar estados pendientes para el departamento
        total_articulos_pendientes = Articulo.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').count()
        total_premios_pendientes = Premio.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').count()
        total_proyectos_pendientes = Proyecto.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').count()
        total_eventos_pendientes = Evento.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').count()
        total_programas_pendientes = Programa.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Pendiente').count()

        # Datos para la gráfica de investigadores por área dentro del departamento
        data_grafica_investigadores = Perfil.objects.filter(departamento=departamento_JefeDepartamento).values('area').annotate(count=Count('id')).order_by('area')
        
        # Si no hay datos por área, usar el departamento como categoría
        if not data_grafica_investigadores:
            data_grafica_investigadores = [{'departamento': str(departamento_JefeDepartamento), 'count': investigadores.count()}]

        # Datos para la gráfica de premios aprobados por área dentro del departamento
        premios_aprobados_por_departamento = Premio.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').values('area').annotate(count=Count('id')).order_by('area')
        
        # Si no hay datos por área, usar el departamento como categoría
        if not premios_aprobados_por_departamento:
            premios_aprobados_por_departamento = [{'departamento': str(departamento_JefeDepartamento), 'count': Premio.objects.filter(departamento=departamento_JefeDepartamento, aprobacion='Aprobado').count()}]

        # Agregar los datos al contexto
        context['investigadores'] = investigadores
        context['total_articulos'] = total_articulos
        context['total_premios'] = total_premios
        context['total_proyectos'] = total_proyectos
        context['total_eventos'] = total_eventos
        context['data_grafica_investigadores'] = list(data_grafica_investigadores)
        context['total_articulos_pendientes'] = total_articulos_pendientes
        context['total_premios_pendientes'] = total_premios_pendientes
        context['total_proyectos_pendientes'] = total_proyectos_pendientes
        context['total_eventos_pendientes'] = total_eventos_pendientes
        context['total_programas_pendientes'] = total_programas_pendientes

        # Datos para el gráfico de pastel (solo el departamento actual)
        context['datos_gráfico_pendientes'] = {
            'Artículos': total_articulos_pendientes,
            'Premios': total_premios_pendientes,
            'Proyectos': total_proyectos_pendientes,
            'Eventos': total_eventos_pendientes,
            'Programas': total_programas_pendientes,
        }

        # Datos para el gráfico de barras (solo el departamento actual)
        context['premios_aprobados_por_departamento'] = list(premios_aprobados_por_departamento)
        
        # Añadir información de notificaciones
        if hasattr(self.request.user, 'notificaciones'):
            context['tiene_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).exists()
            context['contador_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).count()
        else:
            context['tiene_notificaciones_no_leidas'] = False
            context['contador_notificaciones_no_leidas'] = 0
            
        return context



@method_decorator([login_required, jefearea_required ], name='dispatch')
class Dashboard_JefeArea(LoginRequiredMixin, TemplateView):
    template_name = 'JefeArea/dashboard_JefeArea.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil_JefeArea = self.request.user
        
        area_JefeArea = perfil_JefeArea.area
        investigadores =Perfil.objects.filter(area=area_JefeArea)

        # Calcula los totales para todo el sistema
        total_articulos = Articulo.objects.filter(area=area_JefeArea, aprobacion='Aprobado').count()
        total_premios = Premio.objects.filter(area=area_JefeArea, aprobacion='Aprobado').count()
        total_proyectos = Proyecto.objects.filter(area=area_JefeArea, aprobacion='Aprobado').count()
        total_eventos = Evento.objects.filter(area=area_JefeArea, aprobacion='Aprobado').count()

        data_grafica_investigadores = Perfil.objects.values('area').annotate(count=Count('id')).order_by('area')

        # Calcula los totales de estados pendientes para todos los modelos
        total_articulos_pendientes = Articulo.objects.filter(aprobacion='Pendiente').count()
        total_premios_pendientes = Premio.objects.filter(aprobacion='Pendiente').count()
        total_proyectos_pendientes = Proyecto.objects.filter(aprobacion='Pendiente').count()
        total_eventos_pendientes = Evento.objects.filter(aprobacion='Pendiente').count()
        total_programas_pendientes = Programa.objects.filter(aprobacion='Pendiente').count()

        # Calcula los premios aprobados por area
        premios_aprobados_por_area = Premio.objects.filter(aprobacion='Aprobado').values('area').annotate(count=Count('id')).order_by('area')
        # 3. Eventps aprobados por área
        eventos_aprobados_por_area = Evento.objects.filter(aprobacion='Aprobado').values('area').annotate(count=Count('id')).order_by('area')
        # 3. Artículos aprobados por área
        articulos_aprobados_por_area = Articulo.objects.filter(aprobacion='Aprobado').values('area').annotate(count=Count('id')).order_by('area')

        # Agrega estos datos al contexto
        context['investigadores'] = investigadores
        context['total_articulos'] = total_articulos
        context['total_premios'] = total_premios
        context['total_proyectos'] = total_proyectos
        context['total_eventos'] = total_eventos
        context['data_grafica_investigadores'] = list(data_grafica_investigadores)
        context['total_articulos_pendientes'] = total_articulos_pendientes
        context['total_premios_pendientes'] = total_premios_pendientes
        context['total_proyectos_pendientes'] = total_proyectos_pendientes
        context['total_eventos_pendientes'] = total_eventos_pendientes
        context['total_programas_pendientes'] = total_programas_pendientes

         # Datos para el gráfico de pastel
        context['datos_gráfico_pendientes'] = {
            'Artículos': total_articulos_pendientes,
            'Premios': total_premios_pendientes,
            'Proyectos': total_proyectos_pendientes,
            'Eventos': total_eventos_pendientes,
            'Programas': total_programas_pendientes,
        }
         # Datos para el gráfico de barras
        context['premios_aprobados_por_area'] = list(premios_aprobados_por_area)
        context['eventos_aprobados_por_area'] = list(eventos_aprobados_por_area)
        context['articulos_aprobados_por_area'] = list(articulos_aprobados_por_area)
        
        # Corregido: usar self.request.user en lugar de user
        if hasattr(self.request.user, 'notificaciones'):
            context['tiene_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).exists()
            context['contador_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).count()
        else:
            context['tiene_notificaciones_no_leidas'] = False
            context['contador_notificaciones_no_leidas'] = 0
            
        return context


@method_decorator([login_required, vicerrector_required ], name='dispatch')
class Dashboard_Vicerrector(LoginRequiredMixin, TemplateView):
    template_name = 'Vicerrector/dashboard_vicerrector.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investigadores = Perfil.objects.all

        # Calcula los totales para todo el sistema
        total_articulos = Articulo.objects.count()
        total_premios = Premio.objects.count()
        total_proyectos = Proyecto.objects.count()
        total_eventos = Evento.objects.count()

        data_grafica_investigadores = Perfil.objects.values('area').annotate(count=Count('id')).order_by('area')

        # Calcula los totales de estados pendientes para todos los modelos
        total_articulos_pendientes = Articulo.objects.filter(aprobacion='Pendiente').count()
        total_premios_pendientes = Premio.objects.filter(aprobacion='Pendiente').count()
        total_proyectos_pendientes = Proyecto.objects.filter(aprobacion='Pendiente').count()
        total_eventos_pendientes = Evento.objects.filter(aprobacion='Pendiente').count()
        total_programas_pendientes = Programa.objects.filter(aprobacion='Pendiente').count()

        # Calcula los premios aprobados por areas
        premios_aprobados_por_area = Premio.objects.filter(aprobacion='Aprobado').values('area').annotate(count=Count('id')).order_by('area')

        premios_aprobados_por_area = Premio.objects.filter(aprobacion='Aprobado') \
            .values('area') \
            .annotate(count=Count('id')) \
            .order_by('area')
        
        # Convertir a formato compatible con Highcharts
        premios_data = [
            {'area': item['area'], 'count': item['count']} 
            for item in premios_aprobados_por_area
        ]
        

        # Agrega estos datos al contexto
        context['investigadores'] = investigadores
        context['total_articulos'] = total_articulos
        context['total_premios'] = total_premios
        context['total_proyectos'] = total_proyectos
        context['total_eventos'] = total_eventos
        context['data_grafica_investigadores'] = list(data_grafica_investigadores)
        context['total_articulos_pendientes'] = total_articulos_pendientes
        context['total_premios_pendientes'] = total_premios_pendientes
        context['total_proyectos_pendientes'] = total_proyectos_pendientes
        context['total_eventos_pendientes'] = total_eventos_pendientes
        context['total_programas_pendientes'] = total_programas_pendientes

         # Datos para el gráfico de pastel
        context['datos_gráfico_pendientes'] = {
            'Artículos': total_articulos_pendientes,
            'Premios': total_premios_pendientes,
            'Proyectos': total_proyectos_pendientes,
            'Eventos': total_eventos_pendientes,
            'Programas': total_programas_pendientes,
        }
         # Datos para el gráfico de barras
        context['premios_aprobados_por_area'] = list(premios_aprobados_por_area)
        
        # Añadir información de notificaciones
        if hasattr(self.request.user, 'notificaciones'):
            context['tiene_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).exists()
            context['contador_notificaciones_no_leidas'] = self.request.user.notificaciones.filter(leida=False).count()
        else:
            context['tiene_notificaciones_no_leidas'] = False
            context['contador_notificaciones_no_leidas'] = 0
            
        return context
