//var searchResult;
var postType = ["byName","byLocation","byType"];
var postReg;
var ipconfig = "140.121.199.231:27018"
//var ipconfig = "127.0.0.1:27018"


function rederictEvent(name){
	$.ajax({
		type: 'POST',
		url: "http://"+ipconfig+"/eventdetails",
		data: JSON.stringify({"eventName" : name.toString()}),
		contentType: 'application/json; charset=utf-8',
		success: function(data, textStatus) {
			if (data.redirect) {
				// data.redirect contains the string URL to redirect to
				window.location.href = data.redirect;
			}
		}
	});
}

function setResult(searchResult)
{
	$('#three').empty();
	var popContent = '<h1 align="center"><搜尋結果></h1>';
	for(var i=0;i*3<searchResult.length;i++){
		popContent += '<div class="inner flex flex-3">';
		for(var j=0;j<3 && i*3+j < searchResult.length;j++){
			popContent +=
				'<form action="/eventdetails" class="flex-item box"  method="GET"  name="form-search'+(i*3+j)+'" id="form-search'+(i*3+j)+'"><input type="hidden" name="eventName" value="'+searchResult[(i*3+j)].eventName+'">'+
				'<div  onClick="document.forms[\'form-search'+(i*3+j)+'\'].submit();"><a style="text-decoration:none;" target="_blank">';
			popContent +=
				'<div class="image fit"><img src="static/images/'+searchResult[(i*3+j)].eventName+'.jpg" alt="" /></div>';
			popContent +=
				'<div class="content">'+
				'<h3>'+searchResult[i*3+j].eventName+'</h3>'+
				'<p><b><span style="color:#AAAAAA;">活動時間 : <br>'+searchResult[i*3+j].eventM_B+'</b></p>'+
				'<p><b><span style="color:#AAAAAA;">活動地點 : <br>'+searchResult[i*3+j].eventLocation+'</span></b></p>'+
				'</div></a></div></form>';
		}
		popContent += '</div>';
	}

	$('#three').append(popContent);
}


function searchRequest(){
	var selected= [];
	//console.log($('#eventName').val());
	if(postReg == 0){
		$.ajax({
		type: 'POST',
		url: "http://"+ipconfig+"/searchcomplete",
		data: JSON.stringify({"type" : postType[postReg] , "data" : $('#eventName').val().toString()}),
		contentType: 'application/json; charset=utf-8',
		success: setResult
		});
	}
	if(postReg == 2){
		if($('#learn').is(":checked")){selected.push("learn");}
		if($('#art').is(":checked")){selected.push("art");}
		if($('#sport').is(":checked")){selected.push("sport");}
		if($('#ocean').is(":checked")){selected.push("ocean");}
		if($('#fishery').is(":checked")){selected.push("fishery");}
		if($('#welfare').is(":checked")){selected.push("welfare");}
		if($('#techlogy').is(":checked")){selected.push("techlogy");}
		if($('#health').is(":checked")){selected.push("health");}
		if($('#entertainment').is(":checked")){selected.push("entertainment");}

		$.ajax({
		type: 'POST',
		url: "http://"+ipconfig+"/searchcomplete",
		data: JSON.stringify({"type" : postType[postReg] , "data" : selected}),
		contentType: 'application/json; charset=utf-8',
		success: setResult
		});
	}
	
	
	//searchRequest = $.post("http://140.121.199.231:27018/searchcomplete",{"type" : postType[postReg] , "data" : $('#eventName').value},setResult(),"json");
}

function createSearchBarNode()
	{
		postReg = 0;
		$('#main').empty();
		var popContent =			
					'<div class="inner"><input type="text" name="searchEventName" id="eventName" placeholder="請輸入活動名稱" autofocus></div><br>'+
					'<div class="inner">'+
								'<ul class="actions" style="text-align:right;" >'+
									'<li><input type="submit" value="確認送出" onclick="searchRequest()"/></li>'+
									'<li><input type="reset" value="取消" class="alt" /></li>'+
								'</ul></div>';

		$('#main').append(popContent);
		//return newNode;
	}

	function createTypeBoxNode()
	{
		postReg = 2;
		$('#main').empty();
		var popContent =
				'<div class="inner"><div style="font-size: 16pt">'+
				'<p><label style="font-size: 20pt"> 請勾選籌畫狀況(可複選,至少一項)'+
				'<div style="display: inline-block;"><input type="checkbox" name="done" id="done" ><label for="done">已完成</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="planning" id="planning" checked><label for="planning">籌畫中</label></div><p>'+			
				'<p><label style="font-size: 20pt"> 請勾選活動分類(可複選,至少一項)'+
				'<div style="display: inline-block;"><input type="checkbox" name="learn" id="learn" ><label for="learn">學習</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="art" id="art" ><label for="art">藝文</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="sport" id="sport" ><label for="sport">運動</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="ocean" id="ocean" ><label for="ocean">海洋</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="fishery" id="fishery" ><label for="fishery">漁業</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="welfare" id="welfare" ><label for="welfare">公益</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="techlogy" id="techlogy" ><label for="techlogy">科技</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="health" id="health" ><label for="health">健康</label></div>'+
				'<div style="display: inline-block;"><input type="checkbox" name="entertainment" id="entertainment" ><label for="entertainment">娛樂</label></div>'
				'</p></div></div><br>';
			popContent += '<div class="inner">'+
			'<ul class="actions" style="text-align:left;" >'+
				'<li><input type="submit" value="確認送出" onclick="searchRequest()"/></li>'+
				'<li><input type="reset" value="取消" class="alt" /></li>'+
			'</ul></div>';

		$('#main').append(popContent);
	}




	