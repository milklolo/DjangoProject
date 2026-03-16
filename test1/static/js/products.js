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
let baseUrl = '/products/';

let table = $('#datatable').DataTable({
    'processing': true,
    'serverSide': true,
    'searching': true,
    'scrollCollapse': false,
    'language': {url: jsonUrl},
    'ajax': {
        url: baseUrl,
        type: 'GET',
        dataSrc: 'data',
    },
    'columns': [
        {"data": "id"},
        {"data": "name"},
        {"data": "price"},
        {
            "data": "image1",
            "render": function (data) {
                if (data) {
                    return `<img src="${data}" width="50" class="img-thumbnail">`;
                }
                return '無圖片';
            }
        },
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
const modal_title = '商品'
$('#new').html(`<i class="ri-add-line"></i> 新增${modal_title}`)

$(document).ready(function () {
    $('#datatable tbody').on('click', '.edit-item-btn, .remove-item-btn', function () {
        let rowElement = $(this).closest('tr');
        let data = table.row(rowElement).data();

        if (!data) return; // 防錯處理
        id = data['id'];

        if ($(this).hasClass('edit-item-btn')) {
            // 修改
            $('#id').val(data['id']);
            $('#name').val(data['name']);
            $('#price').val(data['price']);
            $('#type').val('EDIT');
            $('#clear_image').val('false'); // 每次打開 Modal 都重置為不刪除
            if (data['image1']) {
                $('#current-image-preview').attr('src', data['image1']); // 設定圖片來源
                $('#image-preview-container').show(); // 顯示預覽區
            } else {
                $('#image-preview-container').hide(); // 若沒圖片則隱藏
            }
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
        let formData = new FormData(this);
        $.ajax({
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            url: url,
            method: method,
            // data: $(this).serialize(),
            data: formData,
            processData: false,  // 告訴 jQuery 不要處理傳送的資料
            contentType: false,  // 告訴 jQuery 不要設定 Content-Type 標頭（讓瀏覽器自動處理）
            success: function () {
                table.ajax.reload(null, false);
                $("#NewAndEditModal").modal('hide');
                Toast.fire({icon: 'success', title: '存檔成功'});
                $('#image1').val('');
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
        $('#id, #name, #price, #image1').val('');
        $('#type').val('NEW');
        $('#modal_title').html(`<i class="fa fa-plus modal-icon text-primary"> 新增${modal_title}</i>`);
    });

    // 當使用者「重新選檔案」時，要把刪除標記重設為 false
    $('#image1').on('change', function() {
        if (this.files.length > 0) {
            $('#clear_image').val('false');
        }
    });

    //  取消圖片
    $('#clear-image-btn').on('click', function () {
        $('#current-image-preview').attr('src', ''); // 清空預覽圖
        $('#image-preview-container').hide();        // 隱藏容器
        $('#image1').val('');                        // 清空已選檔案
        $('#clear_image').val('true');               // 標記為「要刪除圖片」
    });
});

