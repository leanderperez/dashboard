new DataTable('#datatable', {
    paging: false,
        scrollCollapse: true,
        scrollY: '60vh',
    layout: {
        topStart : 'search',
        bottomStart: 'pageLength',
        bottomEnd: 'paging',
        topEnd: {
            buttons: ['excel', 'pdf', 'print']
        },
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json",
        }
    }
});