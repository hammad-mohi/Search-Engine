function Load(results){
	for (var i = 0; i < 5; i++){
    		document.write("<div class = 'blurred-box' style='max-width: 50rem'>");
    		document.write(" 	<h4 class = 'result-title'> " + results[i][1] + "</h4>");
    		document.write("	<a class = 'result-link' href='" + results[i][0] + "' target='_blank'>Link</a>");
    		document.write("	<h1 class = 'result-desc'> " + results[i][2] + "</h1>");
    		document.write("</div>");
  	}
}
