function getData() {
    $('#data').DataTable({
        responsive: true,
        autoWidth: true,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'action': 'search'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "parroquia.canton.province.country.name"},
            {"data": "parroquia.canton.province.name"},
            {"data": "parroquia.canton.name"},
            {"data": "parroquia.name"},
            {"data": "name"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/location/district/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/location/district/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    buttons += '<a href="/location/verBarrio/' + row.id + '/" class="btn btn-info btn-xs btn-flat"><i class="fa fa-search" aria-hidden="true"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    getData();
});