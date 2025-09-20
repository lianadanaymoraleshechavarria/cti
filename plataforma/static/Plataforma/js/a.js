/**
 * Script para manejar filtros dependientes en DataTables
 * Este script puede ser reutilizado en diferentes tablas
 */

class FiltrosDependientes {
    constructor(options) {
      this.tableId = options.tableId
      this.filtroAreaId = options.filtroAreaId || "filtro-area"
      this.filtroDepartamentoId = options.filtroDepartamentoId || "filtro-departamento"
      this.btnLimpiarId = options.btnLimpiarId || "btn-limpiar-filtros"
      this.columnaArea = options.columnaArea || 4
      this.columnaDepartamento = options.columnaDepartamento || 5
  
      this.init()
    }
  
    init() {
      const self = this
  
      // Crear un select oculto con todos los departamentos para referencia
      const departamentosHidden = $('<select id="filtro-departamento-hidden" style="display:none;"></select>')
      $(`#${this.filtroDepartamentoId} option`).each(function () {
        departamentosHidden.append($(this).clone())
      })
      $("body").append(departamentosHidden)
  
      // Obtener referencia a la tabla DataTable
      this.table = $(`#${this.tableId}`).DataTable()
  
      // Evento de cambio en el filtro de área
      $(`#${this.filtroAreaId}`).on("change", function () {
        const areaSeleccionada = $(this).val()
  
        // Actualizar departamentos disponibles
        self.actualizarDepartamentos()
  
        // Aplicar filtro a la tabla
        self.table.column(self.columnaArea).search(areaSeleccionada).draw()
      })
  
      // Evento de cambio en el filtro de departamento
      $(`#${this.filtroDepartamentoId}`).on("change", function () {
        const departamentoSeleccionado = $(this).val()
        self.table.column(self.columnaDepartamento).search(departamentoSeleccionado).draw()
      })
  
      // Botón para limpiar filtros
      $(`#${this.btnLimpiarId}`).on("click", () => {
        // Limpiar selecciones
        $(`#${self.filtroAreaId}`).val("")
        $(`#${self.filtroDepartamentoId}`).val("")
  
        // Restaurar todos los departamentos
        self.actualizarDepartamentos()
  
        // Limpiar filtros de la tabla
        self.table.column(self.columnaArea).search("").column(self.columnaDepartamento).search("").draw()
      })
    }
  
    actualizarDepartamentos() {
      const areaSeleccionada = $(`#${this.filtroAreaId}`).val()
      const departamentoSelect = $(`#${this.filtroDepartamentoId}`)
  
      // Guardar el valor actual del departamento
      const valorActual = departamentoSelect.val()
  
      // Limpiar el select de departamentos
      departamentoSelect.empty()
      departamentoSelect.append('<option value="">Todos los departamentos</option>')
  
      // Si no hay área seleccionada, mostrar todos los departamentos
      if (!areaSeleccionada) {
        $("#filtro-departamento-hidden option").each(function () {
          if ($(this).val()) {
            // Excluir la opción vacía
            departamentoSelect.append($(this).clone())
          }
        })
      } else {
        // Filtrar departamentos por área
        $("#filtro-departamento-hidden option").each(function () {
          if ($(this).data("area") === areaSeleccionada || !$(this).val()) {
            departamentoSelect.append($(this).clone())
          }
        })
      }
  
      // Intentar restaurar el valor anterior si existe en las nuevas opciones
      if (valorActual && departamentoSelect.find(`option[value="${valorActual}"]`).length > 0) {
        departamentoSelect.val(valorActual)
      }
    }
  }
  
  // Uso:
  document.addEventListener("DOMContentLoaded", () => {
    new FiltrosDependientes({
      tableId: "Articulos",
      filtroAreaId: "filtro-area",
      filtroDepartamentoId: "filtro-departamento",
      btnLimpiarId: "btn-limpiar-filtros",
      columnaArea: 4,
      columnaDepartamento: 5,
    })
  })
  