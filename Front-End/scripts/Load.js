function Load(){
  for (var i = 0; i < 50; i++){
    document.write("<div class = 'blurred-box' style='max-width: 50rem'>");
    document.write(" 	<h4 class = 'result-title'> Search Result: " + i + "</h4>");
    document.write("	<a class = 'result-link' href='https://www.google.com' target='_blank'>Link</a>");
    document.write("	<h1 class = 'result-desc'> Description/Sample text from search result</h1>");
    document.write("</div>");
  }
}
