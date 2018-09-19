$(document).ready(function () {
    /* 焦点离开文本框 */
    console.log('判断url和method不能为空');
    $("#url").blur(function () {
        if ($('#url').val().length == 0) {
            $("#error-url").css("display", 'block');
        } else {
            $("#error-url").css("display", 'none');
        }
    });
    $("#method").blur(function () {
        if ($('#method').val().length == 0) {
            $("#error-method").css("display", 'block');
        } else {
            $("#error-method").css("display", 'none');
        }
    });
});
function del(obj) {
    if (document.getElementById('tbodyid').children.length > 1) {
        var trid = obj.parentNode.parentNode.id;
        var objtr = document.getElementById(trid);
        document.getElementById('tbodyid').removeChild(objtr);
        var tbody = document.getElementById('tbodyid');
        var countchildren = tbody.childElementCount;
        for (var i = 0; i < countchildren; i++) {
            tbody.children[i].children[0].innerHTML = i + 1;
        }
    }
    else {
        alert("请不要全部删除");
    }
}
function add() {
    var trid = new Date().getTime();
    var packageid = trid + 'packageid';
    var priceid = trid + 'priceid';
    var objtr = document.createElement('tr');
    objtr.id = trid;
    objtr.innerHTML = "<td></td> " +
        "      <td><input id='" + trid + "packageid'></td> " +
        "      <td><input id='" + trid + "priceid'></td> " +
        "      <td><button type='button' onclick='del(this)'>删除</button></td>";
    document.getElementById("tbodyid").appendChild(objtr);
    var tbodyobj = document.getElementById('tbodyid');
    var countchildren = tbodyobj.childElementCount;
    for (var i = 0; i < countchildren; i++) {
        tbodyobj.children[i].children[0].innerHTML = i + 1;
    }
}