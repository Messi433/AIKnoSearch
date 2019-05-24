/*
* 分页实现的功能:
* 1.当前是第1页显示后面的4个页码和最后2个页码中间的用...隔开
* 2.当前是最后1页则反过来
* 3.(一个range显示6个页码)从前到后切换页码,前3页显示页码不变,切换到第4页增加第5页，直到增加到第6页，再往后显示当前页码范围的,从后往前切同理可得
* 4.
* */
jQuery.fn.pagination = function(maxentries, info) {
	info = jQuery.extend({
				items_per_page : 10, // 每页显示多少条记录
				current_page : 0,      //当前页码
				num_mid_show : 4, // 中间显示页码的个数
				num_end_show : 2, // 末尾显示页码的个数
				a_href : "#page",         //页码点击后的链接
				previous_text : "上一页",   //上一页的文字
				next_text : "下一页",	   //下一页的文字
				ellipse_text : "...",  //页码之间的省略号
				show_msg : true, // 是否显示记录信息
				previous_show_always : true, //是否总是显示最前页
				next_show_always : true,//是否总是显示最后页
				setPageNo:false,//是否显示跳转第几页
				callback : function() {
					return false;
				} // 回调函数
			}, info || {});

	return this.each(function() {
		// 总页数
		function numPages() {
			return Math.ceil(maxentries / info.items_per_page);
		}
		/**
		 * 计算页码
		 */
		function getInterval() {
			var ne_half = Math.ceil(info.num_mid_show / 2);
			var np = numPages();
			var upper_limit = np - info.num_mid_show;
			var start = current_page > ne_half ? Math.max(Math.min(current_page
									- ne_half, upper_limit), 0) : 0;
			var end = current_page > ne_half ? Math.min(current_page + ne_half,
					np) : Math.min(info.num_mid_show, np);
			return [start, end];
		}

		/**
		 * 点击事件
		 */
		function pageSelected(page_id, evt) {
			var page_id = parseInt(page_id);
			current_page = page_id;
			drawLinks();
			var continuePropagation = info.callback(page_id, panel);
			if (!continuePropagation) {
				if (evt.stopPropagation) {
					evt.stopPropagation();
				} else {
					evt.cancelBubble = true;
				}
			}
			return continuePropagation;
		}

		/**
		 * 链接
		 */
		function drawLinks() {
			panel.empty();
			var interval = getInterval();
			var np = numPages();
			var getClickHandler = function(page_id) {
				return function(evt) {
					return pageSelected(page_id, evt); //选择页码
				}
			}
			var appendItem = function(page_id, appendinfo) {
				page_id = page_id < 0 ? 0 : (page_id < np ? page_id : np-1);
				appendinfo = jQuery.extend({
							text : page_id+1,
							classes : ""
						}, appendinfo || {});
				if (page_id == current_page) {
					var lnk = $("<span class='current'>" + (appendinfo.text)
							+ "</span>");
				} else {
					var lnk = $("<a>" + (appendinfo.text) + "</a>").bind(
							"click", getClickHandler(page_id)).attr('href',
							info.a_href.replace(/__id__/, page_id));

				}
				if (appendinfo.classes) {
					lnk.addClass(appendinfo.classes);
				}
				panel.append(lnk);
			}
			// 上一页
			if (info.previous_text && (current_page > 0 || info.previous_show_always)) {
				appendItem(current_page - 1, {
							text : info.previous_text,
							classes : "previous"
						});
			}
			// 省略号
			if (interval[0] > 0 && info.num_end_show > 0) {
				var end = Math.min(info.num_end_show, interval[0]);
				for (var i = 0; i < end; i++) {
					appendItem(i);
				}
				if (info.num_end_show < interval[0] && info.ellipse_text) {
					jQuery("<span>" + info.ellipse_text + "</span>")
							.appendTo(panel);
				}
			}
			// 中间的页码
			for (var i = interval[0]; i < interval[1]; i++) {
				appendItem(i);
			}
			// 最后的页码
			if (interval[1] < np && info.num_end_show > 0) {
				if (np - info.num_end_show > interval[1]
						&& info.ellipse_text) {
					jQuery("<span>" + info.ellipse_text + "</span>")
							.appendTo(panel);
				}
				var begin = Math.max(np - info.num_end_show, interval[1]);
				for (var i = begin; i < np; i++) {
					appendItem(i);
				}

			}
			// 下一页
			if (info.next_text
					&& (current_page < np - 1 || info.next_show_always)) {
				appendItem(current_page + 1, {
							text : info.next_text,
							classes : "next"
						});
			}
			// 记录显示
			if (info.show_msg) {
				if(!maxentries){
					panel
						.append('<div class="page-result">暂未搜索出任何有效数据</div>');
				}else{
				panel
						.append('<div class="page-result">显示第&nbsp;'
								+ ((current_page * info.items_per_page) + 1)
								+ '&nbsp;条到&nbsp;'
								+ (((current_page + 1) * info.items_per_page) > maxentries
										? maxentries
										: ((current_page + 1) * info.items_per_page))
								+ '&nbsp;条记录，总共&nbsp;' + maxentries + '&nbsp;条</div>');
				}
			}
			//bug
			//设置跳到第几页
			if(info.setPageNo){
				  panel.append("<div class='goto'><span class='text'>跳转到</span><input type='text'/><span class='page'>页</span>" +
					  "<button type='button' class='ue-button long2'>确定</button></div>");
			}
		}

		// 当前页
		var current_page = info.current_page;
		maxentries = ( maxentries < 0) ? 0 : maxentries;
		info.items_per_page = (!info.items_per_page || info.items_per_page < 0)
				? 1
				: info.items_per_page;
		var panel = jQuery(this);
		this.selectPage = function(page_id) {
			pageSelected(page_id);
		}
		this.prevPage = function() {
			if (current_page > 0) {
				pageSelected(current_page - 1);
				return true;
			} else {
				return false;
			}
		}
		this.nextPage = function() {
			if (current_page < numPages() - 1) {
				pageSelected(current_page + 1);
				return true;
			} else {
				return false;
			}
		}
		
		if(maxentries==0){
			panel.append(
				'<span class="current previous">'+info.previous_text+'</span><span class="current next">'+
				info.next_text+'</span><div class="page-result">暂未搜索出任何有效数据</div>');
		}else{
			drawLinks();
		}
		$(this).find(".goto button").live("click",function(evt){
			var setPageNo = $(this).parent().find("input").val();
			if(setPageNo!=null && setPageNo!=""&&setPageNo>0&&setPageNo<=numPages()){
				pageSelected(setPageNo-1, evt);
			}
		});		
	});
}
