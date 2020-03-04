//生成图片
$(function(){
    var q_id=$("#main").attr("q_id")
    $.ajax({
        type : "get",
        dataType : "json",
        url : "/getGoodsResult?q_id="+q_id,
        success: function(data){

            $("#sentiment").append("<img src='"+data.data[0][0]+"'>")
            $("#daily_comment").append("<img src='"+data.data[0][1]+"'>")
            $("#wordcloud").append("<img src='"+data.data[0][2]+"'>")
        },
        error:function(){
            alert("网络未连接")
        }
    });
});