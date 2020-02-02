// 分页数据列表
function g_directory(page){ 
    var size=2;  
    $.ajax(
        {
            type : "get",
            dataType : "json",
            url : "/g_directory?page="+page+"&size="+size,
            success: function(data){
                if(!(data.status == "200")){
                    alert("ErrorCode : "+data.status)
                    return;
                }     
                var con = "";
                var is_success = "";
                //生成列表(首先清除列表与页码原有数据)  
                $("#directory").empty()
                $("#pageNum").empty()
                $.each(data.data, function(index, item){
                    if(item[1]==1){
                        is_success="成功"
                    }
                    else{
                        is_success="失败"
                    };
                    con += "<li>"+item[0]+"["+is_success+"]"+"["+item[2]+"]"+"</li><br>";
                     });
                     $("#directory").append(con); 
                //生成页码
                var pageNum = "";
                for(var i=1;i<=data.totalPage;i++){
                    if(i == page){
                        pageNum +="<li class='current'><span>"+i+"</span></li>";
                    }
                    else{
                        pageNum +="<li class=''><a onclick='g_directory("+i+")'>"+i+"</a></li>";
                    };   
                };
                $("#pageNum").append(pageNum)
            },
            error:function(){
                alert("error")
            }
        }
    )
};
//页面加载就调用一次
g_directory(1);
