/*main*/
var suggest_url = '/suggest/';
var search_url = '/search/';

function main() {
    /*
    由于s标签乱入所以删除s标签再添加s标签包含的元素
    (不明白为什么，前端能力有限)
    <div>内嵌<span>
    */
    /*$.ajaxSetup({
        async: false
    });*/
    //选择搜索类别,并执行相应搜索
    $('.searchType').on('click', '.typeItem', function () {

        if ($('.top-search-input').val() == '') {

        } else {
            $('.searchType .typeItem').removeClass('current');
            $(this).addClass('current');
            search();
        }
    });
    //鼠标悬停在userList
    $('.dropdown').hover(function () {
        $('.user-menu').show()
    }, function () {
        $('.user-menu').hide()
    });
    //点击下拉历史搜索
    $(function () {
        $(".top-search-input").on("click", function (e) {
            dealHistoryList();
            e.stopPropagation();
        });
        $(".top-historyList").on("click", function (e) {
            e.stopPropagation();
        });
    });
    //回车搜索
    $('.top-search-input').bind('keypress', function (event) {
        if (event.keyCode == "13") {
            search();
        }
    });
    //输入提示搜索建议
    $(function () {
        $('.top-search-input').bind(' input propertychange ', function () {
            var searchText = $(this).val(); //获得input输入的值
            var suggestHtml = "";
            $('.top-historyList').hide();
            $.ajax({
                cache: false,
                type: 'get',
                dataType: 'json',
                url: suggest_url + "?s=" + searchText + "&s_type=" + $(".typeItem.current").attr('data-type'),
                async: false,
                success: function (data) {
                    for (var i = 0; i < data.length; i++) {
                        suggestHtml += '<li><a href="' + search_url + '?q=' + data[i].slice(0, 35) +
                            '&s_type=' + $(".typeItem.current").attr('data-type') + '">' + data[i] + '</a></li>'
                    }
                    $(".top-suggestList").html("")
                    $(".top-suggestList").append(suggestHtml);
                    if (data.length == 0) {
                        $('.top-suggestList').hide()
                    } else {
                        $('.top-suggestList').show()
                        $(document).one("click", function () {
                            $(".top-suggestList").hide();
                        });
                    }
                }
            });

        });
    });
}

//搜索函数
function search() {
    var input_val = $(".top-search-input").val();
    //判断输入框是否为空
    if (input_val == '') {
        $('.top-search-input').addClass('warning')
    } else {
        //跳转搜索链接
        window.location.href = search_url + '?q=' + input_val + "&s_type=" + $(".typeItem.current").attr('data-type')
    }
}
//历史记录
function dealHistoryList() {
    $(".top-historyList").show();
    //点击历史搜索记录跳转搜索
    $('.historyList-li').click(function () {
        history_text = $(this).text()
        window.location.href = search_url + '?q=' + history_text + "&s_type=" + $(".typeItem.current").attr('data-type')
    });
    $(document).one("click", function () {
        $(".top-historyList").hide();
    });
}

//实时热点
function dealTopn() {
    var topBox = $('.topi-box');
    topBox.find('.top-number').eq(0).removeClass('color-sublue-b');
    topBox.find('.top-number').eq(1).removeClass('color-sublue-b');
    topBox.find('.top-number').eq(2).removeClass('color-sublue-b');
    topBox.find('.top-number').eq(0).addClass('color-red-b');
    topBox.find('.top-number').eq(1).addClass('color-dimred-b');
    topBox.find('.top-number').eq(2).addClass('color-orange-b');

    $('.topi-keyword').click(function () {
        topiText = $(this).text();
        window.location.href = search_url + '?q=' + topiText + "&s_type=" + $(".typeItem.current").attr('data-type');
    });

}

