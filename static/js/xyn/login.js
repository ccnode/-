//登录验证
function checkUser(){
    var username = $("#username").val()
    var passwd = $("#passwd").val()
    if (username==""){
        $("#nameHint").html("提示：用户名不能为空！")
        $("#pwdHint").html("")
        return false
    }
    if (passwd==""){
        $("#pwdHint").html("提示：密码不能为空！")
        $("#nameHint").html("")
        return false
    }
    return true
}