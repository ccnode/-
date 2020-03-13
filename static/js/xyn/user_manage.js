// 用户数据列表
function directory(page){
    var size=10;
    $.ajax(
        {
            type : "get",
            dataType : "json",
            url : "/user_directory?page="+page+"&size="+size,
            success: function(data){
                if(!(data.status == "200")){
                    alert("ErrorCode : "+data.status)
                    return;
                };
                if (data.data=="None"){
                    return;
                };
                var con = "";
                //生成列表(首先清除列表与页码原有数据)

                $("#directory").empty()
                $("#pageNum").empty()
                $.each(data.data, function(index, item){
                    var freeze="正常"
                    var freeze_but="<td><button type='submit' onclick='freeze(this)' class='templatemo-blue-button'>冻结</button>"
                    if (item[2]=="1"){
                        freeze="冻结"
                        freeze_but="<td><button type='submit' onclick='unfreeze(this)' class='templatemo-blue-button'>解冻</button>"
                    }
                    var is_admin="普通用户"
                    if (item[3]=="1"){
                        is_admin="管理员"
                    }

                    con += "<tr style='text-align: center;' uid='"+item[0]+"'>" +
                        "                    <td>"+item[0]+"</td>" +
                        "                    <td>"+item[1]+"</td>" +
                        "                    <td>"+freeze+"</td>" +
                        "                     <td>"+is_admin+"</td>" +
                        freeze_but +
                        "                      <button type='submit' onclick='del(this)' class='templatemo-blue-button' style='background: #D7425C'>删除</button>" +
                        "                    </td>" +
                        "                  </tr>"
                     });
                     $("#directory").append(con);
                //调用页码方法
                pageNum(data,page);
            },
            error:function(){
                alert("error")
            }
        }
    )
};
//页码
function pageNum(data,page){
    //生成页码
    var totalPage = data.totalPage;
    var pageNum = "";
    //上一页
    if(page!=1){
        pageNum +="<li class=''><a onclick='directory("+(page-1)+")'><<</a></li>";
    }
    //中间页
    //只显示7页，本页显示在中间
    if(totalPage>7){
        if(page>3&&page<totalPage-2){
            for(var i=page-3;i<=page+3;i++){
                if(i == page){
                    pageNum +="<li class='current' id='this_page'><span>"+i+"</span></li>";
                }
                else{
                    pageNum +="<li class=''><a onclick='directory("+i+")'>"+i+"</a></li>";
                };
            };
        }
        else{
            //不符合则是最开始7页或最后7页
            if(page<7){
                for(var i=1;i<=7;i++){
                    if(i == page){
                        pageNum +="<li class='current' id='this_page'><span>"+i+"</span></li>";
                    }
                    else{
                        pageNum +="<li class=''><a onclick='directory("+i+")'>"+i+"</a></li>";
                    };
                };
            }
            else{
                for(var i=totalPage-7;i<=totalPage;i++){
                    if(i == page){
                        pageNum +="<li class='current' id='this_page'><span>"+i+"</span></li>";
                    }
                    else{
                        pageNum +="<li class=''><a onclick='directory("+i+")'>"+i+"</a></li>";
                    };
                };
            }
        }
    }
    else{
        for(var i=1;i<=totalPage;i++){
            if(i == page){
                pageNum +="<li class='current' id='this_page'><span>"+i+"</span></li>";
            }
            else{
                pageNum +="<li class=''><a onclick='directory("+i+")'>"+i+"</a></li>";
            };
        };
    }
    //下一页
    if (page == 0){
        return;
    }
    if(page!=totalPage){
        pageNum +="<li class=''><a onclick='directory("+(page+1)+")'>>></a></li>";
    }
    //生成总页数
    pageNum +="<li class='' ><strong style='color:red; text-align:center;line-height:32.8px'>&nbsp;共"+totalPage+"页&nbsp;</strong></li>";
    $("#pageNum").append(pageNum)
};
//页面加载就调用一次
directory(1);

//冻结
function freeze(obj) {
    if(!confirm("确定冻结该用户?")){
 　　return
}
    var uid = $(obj).parent().parent().attr("uid");
    $.ajax(
        {
            type: "get",
            dataType: "json",
            url: "/user_freeze?uid="+uid,
            success: function (data) {
                var page=$("#this_page").find("span").text()
                directory(page)
            },
            error:function(){
                alert("error")
            }
        });
};

//解冻
function unfreeze(obj) {
    if(!confirm("确定解冻该用户?")){
 　　return
}
    var uid = $(obj).parent().parent().attr("uid");
    $.ajax(
        {
            type: "get",
            dataType: "json",
            url: "/user_unfreeze?uid="+uid,
            success: function (data) {
                var page=$("#this_page").find("span").text()
                directory(page)
            },
            error:function(){
                alert("error")
            }
        });
};

//删除用户
function del(obj) {
    if(!confirm("确定删除该用户?")){
 　　return
}
    var uid = $(obj).parent().parent().attr("uid");
    $.ajax(
        {
            type: "get",
            dataType: "json",
            url: "/user_del?uid="+uid,
            success: function (data) {
                var page=$("#this_page").find("span").text()
                directory(page)
            },
            error:function(){
                alert("error")
            }
        });
};