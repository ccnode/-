function g_directory(){
    
    var page = 1;
    var size = 10;
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
                // $(".directory").empty()
                $.each(data.data, function(index, item){
                    if(item[1]==1){
                        is_success="成功"
                    }
                    else{
                        is_success="失败"
                    }  
                    con += "<li>"+item[0]+"["+is_success+"]"+"["+item[2]+"]"+"</li><br>";
                     });
                     $("#directory").append(con) 

            },
            error:function(){
                alert("error")
            }
        }
    )
};
g_directory();
