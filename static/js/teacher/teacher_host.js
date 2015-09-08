$(document).ready(function(){
  $('#teacher_host').addClass('list-group-item-active');
  $("#select-teach-heroes").select2({dropdownCssClass: 'dropdown-inverse'});
  $.ajax(
      {
        url: "/get_all_heroes",
        type: "get",
        data: '',
        dataType: "json",
        success: function(data, status){
          localStorage['all_heroes'] = JSON.stringify(data)
        }
      }
  )
});

/* teacher_host checkbox*/

function position_check(term_id){
  var status = $('#' + term_id).attr('checked');
  if(term_id === 'checkbox-all'){
    change_check('checkbox-mid', status);
    change_check('checkbox-top', status);
    change_check('checkbox-jungle', status);
    change_check('checkbox-ADC', status);
    change_check('checkbox-support', status);
    change_check('checkbox-all', status)
  } else if(term_id === 'checkbox-area-all' || term_id === 'checkbox-telecom' ||
      term_id === 'checkbox-netcom'){
    change_check('checkbox-telecom', 'checked');
    change_check('checkbox-area-all', 'checked');
    change_check('checkbox-netcom', 'checked');
    change_check(term_id)
  } else if(term_id === 'checkbox-video' || term_id === 'checkbox-picture'){
    change_check('checkbox-video', 'checked');
    change_check('checkbox-picture', 'checked');
    change_check(term_id)
  } else{
    change_check(term_id, 1)
  }
}

