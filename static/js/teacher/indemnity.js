$(document).ready(function(){
  $('#manage_indemnity').addClass('list-group-item-active');
  $('.table-indemnity tbody tr:odd td').css({background: 'rgb(247, 247, 247)',color: 'rgb(170, 170, 170)'});
  $('.table-indemnity tbody tr:even td').css({background:'#ffffff',color:'rgb(170, 170, 170)'});
});

function submitOutCash(money){
  var inputNumber = $('input[name=money]').val();
  if(inputNumber && inputNumber <= money){
    $.ajax({
      url: "/teacher/indemnity",
      type: "post",
      data: {
        "money": inputNumber,
        "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
      },
      dataType: "json",
      success: function(data, status){
        if(data === "success"){
          window.location = "/teacher/indemnity"
        } else{
          Notify(data);
        }
      }
    })
  } else{
    Notify("信息有误，请重新填写");
  }
}