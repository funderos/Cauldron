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
      let i = 1;
      for (key in data) {
        info = info + (i % 2 ? "<tr><td>" : "<td>") + key + "</td><td>" + data[key] + (i % 2 ? "</td>" : "</td></tr>");
        i++;
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