function change_check(term_id, option){
  var checkbox_input = $('#' + term_id);
  var checkbox_label = $('#' + term_id + '-label');
  var checkbox_div = $('#' + term_id + '-div');
  if(option != 1){
    if(option === 'checked'){
      checkbox_input.removeAttr('checked');
      checkbox_label.hide();
      checkbox_div.hide();
      return true;
    } else{
      checkbox_input.attr('checked', 'true');
      checkbox_label.show();
      checkbox_div.show();
      return true;
    }
  }

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

function removeHero(id, option){
  if(option === 1){
    $('#expert_hero'+id).remove();
  } else{
    $('#expert_hero'+id).remove();
    $('#teach_hero'+id).remove();
  }
}

function initAddHero(option){
  var expertHeroesBox = $('#expert-heroes');
  var expertHeroesId = expertHeroesBox.find('.hero-id');
  var teachHeroesBox = $('#teach-heroes');
  var teachHeroesId = teachHeroesBox.find('.hero-id');
  var teachHeroesName = teachHeroesBox.find('.hero-name');
  var selectObj;
  if(option === 1){
    selectObj = $('#select-expert-heroes');
    selectObj.children('option').each(function(){
      $(this).remove()
    });
    var expertIdList = [];
    var expertNameList = [];

    teachHeroesId.each(function(){
      expertIdList.push($(this).text());
    });
    teachHeroesName.each(function(){
      expertNameList.push($(this).text())
    });

    for(var i = 0; i < expertIdList.length; i++){
      selectObj.append("<option value='" + expertIdList[i] + "'>" + expertNameList[i] + "</option>")
    }

    expertHeroesId.each(function(){
      selectObj.children("option[value='" + $(this).text() + "']").attr('selected', 'true');
    });

    selectObj.select2({dropdownCssClass: 'dropdown-inverse'});
    $('#editExpertHero').modal('show');
  } else{
    selectObj = $('#select-teach-heroes');

    teachHeroesId.each(function(){
      selectObj.children("option[value='" + $(this).text() + "']").attr('selected', 'true');
    });

    selectObj.select2({dropdownCssClass: 'dropdown-inverse'});
    $('#editTeachHero').modal('show');
  }
}

function changeHeroesList(option){
  var selectObj;
  var heroList;
  var selectedHeroes;
  var allHeroes = JSON.parse(localStorage['all_heroes']);
  var HeroesView;
  if(option === 1){
    selectObj = $('#select-expert-heroes');
    HeroesView = $('#expert-heroes');
  } else{
    selectObj = $('#select-teach-heroes');
    HeroesView = $('#teach-heroes');
  }
  selectedHeroes = selectObj.children('option:selected');
  if (option === 1 && selectedHeroes.length > 3){
    Notify("只能选择3个擅长英雄");
    return false;
  }
  heroList = [];
  selectedHeroes.each(function(){
    var heroId = $(this).val();
    for(var i = 0; i < allHeroes.length; i++){
      if(parseInt(heroId) === allHeroes[i].id){
        heroList.push(allHeroes[i]);
        break
      }
    }
  });

  if(option === 1){
    HeroesView.children('.expert-hero').each(function(){
      $(this).remove();
    });
  } else{
    HeroesView.children('.teach-hero').each(function(){
      $(this).remove();
    });
  }

  for(var i = 0; i < heroList.length; i++){
    var newHeroHtml;
    if(option === 1){
      newHeroHtml = "<div class='col-lg-1 col-md-1 expert-hero' id='expert_hero" + heroList[i].id + "'>";
    } else{
      newHeroHtml = "<div class='col-lg-1 col-md-1 teach-hero' id='teach_hero" + heroList[i].id + "'>";
    }
    newHeroHtml += "<span class='hero-id'>" + heroList[i].id +"</span>";
    newHeroHtml += "<span class='hero-name'>" + heroList[i].hero_name + "</span>";
    newHeroHtml += "<div class='hero-img'>";
    newHeroHtml += "<img src='" + heroList[i].hero_pic + "'>";
    if (option === 1){
      newHeroHtml += "<span class=\"hero-remove\" onclick=\"removeHero(\'" + heroList[i].id + "\', 1)\">";
    } else{
      newHeroHtml += "<span class=\"hero-remove\" onclick=\"removeHero(\'" + heroList[i].id + "\', 2)\">";
    }
    newHeroHtml += "<i class='glyphicon glyphicon-remove'></i>";
    newHeroHtml += "</span></div></div>";
    HeroesView.prepend(newHeroHtml);

  }

  if(option === 2){
    var expertHeroes = $('#expert-heroes').find('.hero-id');
    expertHeroes.each(function(){
      var heroId = $(this).text();
      var is_have = false;
      for(var i = 0; i < heroList.length; i++){
        if(heroList[i].id === parseInt(heroId)){
          is_have = true;
        }
      }
      if(!is_have){
        $('#expert_hero' + heroId).remove()
      }
    });
  }

  if(option === 1){
    $('#editExpertHero').modal('hide');
  } else{
    $('#editTeachHero').modal('hide');
  }
}


// 表单提交

var xhr;
function fileSelected(fileId, nameId, sizeId) {
  var file = document.getElementById(fileId).files[0];
  if (file) {
    var fileSize = 0;
    if (file.size > 1024 * 1024)
      fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
    else
      fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';
    document.getElementById(nameId).innerHTML = file.name;
    document.getElementById(sizeId).innerHTML = fileSize;
  }
}

function checkForm(){
  var name = $("input[name='name']").val();
  var intro = $("input[name='intro']").val();

  var goodAt = "";
  var positionMid = $("input[name='position_mid']").attr('checked');
  var positionTop = $("input[name='position_top']").attr('checked');
  var positionADC = $("input[name='position_ADC']").attr('checked');
  var positionJungle = $("input[name='position_jungle']").attr('checked');
  var positionSupport = $("input[name='position_support']").attr('checked');
  if(positionMid) goodAt += '1';
  if(positionTop) goodAt += '2';
  if(positionADC) goodAt += '3';
  if(positionJungle) goodAt += '4';
  if(positionSupport) goodAt += '5';

  var expertHeroes = [];
  $('#expert-heroes').find('.hero-id').each(function(){
    expertHeroes.push($(this).text())
  });

  var teachHeroes = [];
  $('#teach-heroes').find('.hero-id').each(function(){
    teachHeroes.push($(this).text())
  });

  var gameLevel = $("input[name='level']").val();

  var areaTelecom = $("input[name='area_telecom']").attr('checked');
  var areaNetcom = $("input[name='area_netcom']").attr('checked');
  var teachArea;
  if(areaTelecom) teachArea = '1';
  if(areaNetcom) teachArea = '2';
  if(areaTelecom && areaNetcom) teachArea = '0';

  var viewVideo = $("input[name='view_video']").attr('checked');

  if(!name) return false;
  if(!intro) return false;
  if(goodAt === "") return false;
  if(expertHeroes.length === 0) return false;
  if(teachHeroes.length === 0)  return false;
  if(!gameLevel) return false;
  if(!teachArea) return false;
  var viewType;
  if(!viewVideo){
    viewType = '0'
  } else{
    viewType = '1'
  }


  var formData = {};
  formData.name = name;
  formData.intro = intro;
  formData.goodAt = goodAt;
  formData.expertHeroes = JSON.stringify(expertHeroes);
  formData.teachHeroes = JSON.stringify(teachHeroes);
  formData.gameLevel = gameLevel;
  formData.teachArea = teachArea;
  formData.viewType = viewType;

  return formData
}

function submitUpdateForm(){
  var fd = new FormData();
  var formData = checkForm();
  if(!formData) {
    Notify("请完善信息");
    return false;
  }
  if(document.getElementById('new_video').files.length > 0){
    fd.append("new_video", document.getElementById('new_video').files[0]);
  }
  if(document.getElementById('new_pic').files.length > 0){
    //var img = new Image();
    var img = $('#view_new_pic');
    var file = document.getElementById('new_pic').files[0];
    img.attr('src', window.URL.createObjectURL(file));

    img.load(function(){
      if(parseFloat(img.height()) / parseFloat(img.width()) > 1.0){
        Notify("请上传高比宽小于1的图片");
        return false;
      }
    });
    fd.append("new_picture", document.getElementById('new_pic').files[0]);
  }
  fd.append("name", formData.name);
  fd.append("intro", formData.intro);
  fd.append("good_at", formData.goodAt);
  fd.append("expert_heroes", formData.expertHeroes);
  fd.append("teach_heroes", formData.teachHeroes);
  fd.append("game_level", formData.gameLevel);
  fd.append("teach_area", formData.teachArea);
  fd.append("view_type", formData.viewType);
  fd.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val());
  xhr = new XMLHttpRequest();
  xhr.upload.addEventListener("progress", uploadProgress, false);
  xhr.addEventListener("load", uploadComplete, false);
  xhr.addEventListener("error", uploadFailed, false);
  xhr.addEventListener("abort", uploadCanceled, false);
  xhr.open("POST", "/teacher/host");
  xhr.send(fd);
  document.getElementById('fileStatus').innerHTML = '数据上传中...'
}

function uploadProgress(evt) {
  if (evt.lengthComputable) {
    var percentComplete = Math.round(evt.loaded * 100 / evt.total);
    document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
    if (percentComplete == 100) {
      $('#progressNumber').text('');
      document.getElementById('fileStatus').innerHTML = '数据处理中...';
    }
  }
  else {
    document.getElementById('progressNumber').innerHTML = 'unable to compute';
  }
}
function uploadComplete(evt) {
  /* 服务器端返回响应时候触发event事件*/
  var res = JSON.parse(xhr.responseText);
  if(res === 'success'){
    document.getElementById('fileStatus').innerHTML = '上传成功！';
    //location.reload();
  } else{
    document.getElementById('fileStatus').innerHTML = res;

  }
}
function uploadFailed(evt) {
  alert("There was an error attempting to upload the file.");
}
function uploadCanceled(evt) {
  alert("The upload has been canceled by the user or the browser dropped the connection.");
}

function viewVideo(url, poster){
  $('#view-video').modal('show');
  var modalContent = $('.modal-body');
  modalContent.find('video').attr('poster', poster);
  modalContent.find('video').find('source').attr('src', url);
  modalContent.find('video').load();
}