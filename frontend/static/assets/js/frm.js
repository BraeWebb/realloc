function click() {
	var str = "<div class='class-box'><div class=\"field quater first\"> \
					<input name=\"name\" id=\"name\" type=\"text\" placeholder=\"Class\"> \
				</div> \
				<div class=\"field quater first\"> \
				<select> \
					<option selected disabled>Weekday</option> \
					<option value=\"mon\">Mon</option> \
					<option value=\"tue\">Tue</option> \
					<option value=\"wed\">Wed</option> \
					<option value=\"thu\">Thu</option> \
					<option value=\"fri\">Fri</option> \
				</select> \
				</div> \
				<div class=\"field quater first\"> \
					<select> \
						      <option selected disabled>Start</option> \
							  <option value=\"8\">8:00</option> \
							  <option value=\"9\">9:00</option> \
							  <option value=\"10\">10:00</option> \
							  <option value=\"11\">11:00</option> \
							  <option value=\"12\">12:00</option> \
							  <option value=\"13\">13:00</option> \
							  <option value=\"14\">14:00</option> \
							  <option value=\"15\">15:00</option> \
							  <option value=\"16\">16:00</option> \
							  <option value=\"17\">17:00</option> \
							  <option value=\"18\">18:00</option> \
							  <option value=\"19\">19:00</option> \
							  <option value=\"20\">20:00</option> \
							</select> \
						</div> \
						<div class=\"field quater\"> \
							<select> \
						      <option selected disabled>End</option> \
							  <option value=\"8\">8:00</option> \
							  <option value=\"9\">9:00</option> \
							  <option value=\"10\">10:00</option> \
							  <option value=\"11\">11:00</option> \
							  <option value=\"12\">12:00</option> \
							  <option value=\"13\">13:00</option> \
							  <option value=\"14\">14:00</option> \
							  <option value=\"15\">15:00</option> \
							  <option value=\"16\">16:00</option> \
							  <option value=\"17\">17:00</option> \
							  <option value=\"18\">18:00</option> \
							  <option value=\"19\">19:00</option> \
							  <option value=\"20\">20:00</option> \
							</select> \
						</div></div>";
	var div = document.getElementById("allocform");
	console.log(div);
	div.insertAdjacentHTML('beforeend', str);

	/*$("#allocform .class-box").each(function() {
        console.log($(this).find("#day option:selected").text());
    })*/

	return false;
}

function runall() {
	days = {}

	console.log("test");
	var ancestor = document.getElementById("allocform");
	var descs = ancestor.getElementsByTagName('input');
	var i, j, e;
	var inputs = [];
	for(i = 0; i < descs.length; i++) {
		e = descs[i];
		inputs.push(e.value);
	}

	var descs = ancestor.getElementsByTagName('select');
	var selections = [];
	for(i = 0; i < descs.length; i++) {
		e = descs[i];
		selections.push(e.options[e.selectedIndex].text);
	}

	results = {};
	for(i = 0; i < inputs.length; i++) {
		j = i * 3;
		l = [selections[j], selections[j + 1], selections[j + 2]];
		results[inputs[i]] = l;
	}

	console.log("#message").value
	console.log(results);

	$.ajax({
        type: "POST",
        url: "/api/execute",
        data: {users: $("#message").value, classes: results},
        success: function(retrieved) {
            console.log(retrieved);
        }
    });

	return false;
}

document.onready = function() {
	document.getElementById("addrow").onclick = click;
	$("#runall").click(runall);
}
