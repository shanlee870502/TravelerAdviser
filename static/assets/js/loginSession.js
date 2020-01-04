var ipconfig='140.121.199.231:27018'
$.ajax({
    type: 'POST',
    url: "http://"+ipconfig+"/loginSession",
    contentType: 'application/json; charset=utf-8',
    success: setLoginButton
    });
function setLoginButton(sessionLogin){
    if(sessionLogin.user=='False'||sessionLogin.user==''){
        $('#logInOut').text('登入');
        $('#logInOut').attr('href','login');
    }
    else{
        $('#logInOut').text('登出');
        $('#logInOut').attr('href','logout_user');
    }
}