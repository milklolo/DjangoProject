function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // 判斷這個 cookie 是否以我們想要的名稱開頭
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

<!-- datatable init -->
let jsonUrl = $('#datatable').data('json-url');
let baseUrl = '/orders/';

let table = $('#datatable').DataTable({
    'processing': true,
    'serverSide': false,
    'searching': false,
    'scrollCollapse': false,
    'language': {url: jsonUrl},
    'ajax': {
        url: baseUrl,
        type: 'GET',
        dataSrc: '',
    },
    'columns': [
        {"data": "id"},
        {"data": "order_date"},
        {"data": "product_name"}, //serializer
        {"data": "product_price"},
        // {"data": "sales_id"},
        {"data": "sales_name"},
        {"data": "quantity"},
        {
        "data": null,
        "render": function (data, type, row) {
            return `
                <div class="op">
                    <button type="button" class="edit-item-btn btn btn-sm btn-primary" 
                            data-bs-toggle="modal" data-bs-target="#NewAndEditModal">
                        修改
                    </button>
                    <button type="button" class="remove-item-btn btn btn-sm btn-danger" 
                            data-bs-toggle="modal" data-bs-target="#DeleteModal">
                        刪除
                    </button>
                </div>`;
        }
        }
    ],
    'order': [[1, 'asc']]
});

<!-- CRUD -->
let id = 0;
const modal_title = '訂單'
$('#new').html(`<i class="ri-add-line"></i> 新增${modal_title}`)

$(document).ready(function () {
    // 點選修改或刪除
    $('#datatable tbody').on('click', '.edit-item-btn, .remove-item-btn', function () {
        let rowElement = $(this).closest('tr');
        let data = table.row(rowElement).data();

        if (!data) return; // 防錯處理
        id = data['id'];

        if ($(this).hasClass('edit-item-btn')) {
            // 修改
            $('#id').val(data['id']);
            $('#order_date').val(data['order_date']);
            $('#product_name').val(data['product_id']);
            $('#product_price').val(data['product_price']);
            $('#sales_name').val(data['sales_id']);
            // $('#sales_name').val(data['sales_name']);
            $('#quantity').val(data['quantity']);
            $('#type').val('EDIT');
            $('#modal_title').html(`<i class="fa fa-edit modal-icon modify-modal-text"> 修改${modal_title}</i>`);
        } else {
            // 刪除
            $('#delete_modal_title').html(`<i class="fa fa-trash-alt modal-icon text-danger"> 刪除${modal_title}</i>`);
            $('#delid').text(data['id']);
        }
    });

    // 新增或修改存檔
    $('form').on('submit', function (e) {
        e.preventDefault();
        let url = baseUrl;
        let method = $('#type').val() === 'NEW' ? 'POST' : 'PUT';
        if (method === 'PUT') url += id + '/';

        $.ajax({
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            url: url,
            method: method,
            data: $(this).serialize(),
            success: function () {
                table.ajax.reload(null, false);
                $("#NewAndEditModal").modal('hide');
                Toast.fire({icon: 'success', title: '存檔成功'});
            },
            error: function (jqXHR) {
                let errorMessage = jqXHR.responseJSON;
                Toast.fire({icon: 'error', title: errorMessage});
                console.log(jqXHR);
            }
        });
    });

    // 刪除
    $('#DeleteModal').on('click', '#delete', function () {
        $.ajax({
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            url: baseUrl + id + '/',
            method: 'DELETE',
            success: function () {
                table.ajax.reload(null, false);
                $("#DeleteModal").modal('hide');
                Toast.fire({icon: 'success', title: '刪除成功'});
            },
            error: function (jqXHR) {
                let errorText = jqXHR.status + " " + jqXHR.statusText;
            Toast.fire({icon: 'error', title: '刪除失敗: ' + errorText});
            console.error("後端報錯詳情：", jqXHR.responseText);
            }
        });
    });

    // 新增
    $('#new').on('click', function () {
        $('#id, #product_price, #quantity').val('');
        let today = new Date().toISOString().split('T')[0];
        $('#order_date').val(today);
        $('#product_name').val('');
        $('#sales_name').val('');
        $('#type').val('NEW');
        $('#modal_title').html(`<i class="fa fa-plus modal-icon text-primary"> 新增${modal_title}</i>`);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const productSelect = document.getElementById('product_name');
    const priceInput = document.getElementById('product_price');

    productSelect.addEventListener('change', function () {
        const selectedOption = productSelect.options[productSelect.selectedIndex];

        // 取得 data-price 的值
        const price = selectedOption.getAttribute('data-price');

        // 自動設定價格欄位
        if (price) {
            priceInput.value = price;
        } else {
            priceInput.value = '';
        }
    });
});