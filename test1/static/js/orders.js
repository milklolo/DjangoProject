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
    'serverSide': true,
    'searching': true,
    'scrollCollapse': false,
    'language': {url: jsonUrl},
    'ajax': {
        url: baseUrl,
        type: 'GET',
        // DataTables 在 serverSide: true 時，預設傳送的參數已經包含 draw, start, length
        // 但如果你的後端是用 results 裝資料，這裡要改
        dataSrc: function (json) {
            return json.data; // 對應後端 result["data"]
        }
    },
    'columns': [
        { "data": "id" },
        { "data": "order_date" },
        {
            "data": "items",
            "orderable": false, // 這些計算欄位無法直接在後端排序，設為 false
            "render": function (data) {
                if (!data || data.length === 0) return "無商品";
                let mainProduct = data[0].product_name;
                return data.length > 1 ? `${mainProduct} <span class="badge bg-secondary">等 ${data.length} 項</span>` : mainProduct;
            }
        },
        { "data": "sales_name" }, // 索引 3
        {
            "data": "items",
            "orderable": false,
            "render": function (data) {
                return data.reduce((sum, item) => sum + item.quantity, 0);
            }
        },
        {
            "data": "items",
            "orderable": false,
            "render": function (data) {
                let total = data.reduce((sum, item) => sum + (parseFloat(item.product_price) * item.quantity), 0);
                return total.toLocaleString();
            }
        },
        {
            "data": null,
            "orderable": false,
            "render": function (data, type, row) {
                return `
                <div class="op">
                    <button type="button" class="edit-item-btn btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#NewAndEditModal">修改</button>
                    <button type="button" class="remove-item-btn btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#DeleteModal">刪除</button>
                </div>`;
            }
        }
    ],
    'order': [[1, 'desc']] // 預設依日期降冪排序
});

<!-- CRUD -->
let id = 0;
const modal_title = '訂單'
$('#new').html(`<i class="ri-add-line"></i> 新增${modal_title}`)
let rowTemplate = '';
$(document).ready(function () {
    rowTemplate = $('#product-row-template').html();
    // 點選修改或刪除
    $('#datatable tbody').on('click', '.edit-item-btn, .remove-item-btn', function () {
        let rowElement = $(this).closest('tr');
        let data = table.row(rowElement).data();
        rowTemplate = $('#product-row-template').html();

        if (!data) return; // 防錯處理
        id = data['id'];

        if ($(this).hasClass('edit-item-btn')) {
            // 修改
            $('#id').val(data['id']);
            $('#order_date').val(data['order_date']);
            $('#sales_name').val(data['sales']); // 填入銷售人員 ID

            // 重要：清空容器並根據 items 數量重新產生 row
            $('#product-items-container').empty();
            if (data.items && data.items.length > 0) {
                data.items.forEach(item => {
                    let $newRow = $(rowTemplate);
                    $newRow.find('.product-select').val(item.product);
                    $newRow.find('.product-price').val(item.product_price);
                    $newRow.find('input[name="quantity[]"]').val(item.quantity);
                    $('#product-items-container').append($newRow);
                });
            }

            $('#type').val('EDIT');
            $('#modal_title').html(`<i class="fa fa-edit modal-icon modify-modal-text"> 修改${modal_title}</i>`);
        } else {
            // 刪除部分保持不變...
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
        $('#id').val('');
        let today = new Date().toISOString().split('T')[0];
        $('#order_date').val(today);
        $('#sales_name').val('');

        // 初始化：只留一個空白的商品列
        $('#product-items-container').empty().append(rowTemplate);

        $('#type').val('NEW');
        $('#modal_title').html(`<i class="fa fa-plus modal-icon text-primary"> 新增${modal_title}</i>`);
    });

    // 增加商品列按鈕 (使用你原本喜歡的 append 方式，但改用 template 較乾淨)
    $('#add-product-item').on('click', function () {
        $('#product-items-container').append(rowTemplate);
    });

    // 刪除單一商品列
    $(document).on('click', '.remove-product-item', function () {
        if ($('.product-item-row').length > 1) {
            $(this).closest('.product-item-row').remove();
        }
    });

    // 價格連動：因為是動態產生的，必須用 $(document).on('change', ...)
    $(document).on('change', '.product-select', function () {
        const selectedOption = $(this).find('option:selected');
        const price = selectedOption.data('price');
        // 找到當前這一個 row 裡面的價格欄位
        $(this).closest('.product-item-row').find('.product-price').val(price || '');
    });
    // 新增商品列
    $('#add-product').on('click', function () {
        let row = `
    <div class="product-row row mb-2">
        <div class="col-md-5">
            <select class="form-control form-select product-select" name="product[]">
                <option value="" selected disabled>請選擇商品</option>
                ${$('#product_name').html()}
            </select>
        </div>
        <div class="col-md-3">
            <input type="text" id="product_price" class="form-control" readonly
                                       placeholder="自動帶入單價">
        </div>
        <div class="col-md-3">
           <input type="number" class="form-control" id="quantity" name="quantity"
                                       min="1"
                                       oninput="this.value = this.value.replace(/[^0-9]/g, '');"
                                       placeholder="請輸入數量"
                                       required>
        </div>
        <div class="col-md-1">
            <button type="button" class="btn btn-danger remove-product">X</button>
        </div>
    </div>
    `;

        $('#product-container').append(row);

    });
});