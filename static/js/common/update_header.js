/**
 * Created by wushengyu on 15/9/6.
 */
var file;
function openUpdateHeader(){
  $('#myModal').modal('show');
  var $image = $('#user-header > img');
  var $body = $('body');
  var $inputImage = $('#inputImage');
  var URL = window.URL || window.webkitURL;
  var blobURL;

  if (URL) {
    $inputImage.change(function () {
      $image.cropper({
        aspectRatio: 1,
        autoCropArea: 0.8,
        crop: function(e) {
          $("#dataX").text(Math.round(e.x));
          $("#dataY").text(Math.round(e.y));
          $("#dataHeight").text(Math.round(e.height));
          $("#dataWidth").text(Math.round(e.width));
          $("#dataRotate").text(e.rotate);
          $("#dataScaleX").text(e.scaleX);
          $("#dataScaleY").text(e.scaleY);
        }
      });
      var files = this.files;

      if (files && files.length) {
        file = files[0];

        if (/^image\/\w+$/.test(file.type)) {
          blobURL = URL.createObjectURL(file);
          $image.one('built.cropper', function () {
            URL.revokeObjectURL(blobURL); // Revoke when load complete
          }).cropper('reset').cropper('replace', blobURL);
        } else {
          $body.tooltip('Please choose an image file.', 'warning');
        }
      }
    });
  } else {
    $inputImage.prop('disabled', true).parent().addClass('disabled');
  }
}
var xhr;
function submitUpdateHeader(){
  var fd = new FormData();
  var dataX1 = $('#dataX').text();
  var dataY1 = $('#dataY').text();
  var height = parseInt($('#dataHeight').text());
  var width = parseInt($('#dataWidth').text());
  var x1 = parseInt(dataX1);
  var y1 = parseInt(dataY1);

  if(height === 0 && width === 0){
    Notify("请至少操作一下图片");
    return false
  }

  fd.append("new_header", file);
  fd.append("dataX1", dataX1);
  fd.append("dataY1", dataY1);
  fd.append("dataX2", (x1+width).toString());
  fd.append("dataY2", (y1+height).toString());
  fd.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val());
  xhr = new XMLHttpRequest();
  xhr.addEventListener("load", uploadComplete, false);
  xhr.open("POST", "/update_header");
  xhr.send(fd);
}

function uploadComplete(evt) {
  /* 服务器端返回响应时候触发event事件*/
  var res = JSON.parse(xhr.responseText);
  if(res != 'success'){
    Notify("更新失败");
  } else{
    location.reload();
  }
}
