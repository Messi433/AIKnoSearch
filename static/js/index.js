/*index*/
function index() {
    /*$.ajaxSetup({
                async: false
            });*/
    // 切换搜索类型
    $('.searchType').on('click', '.typeItem', function () {
        $('.searchType .typeItem').removeClass('current');
        $(this).addClass('current');
    });
    //点击下拉历史搜索记录,当用户清空历史记录，下拉搜索热点
    $(function () {
        $(".search-input").on("click", function (e) {
            deal_historyList();
            deal_topList();
            e.stopPropagation();
        });
        $(".historyList,.topList").on("click", function (e) {
            e.stopPropagation();
        });
    });
    //回车搜索
    $('.search-input').bind('keypress', function (event) {
        if (event.keyCode == "13") {
            search();
        }
    });
    //输入提示搜索建议
    $(function () {
        $('.search-input').bind(' input propertychange ', function () {
            var searchText = $(this).val(); //获得input输入的值
            var suggestHtml = ""
            $('.historyList').hide();
            $('.topList').hide()
            $.ajax({
                cache: false,
                type: 'get',
                dataType: 'json',
                url: suggest_url + "?s=" + searchText + "&s_type=" + $(".typeItem.current").attr('data-type'),
                async: true,
                success: function (data) {
                    //data:响应成功后端发送的数据
                    for (var i = 0; i < data.length; i++) {
                        suggestHtml += '<li><a href="' + search_url + '?q=' + data[i].slice(0, 35) +
                            '&s_type=' + $(".typeItem.current").attr('data-type') + '">' + data[i] + '</a></li>'
                    }
                    $(".suggestList").html("")
                    $(".suggestList").append(suggestHtml);
                    if (data.length == 0) {
                        $('.suggestList').hide()
                    } else {
                        $('.suggestList').show()
                        $(document).one("click", function () {
                            $(".suggestList").hide();
                        });
                    }
                }
            });

        });
    });
}
//搜索函数
function search() {
    var input_val = $(".search-input").val();
    //判断输入框是否为空
    if (input_val == '') {
        $('.search-input').addClass('warning')
    } else {
        //跳转搜索链接
        var regstr = /^#$/; //检测#特殊符号
        if (regstr.test(input_val))
            alert("hello world")
        window.location.href = search_url + '?q=' + input_val + "&s_type=" + $(".typeItem.current").attr('data-type')
    }
}

//历史记录
function deal_historyList() {
    $(".historyList").show();
    //点击历史搜索记录跳转搜索
    $('.historyList-li').click(function () {
        history_text = $(this).text()
        window.location.href = search_url + '?q=' + history_text + "&s_type=" + $(".typeItem.current").attr('data-type')
    });
    $(document).one("click", function () {
        $(".historyList").hide();
    });
}

//搜索热点
function deal_topList() {
    $(".topList").show();
    //点击历史搜索记录跳转搜索
    $('.topList-li').click(function () {
        history_text = $(this).children("span").text()
        window.location.href = search_url + '?q=' + history_text + "&s_type=" + $(".typeItem.current").attr('data-type')
    });
    $(document).one("click", function () {
        $(".topList").hide();
    });
}