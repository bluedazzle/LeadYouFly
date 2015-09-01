/**
 * Created by wushengyu on 15/9/1.
 */
var selectScreen = $('.select-screen');
var selectArea = $('.select-screen-area');
var selectPosition = $('.select-screen-position');
var selectHero = $('.select-screen-hero');

function openSelectScreen(choice){
  selectScreen.fadeIn();
  if(choice === 1){
    selectArea.show();
  } else if(choice == 2){
    selectPosition.show();
  } else if(choice == 3){
    selectHero.show()
  }
}

function closeSelectScreen(){
  selectScreen.fadeOut();
  selectArea.hide();
  selectPosition.hide();
  selectHero.hide()
}

function toMentorDetail(id){
  window.location = "/mentor_detail?mentor_id=" + id;
}