/**
 * Created by wushengyu on 15/8/23.
 */
var number_pic = 1;
var uploadPicObj = $('#upload_pic');
var imageList = [];
function type_check(term_id){
  for(var i = 1; i <= 5; i++){
    var checkItem = "type" + i;
    var checkbox_input = $('#' + checkItem);
    var checkbox_label = $('#checkbox-' + checkItem + '-label');
    var checkbox_div = $('#checkbox-' + checkItem + '-div');
    if(checkItem === term_id){
      checkbox_input.attr('checked', 'true');
      checkbox_label.show();
      checkbox_div.show();
    } else{
      checkbox_input.attr('checked', 'true');
      checkbox_label.hide();
      checkbox_div.hide();
    }
  }
}


uploadPicObj.ajaxfileupload({
  'action': '/user/upload_complain_pic',
  'params': {
    'number': number_pic,
    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
  },
  'onComplete': function(response) {
    if(response == "failed"){
      Notify("上传失败");
      return false
    }
    uploadPicObj.files = '';
    number_pic++;
    $('.upload-pic-list').append("<img src='" + response + "' class='upload-pic-view' />");
    imageList.push(response)
  },
  'onStart': function() {
    var files = this[0].files;
    if(files.length){
      var file = files[0];
      if (file.size > (0.5 * 1024 * 1024)){
        Notify("请上传小于500K的文件");
        return false;
      }
      if (number_pic > 4){
        Notify("最多上传4张图片");
        return false;
      }
    }
  }
});


function submitComplain(){
  var name = $('#name').val();
  var qq = $('#qq').val();
  var phone = $('#phone').val();
  var mentorName = $('#mentor_name').val();
  var complainContent = $('#complain_content').val();
  var checkId = $('input[type=checkbox]:checked').attr('id');

  var postData = {
    name: name,
    phone: phone,
    qq: qq,
    mentor_name: mentorName,
    complain_content: complainContent,
    check_id: checkId,
    image_list: JSON.stringify(imageList),
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
  };
  console.log(postData);
  $.ajax({
    url: '/user/complain',
    type: 'post',
    data: postData,
    dataType: 'json',
    success: function(data){
      if(data === 'success'){
        Notify("提交成功");
        window.location = '/user/my_orders'
      } else{
        Notify("信息填写有误");
      }
    }
  })
}
