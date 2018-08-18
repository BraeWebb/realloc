function getUrlParams() {
  var paramMap = {};
  if (location.search.length == 0) {
    return paramMap;
  }
  var parts = location.search.substring(1).split("&");

  for (var i = 0; i < parts.length; i ++) {
    var component = parts[i].split("=");
    paramMap [decodeURIComponent(component[0])] = decodeURIComponent(component[1]);
  }
  return paramMap;
}

document.onready = function() {
	console.log("ready");
	console.log(document.getElementById("footer"))
	document.getElementById("footer").backgroundColor = "red";
	var params = getUrlParams();
	document.getElementById("errmsg").value = "The e-mail address " + params.user + " has no associated tutor account";
	console.log("done")
}
