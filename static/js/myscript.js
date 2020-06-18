$(document).on('mouseover', '.mainContainer .column', function(){
  $(this).addClass('active').siblings().removeClass('active')
})
