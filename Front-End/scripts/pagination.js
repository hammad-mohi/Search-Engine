"use strict";

var numberOfItems = $("#loop .blurred-box").length;
var limPerPage = 5;
var numPagesShown = 1;


$("#loop .blurred-box:gt("+ (limPerPage - 1) +")").hide();
var totalPages = Math.round(numberOfItems / limPerPage);

$('.pagination').append("<li class = 'page-item active'><a class='page-link' href='javascript:void(0)'>" + 0 +"/" + totalPages +"</a></li>");

for(var i = 1; i <= (totalPages); i++){
  $('.pagination').append("<li class = 'page-item'><a class='page-link' href='javascript:void(0)'>" + i + "/" + totalPages + "</a></li>");
  $(".pagination > li:eq(" + (i +1) + ")").hide();
}
$('.pagination').append("<li id='next-page'><a class='page-link' href='javascript:void(0)' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>");

$('.pagination li.page-item').on("click", function(){
  if ($(this).hasClass("active")){
    return false;
  }
  else{
    var originalPage = $(".pagination li.active").index();
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
  if(currentPage === totalPages + 1){
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
    $(".pagination > li:eq(" + (currentPage -1) + ")").hide();
    $(".pagination > li:eq(" + currentPage + ")").show();
    $(".pagination > li:eq(" + currentPage +")").addClass("active");
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
    $(".pagination > li:eq(" + (currentPage + 1) + ")").hide();
    $(".pagination > li:eq(" +  currentPage + ")").show();
  }
});
