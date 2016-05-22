$().ready(function(){
	$("#signin").click(function(){
		$(".signup").css("display","none");
		$(".signin").css("display","block");
	});
	$("#signup").click(function(){
		$(".signin").css("display","none");
		$(".signup").css("display","block");
	});
	//注册验证
	$("#zhuce").click(function(){
		var email = $("#email").val();
		var password = $("#password").val();
		var username = $("#username").val();
		event.preventDefault();
		$(".tishi").text("");
		if (email===""){
			$("#email").next().text("请填写您的邮箱");
			
		}
		if (password==="" || password.length<6) {
			$("#password").next().text("请填写正确的密码");
		}
		if (username===""){
			$("#username").next().text("请填写您的名字");
		}
		$.post('/polls/checkregister',
		{
			email:email,
			password: password,
			username:username
		},
		function(data){
			var success = eval('(' + data + ')').success;
			if (success==="0"){
				$("#email").next().text("账号已存在");
			}else {
				$(".signin form").submit();
			}
		})
	})
	//登陆验证
	$("#denglu").click(function(){
		var email = $("#id_email").val();
		var password = $("#id_password").val();
		event.preventDefault();
		$(".tishi").text("");
		if (email==="" || password==="" || password.length<6) {
			if (email===""){
				$("#id_email").next().text("请填写您的邮箱");
			}
			if(password==="" || password.length<6){
				$("#id_password").next().text("请填写正确的密码");
			}
		}else {
			$.post('/polls/checklogin',
		{
			email: email,
			password: password
		},
		function(data){
			var success = eval('(' + data + ')').success;
			if (success==="0"){
				$("#id_password").next().text("账号密码错误");
			}else {
				$(".signup form").submit();
			}
		});
		}
	});

	$("#shouye").mouseover(function(){
		$("#shouye").css({"background-color":"#0078D8", "border":"none"});
	}).click(function(){
		$("#shouye").css({"background-color":"#055fb8", "border":"none"});
	});
	$("#huati").mouseover(function(){
		$("#huati").css({"background-color":"#0078D8", "border":"none"});
	});
	$("#faxian").mouseover(function(){
		$("#faxian").css({"background-color":"#0078D8", "border":"none"});
	});

	$(".dropdown").hover(function(){
		$("#name").css({"background-color":"#055fb8", "border":"none"});
		$(".dropdown-menu").show();
	}, function(){
		$("#name").css({"background-color":"#0078D8", "border":"none"});
		$(".dropdown-menu").hide();
	})
	$("#name-down a").hover(function(){
		$(this).css("background-color", "#0078D8");
	}, function(){
		$(this).css("background-color", "#055fb8");
	})

	$(".ask a").mouseover(function(){
		$(this).css("background-color", "#0e7bef");
	})

	//回答问题
	$(".question-answer button").click(function(){
		var answer = $(".question-answer textarea").val();
		var question_id = $(".question-name").attr("name");
		$.post("/polls/answer",
		{
			answer: answer,
			question_id: question_id
		},
		function(data){
			var result = eval('(' + data + ')');
			var has_commented = result.has_commented;
			var html = $(".answer-item:first").html();
			if (has_commented==='0'){
				var user_name = result.user_name;
				var answer = result.answer;
				var answer_time = result.answer_time;
				$(".answers-contents").append(html);
				$(".answer-text:last").text(answer);
			};
		});
	});
	//展开评论
	$(".toggle-comment").click(function(){
		$(this).parent().next().toggle();
	})
	$(".comment-button").focus(function(){
		$(this).parent().next().css("display", "block");
	})
	$(".quxiao").click(function(){
		$(this).parent().css("display", "none");
	})
	//回复评论
	$(".comment-hui").click(function(){
		$(this).parent().next().toggle();
	})
	$(".comment-quxiao").click(function(){
		$(this).parent().parent().css("display", "none");
	})

	//提交评论
	$(".comment-submit-button").click(function(){
		var content = $(this).parent().prev().children().val();
		var user_to = $(this).parent().parent().attr("user-to");
		var answer_id = $(this).parent().parent().attr("answer-id");
		var obj = $(this);
		$.post("/polls/comment",
		{
			content:content,
			answer_id:answer_id,
			user_to:user_to,
		},
		function(data){
			var result = eval('(' + data + ')');
			var content = result.content;
			var userto_name = result.userto_name;
			var userfrom_name = result.userfrom_name;
			var comment_time = result.comment_time;
			$(obj).parents(".comment-form-root").css("display", "none");
			if (userto_name===""){
				var item = $(obj).parents(".comment-form-root").prev();
				var html = $(item).html();
				$(item).after(html);
				$(item).next().html("<a href='javascript:void(0);'>" + userfrom_name + "</a>");
				$(item).siblings(".comment-content").text(content);
				$(item).siblings(".comment-item-foot").children("span").text(comment_time);
			}else{
				var item = $(obj).parents(".comment-item");
				var html = $(item).html();
				$(item).after(html);
				$(item).next().html("<a href='javascript:void(0);'>" + userfrom_name + "</a>"
					+ "<span>回复</span>" + "<a href='javascript:void(0);'>" + userto_name+ "</a>");
				$(item).siblings(".comment-content").text(content);
				$(item).siblings(".comment-item-foot").children("span").text(comment_time);
				$(item).siblings(".comment-form-root").css("display", "none");
			}
		})
	})
	//关注人
	$(".follower").click(function(){
		var people_id = $(this).attr("people-id");
		$.post("/polls/follow",
		{
			people_id:people_id,
			follow:"1"
		},
		function(data){
		})
	})
	//取消关注
	$(".followed").click(function(){
		var people_id = $(this).attr("people-id");
		$.post("/polls/follow",
		{
			people_id:people_id,
			follow:"0"
		},
		function(data){
		})
	})
});