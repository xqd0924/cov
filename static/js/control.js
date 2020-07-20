function gettime() {
	$.ajax({
		type: "get",
		url: "/time",
		timeout: 10000,
		success: function(data) {
			$("#time").html(data)
		},
		error: function(xhr, type, errorThrown) {

		}
	});
}

function get_c1_data() {
	$.ajax({
		type: "get",
		url: "/c1",
		timeout: 10000,
		success: function(data) {
			$(".num h1").eq(0).html(data.confirm);
			$(".num h1").eq(1).html(data.suspect);
			$(".num h1").eq(2).html(data.dead);
			$(".num h1").eq(3).html(data.heal);
		}
	});
}

function get_c2_data(){
	$.ajax({
		type:"get",
		url:"/c2",
		success: function(data) {
			ec_center_option.series[0].data = data.data;
			ec_center.setOption(ec_center_option)
		},
	});
}

function get_le1_data(){
	$.ajax({
		type:"get",
		url:"/le1",
		success: function(data) {
			ec_left1_Option.xAxis[0].data = data.day;
			ec_left1_Option.series[0].data = data.confirm;
			ec_left1_Option.series[1].data = data.suspect;
			ec_left1_Option.series[2].data = data.heal;
			ec_left1_Option.series[3].data = data.dead;
			ec_left1.setOption(ec_left1_Option)
		},
	});
}

function get_le2_data(){
	$.ajax({
		type:"get",
		url:"/le2",
		success: function(data) {
			ec_left2_Option.xAxis[0].data = data.day;
			ec_left2_Option.series[0].data = data.confirm_add;
			ec_left2_Option.series[1].data = data.suspect_add;
			ec_left2.setOption(ec_left2_Option)
		},
	});
}

function get_r1_data(){
	$.ajax({
		type:"get",
		url:"/r1",
		success: function(data) {
			ec_right1_option.xAxis.data = data.city;
			ec_right1_option.series[0].data = data.confirm;
			ec_right1.setOption(ec_right1_option)
		},
	});
}

function get_r2_data(){
	$.ajax({
		type:"get",
		url:"/r2",
		success: function(data) {
			ec_right2_option.series[0].data = data.kws;
			ec_right2.setOption(ec_right2_option)
		},
	});
}

setInterval(gettime, 1000);
get_c1_data();
get_c2_data();
get_le1_data();
get_le2_data();
get_r1_data();
get_r2_data();