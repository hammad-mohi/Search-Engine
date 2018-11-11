"use strict";

var numberOfItems = $("#loop .blurred-box").length;
var limPerPage = 5;

$("#loop .blurred-box:gt("+ (limPerPage - 1) +")").hide();
var totalPages = Math.round(numberOfItems / limPerPage);

$('.pagination').append("<li class = 'page-item active'><a class='page-link' href='javascript:void(0)'>" + 1 + "</a></li>");

for(var i = 2; i <= totalPages; i++){
  $('.pagination').append("<li class = 'page-item'><a class='page-link' href='javascript:void(0)'>" + i + "</a></li>");
}
$('.pagination').append("<li id='next-page'><a class='page-link' href='javascript:void(0)' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>");

$('.pagination li.page-item').on("click", function(){
  if ($(this).hasClass("active")){
    return false;
  }
  else{
    var currentPage = $(this).index();
    $('.pagination li').removeClass("active");
    $(this).addClass("active");
    $('#loop .blurred-box').hide();

    var grandTotal = limPerPage * currentPage;
    for (var i = grandTotal - limPerPage; i < grandTotal; i++){
      $("#loop .blurred-box:eq("+ i + ")").show();
    }
  }
});

$("#next-page").on("click", function(){
  var currentPage = $(".pagination li.active").index();
  if(currentPage === totalPages){
    return false;
  }
  else{
    currentPage++;
    $(".pagination li").removeClass("active");
    $("#loop .blurred-box").hide();

    var grandTotal = limPerPage * currentPage;
    for (var i = grandTotal - limPerPage; i < grandTotal; i++){
      $("#loop .blurred-box:eq("+ i + ")").show();
    }
    $(".pagination li.page-item:eq(" + currentPage +")").addClass("active");
  }
});


$("#prev-page").on("click", function(){
  var currentPage = $(".pagination li.active").index();
  if(currentPage === 1){
    return false;
  }
  else{
    currentPage--;
    $(".pagination li").removeClass("active");
    $("#loop .blurred-box").hide();

    var grandTotal = limPerPage * currentPage;
    for (var i = grandTotal - limPerPage; i < grandTotal; i++){
      $("#loop .blurred-box:eq("+ i + ")").show();
    }
    $(".pagination > li:eq(" + currentPage +")").addClass("active");
  }
});
