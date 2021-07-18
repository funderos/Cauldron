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
        let value = data[key];
        if (!isNaN(value)) {
          let aFloat = value.toString().split(".");
          if (aFloat.length > 1) value = aFloat[0] + "." + aFloat[1].substr(0, 4);
        }
        info = info + (i % 2 ? "<tr><td>" : "<td>") + key + "</td><td>" + value + (i % 2 ? "</td>" : "</td></tr>");
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