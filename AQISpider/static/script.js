function parseSeiyuu(txt) {
	var output, obj;
	output = '<table>\n';
	obj = jQuery.parseJSON(txt);
	$.each(obj, function(index,value) {
		output += '<tr><td>'+value.chara+'</td><td>'+value.name+'</td><td>'+value.alias+'</td></tr>\n'
	})
	output += '</table>\n';
	return output;
}


function parseLinks(txt) {
	var output, obj;
	output = '<ul>\n';
	obj = jQuery.parseJSON(txt);
	$.each(obj, function(index,value) {
		output += '<li><a href="'+value.link+'">'+value.label+'</a></li>\n'
	})
	output += '</ul>\n';
	return output;
}

function loadInfo(Id) {
	var infoxmlreqest;
	//Create XML Request
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		infoxmlreqest=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		infoxmlreqest=new ActiveXObject("Microsoft.XMLHTTP");
	}
	//function to parse response
	infoxmlreqest.onreadystatechange=function() {
		if (infoxmlreqest.readyState==4 && infoxmlreqest.status==200){
			document.getElementById("detail").innerHTML=infoxmlreqest.responseText;
			json = document.getElementById("seiyuu").innerHTML;
			document.getElementById("seiyuu").innerHTML = parseSeiyuu(json);
			json = document.getElementById("memo").innerHTML;
			document.getElementById("memo").innerHTML = parseLinks(json);
		}
	}
	//Send Request
	infoxmlreqest.open("GET", "/info?Id="+Id, true);
	infoxmlreqest.send();
}

$(function(){
    var _wrap=$('ul.list.a');//定义滚动区域
    var _interval=2000;//定义滚动间隙时间
    var _moving;//需要清除的动画
    _wrap.hover(function(){
        clearInterval(_moving);//当鼠标在滚动区域中时,停止滚动
    },function(){
        _moving=setInterval(function(){
            var _field=_wrap.find('li:first');//此变量不可放置于函数起始处,li:first取值是变化的
            var _h=_field.height();//取得每次滚动高度(多行滚动情况下,此变量不可置于开始处,否则会有间隔时长延时)
            _field.animate({marginTop:-_h+'px'},600,function(){//通过取负margin值,隐藏第一行
                _field.css('marginTop',0).appendTo(_wrap);//隐藏后,将该行的margin值置零,并插入到最后,实现无缝滚动
            })
        },_interval)//滚动间隔时间取决于_interval
    }).trigger('mouseleave');//函数载入时,模拟执行mouseleave,即自动滚动
});

