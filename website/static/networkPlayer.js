function showPlayer(firstTry) {
  return new Promise((resolve, reject) => {
    var chooser = document.getElementById("summonerid");
    var key = chooser.options[chooser.selectedIndex].value;
    $.ajax({
      dataType: "json",
      url: "network/" + key + "?content=details",
      success: function (data) {
        console.log(data);
        for (key in data) {
          let value = data[key];
          if (!isNaN(value)) {
            let aFloat = value.toString().split(".");
            if (aFloat.length > 1)
              value = aFloat[0] + "." + aFloat[1].substr(0, 4);
          }
          console.log(key)
          let row = document.getElementById("detail" + key);
          row.innerHTML = row.innerHTML + "<td>" + value + "</td>";
        }
        resolve();
      },
      error: function (data) {
        console.log(data);
        if (firstTry) {
          return showPlayer(content);
        }
        reject()
      },
      timeout: 1000,
    });
  });
}
