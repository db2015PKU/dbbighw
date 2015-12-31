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
	$.each(data.data, function (i, item) {
		console.log(item);
		var content = "<div class=\"cinemaEntry col-md-3\"><div class=\"panel panel-default\"><div class=\"panel-heading\"><h3 class=\"panel-title\"><a href=\"" + item.url + "\">" + item.cinema_name + "</a></h3></div><div class=\"panel-body\"><p>评分：" + item.estimate + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p>营业时间：" + item.businessHoursBegin + "~" + item.businessHoursEnd + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p>行政区：" + item.district + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p>街道：" + item.road + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px\" /><p style=\"margin-bottom: 0px\">公交站：" + item.busStation + "</p></div></div>";
		$("#cinemas").append(content);
	});
}

function buyticket() {
	var allseat = $(".seatCharts-seat.selected");
	var data = new Array();
	for (var i = 0; i < allseat.length; i++) {
		data.push(allseat[i].id);
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
		var tmp = data[i].split("_");
		//console.log(row);
		//console.log(col);
		$(".modal-body").append("<li>" + tmp[0] + "排" + tmp[1] + "号</li>");
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
function modalclose() {
	$('#mymodal').modal("hide");
}
function buysuccess() {
	//window.location = "http://localhost:8000/";
	modalclose();
}
function buyfailed() {
	//window.location = "http://localhost:8000/hall/";
	modalclose();
}

function indexCinema() {
	var area = 0;
	var rankmethod = 0;
	var abovemean = 0;
	$.post("/search/cinema/by_district/", { area: area, rankmethod: rankmethod, abovemean: abovemean }, changeCinemas);
}

function getCinemaXML(url) {
	$.get(url, function (xml) {
		var cinema_name = $(xml).find("CinemaName").text();
		var district = $(xml).find("District").text();
		var road = $(xml).find("Road").text();
		var busStation = $(xml).find("BusStation").text();
		var phone = $(xml).find("Phone").text();
		var businessHours = $(xml).find("BusinessHours").text();
		var estimate = $(xml).find("Estimate").text();
		$("#estimate").html("评分： " + estimate);
		$("#phone").html("联系方式： " + phone);
		$("#time").html("营业时间： " + businessHours);
		$("#location").html("地址： " + district + "，" + road + "，" + busStation);
		$("#films").html("");
		$(xml).find("Movie").each(function (i) {
			var content = "<div class=\"filmEntry col-md-8 col-md-offset-2\"><div class=\"panel panel-default \"><div class=\"panel-heading \"><h3 class=\"panel-title \"><a href=\"" + $(this).children("RoomUrl").text() + "\">" + $(this).children("Name").text() + "</a></h3></div><div class=\"panel-body \"><p>时间： " + $(this).children("Date").text() + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px \" /><p>价格： " + $(this).children("Price").text() + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px \" /><p>放映厅： " + $(this).children("Room").text() + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px \" /><p>时长： " + $(this).children("Runtime").text() + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px \" /><p>类别： " + $(this).children("Type").text() + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px \" /><p>语言： " + $(this).children("Language").text() + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px \" /><p>导演： " + $(this).children("Director").text() + "</p><hr style=\"margin-top: 10px; margin-bottom: 10px \" /><p style=\"margin-bottom: 0px \">主演： " + $(this).children("Actors").text() + "</p></div></div></div>";
			$("#films").append(content);
		});
	});
}