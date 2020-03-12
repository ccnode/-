
//检查公告表
function checkForm(){
    var title = $("#title").val()
    var describe = $("#describe").val()
    var myEdit =  $("#myEdit").val()
    if(title==""){
        $("#nint").html("标题不能为空！")
        return false
    }
    if(describe==""){
        $("#nint").html("描述不能为空！")
        return false
    }
    if(myEdit==""){
        $("#nint").html("内容不能为空！")
        return false
    }
    return true
};

