/**
 * Created by wushengyu on 15/8/8.
 */
$(document).ready(function(){
  $('#complete_mes_submit').click(function(){
    var qq = $('#qq').val();
    var yy = $('#yy').val();
    var phone = $('#phone').val();
    if (qq && yy && phone && phone.length == 11){
      $.ajax({
            url: "/user/complete_mes",
            type: "post",
            data: {
              "qq": qq,
              "yy": yy,
              "phone": phone,
              "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "json",
            success: function(data, status){
              if(data === "success"){
                window.location = "/user/complete_mes"
              } else{
                Notify(data);
              }
            }
          }
      )
    }
    else{
      Notify("请填写正确的信息");
    }
  });
});

function openUpdateHeader(){
  $('#myModal').modal('show');
  var $body = $('body');
  var $inputImage = $('#inputImage');
  var URL = window.URL || window.webkitURL;
  var blobURL;

  if (URL) {
    $inputImage.change(function () {
      var files = this.files;
      var file;

      if (files && files.length) {
        file = files[0];

        if (/^image\/\w+$/.test(file.type)) {
          blobURL = URL.createObjectURL(file);
          var cropperOptions = {
            cropUrl:'/user/complete_mes',
            uploadData:{
              'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            loadPicture: blobURL
          };

          var cropperHeader = new Croppic('stu-header', cropperOptions);
          $inputImage.val('');
        } else {
          $body.tooltip('Please choose an image file.', 'warning');
        }
      }
    });
  } else {
    $inputImage.prop('disabled', true).parent().addClass('disabled');
  }
}
