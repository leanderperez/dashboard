new DataTable('#datatable', {
    layout: {
        topStart : 'search',
        bottomStart: 'pageLength',
        bottomEnd: 'paging',
        topEnd: {
            buttons: ['excel', 'pdf', 'print']
        },
        language: {
            url: 'dataTables.german.json',
        },
    }
});