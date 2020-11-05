var tabID = sessionStorage.tabID
  ? sessionStorage.tabID
  : (sessionStorage.tabID = Math.random());
var tabid = tabID.toString();
document.getElementById("myField").value = tabid;
$(document).ready(function () {
  $(window).on("beforeunload", function () {
    $.ajax({
      type: "GET",
      url: "/data_delete/" + tabid,
      dataType: "json",
      success: function (data) {},
    });
  });
});
