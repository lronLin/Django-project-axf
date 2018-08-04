
function addgoods(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/addtocart/',
        type: 'POST',
        data:{'goods_id': id},
        dataType: 'json',
        headers:{'X-CSRFToken': csrf},
        success:function (data) {
            // alert(data.c_num)
            if(data.code == '200'){
                $('#goods_' + id).text(data.c_num)

                get_count_price()
            }
        },
        error:function (data) {
            alert('请求失败')
        }
    });
}


function subgoods(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/subtocart/',
        type: 'POST',
        data:{'goods_id': id},
        dataType: 'json',
        //403错误需要加headers(权限问题)
        //500是个人代码问题
        headers:{'X-CSRFToken': csrf},
        success:function (data) {
            // alert(data.c_num)
            if(data.code == '200'){
                $('#goods_' + id).text(data.c_num)
                if(data.c_num == '0'){
                    $('#cart_goods_id' + id).remove()
                }
                get_count_price()
            }
        },
        error:function (data) {
            alert('删除商品失败')
        }
    });
}


$.get('/axf/goodsnum', function (data) {
    if(data.code == '200'){
        for(var i=0; i<data.carts.length; i++){
            $('#goods_' + data.carts[i].goods_id).text(data.carts[i].c_num)
        }
    }

});


function changeCartStatus(id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/changeCartStatus/',
        data: {'cart_id': id},
        dataType: 'json',
        type: 'POST',
        headers:{'X-CSRFToken': csrf},
        success: function (data) {
            if(data.code == '200'){
                //如果修改后的is_select是True则为√else为×
                if(data.is_select){
                    s = '√'
                }else{
                    s = '×'
                }
                $('#cart_goods_is_select_' + id).text(s)
                get_count_price()
            }
        },
        error: function (data) {
            alert('请求失败')
        }
    });

}


function get_count_price() {
    $.get('/axf/goodsCount/', function (data) {
        if(data.code == '200'){
            $('#all_price').text(data.count)
        }
    })
}

get_count_price();