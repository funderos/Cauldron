function showPlayer(firstTry) {
  var chooser = document.getElementById('summonerid');
  var key = chooser.options[chooser.selectedIndex].value;
  var infoDiv = document.getElementById('network-output')
  $.ajax({
    dataType: "json",
    url: "network/" + key + "?content=details",
    success: function(data){
      console.log(data)
      let info = "<table>";
      for (key in data) {
        info = info + "<tr><td>" + key + "</td><td>" + data[key] + "</td></tr>";
      }
      info = info + "</table>";
      infoDiv.innerHTML = info;
    },
    error: function(data){
      console.log(data);
      if (firstTry) {
        showPlayer(content, false)
      }
    },
    timeout: 1000
  });
}