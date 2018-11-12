"use strict";

var numberOfItems = $("#loop .blurred-box").length;
var limPerPage = 5;
var numPagesShown = 9;

$("#loop .blurred-box:gt("+ (limPerPage - 1) +")").hide();
var totalPages = Math.round(numberOfItems / limPerPage);

$('.pagination').append("<li class = 'page-item active'><a class='page-link' href='javascript:void(0)'>" + 1 + "</a></li>");

for(var i = 2; i <= totalPages; i++){
  $('.pagination').append("<li class = 'page-item'><a class='page-link' href='javascript:void(0)'>" + i + "</a></li>");
  if (i > numPagesShown){
    $(".pagination > li:eq(" + i + ")").hide();
  }
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
    
    if (currentPage >= 3){
      var pageToHide;
      var pageToShow;
      var diff = currentPage - originalPage;
      if ((diff > 0 && originalPage >= 2) || (diff > 2)){
        pageToHide = currentPage - 3;
        pageToShow = currentPage + 2;
        if(pageToHide > 0){
          $(".pagination > li:eq(" + pageToHide +")").hide();
        }
        $(".pagination > li:eq(" + pageToShow +")").show();
        if (diff >= 2){
          pageToHide = currentPage - 4;
          pageToShow = currentPage + 1;
          if (pageToHide > 0){
            $(".pagination > li:eq(" + pageToHide +")").hide();
          }
          $(".pagination > li:eq(" + pageToShow +")").show();
        }
      }
      else if(diff < 0 && currentPage < totalPages -2 ){
        pageToShow = currentPage - 2;
        pageToHide = currentPage + 3;
        $(".pagination > li:eq(" + pageToHide +")").hide();
        $(".pagination > li:eq(" + pageToShow +")").show();
        if (diff <= -2 && currentPage != 3){
          pageToShow = currentPage - 1;
          pageToHide = currentPage + 4;
          $(".pagination > li:eq(" + pageToHide +")").hide();
          $(".pagination > li:eq(" + pageToShow +")").show();
        }
      }
    }
  }
});

$("#next-page").on("click", function(){
  var currentPage = $(".pagination li.active").index();
  if(currentPage === totalPages+1){
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
    $(".pagination > li:eq(" + currentPage +")").addClass("active");

    if(totalPages > 5){
      if(currentPage > 5 && currentPage <= totalPages){
        var hid = currentPage - 5;
        var show = currentPage + 4;
        $(".pagination > li:eq(" + hid + ")").hide();
        $(".pagination > li:eq(" + show + ")").show();
      }
    }
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

    if(totalPages > 5){
      if(currentPage >= 5 && currentPage < totalPages - 4){
        var hid = currentPage + 5;
        var show = currentPage - 4;
        $(".pagination > li:eq(" + hid + ")").hide();
        $(".pagination > li:eq(" + show + ")").show();
      }
    }
  }
});
