$(document).ready(function(){
  $('#teacher_host').addClass('list-group-item-active');
});

/* teacher_host checkbox*/

function position_check(term_id){
  var checkbox_input = $('#' + term_id);
  var checkbox_label = $('#' + term_id + '-label');
  var checkbox_div = $('#' + term_id + '-div');
  if(checkbox_input.attr('checked') == 'checked'){
    checkbox_input.removeAttr('checked');
    checkbox_label.hide();
    checkbox_div.hide();
  } else{
    checkbox_input.attr('checked', 'true');
    checkbox_label.show();
    checkbox_div.show();
  }
}