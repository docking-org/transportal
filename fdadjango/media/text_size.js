
function setTextSize(chgsize) {
	if (!document.documentElement || !document.body) return;
	var newSize = 100;
	var startSize = parseInt(getTextSize());
	if (!startSize || startSize < 60) startSize = 100;

	switch (chgsize) {
		case "incr":
			newSize = startSize + 5;
			break;
		case "decr":
			newSize = startSize - 5;
			break;
		case "reset":
			newSize = 100;
			break;
		default:
		 //	newSize = parseInt(getTextCookie("my-textsize"));
			if (!newSize) newSize = startSize;
			break;
	}
	
	if (newSize < 60) newSize = 60;
	if (newSize > 160) newSize = 160;
	
	newSize += "%";
	document.documentElement.style.fontSize = newSize;
	document.body.style.fontSize = newSize;
//	setTextCookie("my-textsize",newSize,365);
}
 
function getTextSize() {
	if (!document.body) return 0;
	var size = 0;
	var body = document.body;
	if (body.style && body.style.fontSize) {
		size = body.style.fontSize;
	} else if (typeof(getComputedStyle) != "undefined") {
		size = getComputedStyle(body,'').getPropertyValue("font-size");
	} else if (body.currentStyle) {
		size = body.currentStyle.fontSize;
	}
	return size;
}
/*
function setTextCookie(name,value,days) {
	var cookie = name + "=" + value + ";";
	if (days) {
		var myDate=new Date();
		myDate.setTime(myDate.getTime()+(days*24*60*60*1000));
		cookie += " expires=" + myDate.toGMTString() + ";";
	}
	cookie += " path=/";
	document.cookie = cookie;
}

function getTextCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(";");
	for(var cnt = 0; cnt < ca.length; cnt++) {
		var cooky = ca[cnt];
		while (cooky.charAt(0) == " ") cooky = cooky.substring(1, cooky.length);
		if (cooky.indexOf(nameEQ) == 0) return cooky.substring(nameEQ.length,cooky.length);
	}
	return;
}
*/
