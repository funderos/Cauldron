function addPlayerToTable(playerId, firstTry = true) {
  let checkExisting = document.getElementsByClassName(playerId.toString());
  if (checkExisting.length) return Promise.resolve();
  return new Promise((resolve, reject) => {
    $.ajax({
      dataType: "json",
      url: "network/" + playerId + "?mode=details",
      success: function (data) {
        for (key in data) {
          let value = data[key];
          if (!isNaN(value)) {
            let aFloat = value.toString().split(".");
            if (aFloat.length > 1)
              value = aFloat[0] + "." + aFloat[1].substr(0, 4);
          }
          let row = document.getElementById("detail" + key);
          row.innerHTML = row.innerHTML + "<td class='" + playerId + "'" + ">" + value + "</td>";
        }
        let row = document.getElementById("detailshownetwork");
        row.innerHTML = row.innerHTML + "<td class='" + playerId + "'" + ">" + "<input type='button' class='btn btn-primary' value='Show!' onclick='drawNetwork(" + playerId + ")'></input>" + "</td>";
        row = document.getElementById("detailremove");
        row.innerHTML = row.innerHTML + "<td class='" + playerId + "'" + ">" + "<input type='button' class='btn btn-primary' value='-' onclick='removePlayerFromTable(" + playerId + ")'></input>" + "</td>";

        resolve();
      },
      error: function (data) {
        console.log(data);
        if (firstTry) {
          return addPlayerToTable(playerId, false);
        }
        reject()
      },
      timeout: 1000,
    });
  });
}

function removePlayerFromTable(playerId) {
  let column = document.getElementsByClassName(playerId.toString());
  while (column[0]) {
    column[0].parentNode.removeChild(column[0]);
  }
}

function showPlayer() {
  var chooser = document.getElementById("summonerid");
  var playerId = chooser.options[chooser.selectedIndex].value;
  return addPlayerToTable(playerId, true);
}

function toggleConnectionField() {
  var chooser = document.getElementById("visconnection");
  chooser.value = "all";
  chooser.disabled = document.getElementById("vismode").value == "extended";
}
