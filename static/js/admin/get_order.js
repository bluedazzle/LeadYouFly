/**
 * Created by RaPoSpectre on 15/9/8.
 */
$(document).ready(function(){
  function getOrder(){
    $.ajax({
          url: "/admin/get_status/",
          type: "get",
          data: '',
          dataType: "json",
          success: function(data, status){
            var order_num = document.getElementById('order_num');
              var report_num = document.getElementById('report_num');
              var cash_num = document.getElementById('cash_num');
            if(data.order_status === true){
              order_num.innerHTML = data.order_counts;
            }
            else{
              order_num.innerHTML = '';
            }
              if(data.report_status === true){
                  report_num.innerHTML = data.report_counts;
              }
              else{
                  report_num.innerHTML = '';
              }
              if(data.cash_status === true){
                  cash_num.innerHTML = data.cash_counts;
              }else{
                  cash_num.innerHTML = '';
              }
          }
        }
    )
  }
  getOrder();

  setInterval(getOrder, 10000);
});
