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
            url: 'dataTables.german.json',
        }
    }
});