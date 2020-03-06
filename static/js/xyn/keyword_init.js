// 分页数据列表
function k_directory(page){
    var size=10;
    $.ajax(
        {
            type : "get",
            dataType : "json",
            url : "/k_directory?page="+page+"&size="+size,
            success: function(data){

                if(!(data.status == "200")){
                    alert("ErrorCode : "+data.status)
                    return;
                };
                if (data.data=="None"){
                    return;
                };
                var con = "";
                var is_success = "";
                //生成列表(首先清除列表与页码原有数据)
                $("#directory").empty()
                $("#pageNum").empty()
                con +="<li><p style='font-size: 20px'>（点击记录可查看分析结果，关键词可跳转至爬取的页面）</p></li>"
                $.each(data.data, function(index, item){
                    console.log(toString.call(item[3]));

                    con += "<li><a style='font-size:14px;' href='/k_history/"+item[0]+"'>" +
                        "<strong>"+"商品分析记录id:"+item[0]+"&nbsp;["+item[3]+"]"+"</strong>" +
                        "</a>" +
                        "<a href='https://search.jd.com/Search?keyword="+item[1]+"&enc=utf-8&psort=3' style='float: right'>" +
                        ">关键词："+item[1]+"</a></li><br>";
                     });
                     $("#directory").append(con);
                //调用页码方法
                g_pageNum(data,page);
            },
            error:function(){
                alert("error")
            }
        }
    )
};
//页码
function k_pageNum(data,page){
    //生成页码
    var totalPage = data.totalPage;
    var pageNum = "";
    //上一页
    if(page!=1){
        pageNum +="<li class=''><a onclick='k_directory("+(page-1)+")'><<</a></li>";
    }
    //中间页
    //只显示7页，本页显示在中间
    if(totalPage>7){
        if(page>3&&page<totalPage-2){
            for(var i=page-3;i<=page+3;i++){
                if(i == page){
                    pageNum +="<li class='current'><span>"+i+"</span></li>";
                }
                else{
                    pageNum +="<li class=''><a onclick='k_directory("+i+")'>"+i+"</a></li>";
                };
            };
        }
        else{
            //不符合则是最开始7页或最后7页
            if(page<7){
                for(var i=1;i<=7;i++){
                    if(i == page){
                        pageNum +="<li class='current'><span>"+i+"</span></li>";
                    }
                    else{
                        pageNum +="<li class=''><a onclick='k_directory("+i+")'>"+i+"</a></li>";
                    };
                };
            }
            else{
                for(var i=totalPage-7;i<=totalPage;i++){
                    if(i == page){
                        pageNum +="<li class='current'><span>"+i+"</span></li>";
                    }
                    else{
                        pageNum +="<li class=''><a onclick='k_directory("+i+")'>"+i+"</a></li>";
                    };
                };
            }
        }
    }
    else{
        for(var i=1;i<=totalPage;i++){
            if(i == page){
                pageNum +="<li class='current'><span>"+i+"</span></li>";
            }
            else{
                pageNum +="<li class=''><a onclick='k_directory("+i+")'>"+i+"</a></li>";
            };
        };
    }
    //下一页
    if (page == 0){
        return;
    }
    if(page!=totalPage){
        pageNum +="<li class=''><a onclick='k_directory("+(page+1)+")'>>></a></li>";
    }
    //生成总页数
    pageNum +="<li class='' ><strong style='color:red; text-align:center;line-height:32.8px'>&nbsp;共"+totalPage+"页</strong></li>";
    $("#pageNum").append(pageNum)
};
//页面加载就调用一次
k_directory(1);



//按钮点击新建分析
function getnew(){
    $("#second-level").html("新建关键词分析");
    $("#title").html("新建分析") ;
    $("#title").attr("href","#") ;
    $("#getNewGoods").css("display","inline");
    $("#directory").css("display","none");
    $("#getnew").remove();
    $("#pageNum").remove();
};

//检查表单
function checkUser() {
    if ($("#keyword_query_text").val()==""){
        $("#hint").html("提示：不可为空！")
        return false
    }

    $("#getNewGoods").css("display","none")
    $("#main").append("<p style='font-size: 18px'><strong>正在分析中。。。预计等待10~20秒，不要离开~</strong></p>")
    return true
};