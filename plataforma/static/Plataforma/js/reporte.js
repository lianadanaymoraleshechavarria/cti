$(document).ready(function() {
    // Inicializar Select2
    $(".select2").select2({
        theme: "bootstrap-5",
        width: "resolve",
    });

    // Inicializar Select2 con AJAX para usuarios
    $(".select2-ajax").select2({
        theme: "bootstrap-5",
        width: "resolve",
        ajax: {
            url: "{% url 'api_usuarios' %}",
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return {
                    search: params.term || '',
                };
            },
            processResults: function(data) {
                return {
                    results: $.map(data, function(item) {
                        return {
                            id: item.id,
                            text: item.name,
                            username: item.username
                        };
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 2,
        placeholder: "Buscar usuario...",
    });

    // Función para filtrar departamentos por área
    function setupAreaDepartamentoFilter(areaSelector, departamentoSelector) {
        $(areaSelector).on('change', function() {
            var areaId = $(this).val();
            var $departamentoSelect = $(departamentoSelector);
            
            if (!areaId) {
                $departamentoSelect.find('option').prop('disabled', false);
                $departamentoSelect.val('').trigger('change');
                return;
            }
            
            $departamentoSelect.find('option').each(function() {
                var $option = $(this);
                var departamentoAreaId = $option.data('area');
                
                if (!$option.val()) {
                    $option.prop('disabled', false);
                    return;
                }
                
                $option.prop('disabled', departamentoAreaId != areaId);
            });
            
            if ($departamentoSelect.find('option:selected').prop('disabled')) {
                $departamentoSelect.val('').trigger('change');
            }
        });
    }

    // Configurar filtros área-departamento para cada pestaña
    setupAreaDepartamentoFilter('#eventoArea', '#eventoDepartamento');
    setupAreaDepartamentoFilter('#proyectoArea', '#proyectoDepartamento');
    setupAreaDepartamentoFilter('#programaArea', '#programaDepartamento');
    setupAreaDepartamentoFilter('#premioArea', '#premioDepartamento');
    setupAreaDepartamentoFilter('#articuloArea', '#articuloDepartamento');

    // Inicializar DataTables con configuración común
    var commonConfig = {
        responsive: true,
        dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
             "<'row'<'col-sm-12'tr>>" +
             "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        language: { 
            url: "/static/libs/Datatable/dataTableLenguage.json" 
        },
        buttons: ["copy", "csv", "excel", "pdf", "print"],
        initComplete: function() {
            // Habilitar botones de exportación
            this.api().buttons().container().appendTo($('.export-buttons'));
        }
    };

    // Inicializar todas las tablas
    var eventosTable = $('#eventosTable').DataTable($.extend(true, {}, commonConfig, {
        columnDefs: [
            { targets: [3, 5, 6, 7], searchable: true }
        ]
    });

    var proyectosTable = $('#proyectosTable').DataTable($.extend(true, {}, commonConfig, {
        columnDefs: [
            { targets: [3, 5, 6, 8], searchable: true }
        ]
    });

    var programasTable = $('#programasTable').DataTable($.extend(true, {}, commonConfig, {
        columnDefs: [
            { targets: [3, 5, 6], searchable: true }
        ]
    }));

    var premiosTable = $('#premiosTable').DataTable($.extend(true, {}, commonConfig, {
        columnDefs: [
            { 
                targets: [5], 
                render: function(data, type, row) {
                    if (type === 'filter' || type === 'sort') {
                        return $(data).text();
                    }
                    return data;
                }
            }
        ]
    });
    
    var articulosTable = $('#articulosTable').DataTable($.extend(true, {}, commonConfig, {
        columnDefs: [
            { 
                targets: [7], 
                render: function(data, type, row) {
                    if (type === 'filter' || type === 'sort') {
                        return $(data).text();
                    }
                    return data;
                }
            }
        ]
    }));

    // Función para aplicar filtros a una tabla
    function applyTableFilters(table, filters) {
        table.columns().every(function() {
            var column = this;
            var columnIndex = column.index();
            var filterValue = filters[columnIndex];
            
            if (filterValue !== undefined && filterValue !== '') {
                column.search(filterValue, true, false).draw();
            } else {
                column.search('').draw();
            }
        });
    }

    // Función para limpiar filtros
    function clearFilters(selectors, table) {
        selectors.forEach(function(selector) {
            $(selector).val('').trigger('change');
        });
        table.search('').columns().search('').draw();
    }

    // Configurar filtros para Eventos
    $('#filtrarEventos').click(function() {
        var filters = {
            1: $('#eventoTipo').val(),      // Tipo
            3: $('#eventoCategoria').val(),  // Carácter
            5: $('#eventoArea').val(),       // Área
            6: $('#eventoDepartamento').val(), // Departamento
            7: $('#eventoUsuario').val()     // Responsable
        };
        applyTableFilters(eventosTable, filters);
    });

    $('#limpiarFiltrosEventos').click(function() {
        clearFilters(['#eventoTipo', '#eventoCategoria', '#eventoArea', '#eventoDepartamento', '#eventoUsuario'], eventosTable);
    });

    // Configurar filtros para Proyectos
    $('#filtrarProyectos').click(function() {
        var filters = {
            3: $('#proyectoTipo').val(),     // Tipo
            5: $('#proyectoArea').val(),     // Área
            6: $('#proyectoDepartamento').val(), // Departamento
            8: $('#proyectoUsuario').val()   // Responsable
        };
        applyTableFilters(proyectosTable, filters);
    });

    $('#limpiarFiltrosProyectos').click(function() {
        clearFilters(['#proyectoTipo', '#proyectoArea', '#proyectoDepartamento', '#proyectoUsuario'], proyectosTable);
    });

    // Configurar filtros para Programas
    $('#filtrarProgramas').click(function() {
        var filters = {
            3: $('#programaLinea').val(),    // Línea Investigación
            5: $('#programaArea').val(),     // Área
            6: $('#programaDepartamento').val(), // Departamento
            7: $('#programaUsuario').val()   // Responsable
        };
        applyTableFilters(programasTable, filters);
    });

    $('#limpiarFiltrosProgramas').click(function() {
        clearFilters(['#programaLinea', '#programaArea', '#programaDepartamento', '#programaUsuario'], programasTable);
    });

    // Configurar filtros para Premios
    $('#filtrarPremios').click(function() {
        var yearFilter = $('#premioAnio').val() ? '^'+$('#premioAnio').val() : '';
        var filters = {
            1: $('#premioTipo').val(),      // Tipo
            2: yearFilter,                  // Fecha (año)
            3: $('#premioArea').val(),       // Área
            4: $('#premioDepartamento').val(), // Departamento
            5: $('#premioUsuario').val()     // Premiados
        };
        applyTableFilters(premiosTable, filters);
    });

    $('#limpiarFiltrosPremios').click(function() {
        clearFilters(['#premioTipo', '#premioArea', '#premioDepartamento', '#premioUsuario', '#premioAnio'], premiosTable);
    });

    // Configurar filtros para Artículos
    $('#filtrarArticulos').click(function() {
        var yearFilter = $('#articuloAnio').val() ? '^'+$('#articuloAnio').val() : '';
        var filters = {
            3: yearFilter,                  // Fecha (año)
            5: $('#articuloArea').val(),     // Área
            6: $('#articuloDepartamento').val(), // Departamento
            7: $('#articuloAutor').val()     // Autores
        };
        applyTableFilters(articulosTable, filters);
    });

    $('#limpiarFiltrosArticulos').click(function() {
        clearFilters(['#articuloArea', '#articuloDepartamento', '#articuloAutor', '#articuloAnio'], articulosTable);
    });

    // Configurar botones de exportación
    $('.export-excel').click(function() {
        var tableId = $(this).data('table');
        $('#' + tableId).DataTable().button('.buttons-excel').trigger();
    });

    $('.export-pdf').click(function() {
        var tableId = $(this).data('table');
        $('#' + tableId).DataTable().button('.buttons-pdf').trigger();
    });

    // Mostrar notificación al cambiar de pestaña
    $('#reportTabs a').on('shown.bs.tab', function() {
        Toastify({
            text: "Mostrando " + $(this).text(),
            duration: 2000,
            close: true,
            gravity: "top",
            position: "right",
            backgroundColor: "#93ba22",
        }).showToast();
    });
});