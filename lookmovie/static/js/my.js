function choicesOnchange() {
	var area = $("input[name='area']:checked").attr("value");
	var rankmethod = $("input[name='rankmethod']:checked").attr("value");
	var abovemean = 0;
	if ($("input[name='abovemean']").prop("checked")) {
		abovemean = 1;
	}
	console.log(area);
	console.log(rankmethod);
	console.log(abovemean);
	$.post("/search/cinema/by_district/", { area: area, rankmethod: rankmethod, abovemean: abovemean }, changeCinemas);
}
function changeCinemas(data) {
	$("#cinemas").html("");
	$.each(data.data, function(i, item){
		// console.log(item.cinema_name);
		var content = "<div class=\"cinemaEntry col-md-3\"><div class=\"panel panel-default\"><div class=\"panel-heading\"><h3 class=\"panel-title\"><a href=\"/cinema/\">" + item.cinema_name + "</a></h3></div><div class=\"panel-body\"><p>评分：" + item.estimate + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p>行政区：" + item.district + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p>营业时间：" + item.businessHoursBegin + "~" + item.businessHoursEnd + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p>行政区：" + item.district + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p>街道：" + item.road + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p style=\"margin-bottom: 0px\">公交站：" + item.busStation + "</p></div></div>";
		$("#cinemas").append(content);
	});
}

function buyticket() {
	var allseat = $("input[name='seat'][disabled!='disabled']:checked");
	var data = new Array();
	for (var i = 0; i < allseat.length; i++) {
		data.push(allseat[i].value);
	}
	console.log(data);
	if (data.length == 0) {
		$(".modal-title").html("警告");
		$(".modal-body").html("请选择座位号！");
		$(".modal-body").html("<div class=\"alert alert-danger\" role=\"alert\"><Strong>请选择座位！</strong></div>");
		$("#buy").html("确定");
		$("#buy").attr("onclick", "modalclose()");
		$('#mymodal').modal("show");
		return;
	}
	
	$(".modal-title").html("购票信息");
	$(".modal-body").html("<h5>已选票：</h5><ul>")
	//<li>3排4号</li><li>3排5号</li>
	for (var i = 0; i < data.length; i++) {
		var row = data[i] % 100;
		var col = (data[i] - row) / 100;
		//console.log(row);
		//console.log(col);
		$(".modal-body").append("<li>" + col + "排" + row + "号</li>");
	}
	$(".modal-body").append("</ul>");
	$("#buy").html("购票");	
	$("#buy").attr("onclick", "buy()");
	$('#mymodal').modal("show");
}
function buy() {
	var allseat = $("input[name='seat'][disabled!='disabled']:checked");
	var data = new Array();
	for (var i = 0; i < allseat.length; i++) {
		data.push(allseat[i].value);
	}
	// send buy request
	var status = 0;
	if (status == 0) { // 成功
		$(".modal-body").html("<div class=\"alert alert-success\" role=\"alert\"><Strong>购票成功！！</strong></div>");
		$("#buy").html("确定");
		$("#close").hide();
		$("#buy").attr("onclick", "buysuccess()");
	} else {
		$(".modal-body").html("<div class=\"alert alert-danger\" role=\"alert\"><Strong>购票失败！！</strong></div>");
		$("#buy").html("确定");
		$("#close").hide();
		$("#buy").attr("onclick", "buyfailed()");
	}
}
function modalclose(){
	$('#mymodal').modal("hide");
}
function buysuccess(){
	//window.location = "http://localhost:8000/";
	modalclose();
}
function buyfailed(){
	//window.location = "http://localhost:8000/hall/";
	modalclose();
}

function indexCinema(){
	console.log('fuckkkkk');
	var area = 0;
	var rankmethod = 0;
	var abovemean = 0;
	$.post("/search/cinema/by_district/", { area: area, rankmethod: rankmethod, abovemean: abovemean }, changeCinemas);
}