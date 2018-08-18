function click() {
	var str = "<div class=\"field quater first\"> \
					<input name=\"name\" id=\"name\" type=\"text\" placeholder=\"Class\"> \
				</div> \
				<div class=\"field quater first\"> \
				<select> \
					<option value=\"mon\">Monday</option> \
					<option value=\"tue\">Tuesday</option> \
					<option value=\"wed\">Wednesday</option> \
					<option value=\"thu\">Thursday</option> \
					<option value=\"fri\">Friday</option> \
				</select> \
				</div> \
				<div class=\"field quater first\"> \
					<select> \
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
						</div>";
	var div = document.getElementById("allocform");
	console.log(div);
	div.insertAdjacentHTML('beforeend', str);
	return false;
}

document.onready = function() {
	document.getElementById("addrow").onclick = click;
}
