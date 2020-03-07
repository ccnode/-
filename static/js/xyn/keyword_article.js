//生成图片
$(function(){
    var q_id=$("#main").attr("q_id")
    $.ajax({
        type : "get",
        dataType : "json",
        url : "/getKeywordResult?q_id="+q_id,
        success: function(data){

            $("#price_distribution").append("<img src='"+data.data[0][0]+"'>")
            $("#shop_ranking").append("<img src='"+data.data[0][1]+"'>")

        },
        error:function(){
            alert("网络未连接")
        }
    });
});
