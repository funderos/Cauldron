let data = null;

function clusterData(firstTry) {
  let form = document.getElementById("clustering-features");
  let labels = "labels=";
  let k = "";
  let chooser = document.getElementById("preprocessing");
  let preprocess = "preprocess=" + chooser.options[chooser.selectedIndex].value;
  for (let i = 0; i < form.length; i++) {
    let val = form.elements[i];
    if (val.type == "checkbox" && val.checked) {
      labels = labels + val.id + ",";
    }
    if (val.type == "number") {
      k = "k=" + val.value;
    }
  }
  let queryString = "?" + labels.slice(0, -1) + "&" + preprocess + "&" + k;
  $.ajax({
    dataType: "json",
    url: "cluster" + queryString,
    success: function (data) {
      let htmlString = "<table style='width:100%'>";
      data.forEach((row) => {
        htmlString += "<tr>";
        row.forEach((val) => {
          htmlString = htmlString + "<th>" + val + "</th>";
        });
        htmlString += "</tr>";
      });
      htmlString += "</table>";
      let resultDiv = document.getElementById("clustering-results");
      resultDiv.innerHTML = htmlString;
    },
    error: function (data) {
      if (firstTry) {
        clusterData(false);
      }
    },
    timeout: 1000,
  });
}

function scatterPlot(clusterType, firstTry) {
  let form = document.getElementById("clustering-features");
  let labels = "labels=";
  let clusterParams = "";
  let chooser = document.getElementById("preprocessing");
  let preprocess =
    "&preprocess=" + chooser.options[chooser.selectedIndex].value;
  chooser = document.getElementById("dimreduce");
  let dimreduce = "&dimreduce=" + chooser.options[chooser.selectedIndex].value;
  for (let i = 0; i < form.length; i++) {
    let val = form.elements[i];
    if (val.type == "checkbox" && val.checked) {
      labels = labels + val.id + ",";
    }
    if (val.type == "number" && val.value) {
      clusterParams = clusterParams + "&" + val.id + "=" + val.value;
    }
  }
  let queryString =
    "?" +
    labels.slice(0, -1) +
    preprocess +
    dimreduce +
    "&clustertype=" +
    clusterType +
    clusterParams;
  $.ajax({
    url: "cluster" + queryString,
    success: (results) => {
      //let htmlString = "<img src='data:image/svg+xml;utf8," + data.slice(data.indexOf("<svg")) + "'>"
      data = results;
      let traces = [];
      let resultPlot = document.getElementById("clustering-results");
      resultPlot.innerHTML = "";
      //Plotly.purge("clustering-results");

      for (const label in data) {
        traces.push({
          x: data[label]["x"],
          y: data[label]["y"],
          z: data[label]["z"],
          mode: "markers",
          marker: {
            size: 12,
            symbol: "circle",
            line: {
              color: "rgb(0, 0, 0)",
              width: 1,
            },
          },
          name: label,
          type: "scatter3d",
        });
      }

      var layout = {
        margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0,
        },
      };

      Plotly.newPlot("clustering-results", traces, layout);
      //let resultDiv = document.getElementById('clustering-results')
      //resultDiv.innerHTML = data.slice(data.indexOf("<svg"));

      resultPlot.on("plotly_click", function (plotdata) {
        var pn = "";
        var label = "";
        for (let point of plotdata.points) {
          pn = point.pointNumber;
          label = point.data.name;
        }
        if (label && pn) {
          document.getElementById("summonerid").value = data[label]["ids"][pn];
          showPlayer(true).then(() =>
            openTabManually("linkPlayer", "playerDetails")
          );
        }
      });
    },
    error: function (error) {
      if (firstTry) {
        scatterPlot(clusterType, false);
      }
    },
    timeout: 50000,
  });
}

function elbowPlot(firstTry) {
  let form = document.getElementById("clustering-features");
  let labels = "labels=";
  let chooser = document.getElementById("preprocessing");
  let preprocess = "preprocess=" + chooser.options[chooser.selectedIndex].value;
  for (let i = 0; i < form.length; i++) {
    let val = form.elements[i];
    if (val.type == "checkbox" && val.checked) {
      labels = labels + val.id + ",";
    }
  }
  let queryString = "?" + labels.slice(0, -1) + "&" + preprocess;
  $.ajax({
    url: "elbow" + queryString,
    success: function (data) {
      let htmlString =
        "<img src='data:image/svg+xml;utf8," +
        data.slice(data.indexOf("<svg")) +
        "'>";
      let resultDiv = document.getElementById("clustering-results");
      console.log(htmlString);
      resultDiv.innerHTML = data.slice(data.indexOf("<svg"));
    },
    error: function (data) {
      if (firstTry) {
        elbowPlot(false);
      }
    },
    timeout: 1000,
  });
}

function updateStats() {
  loadStatistics(data);
  openTabManually("linkStats", "statistics");
}

function exportCsv() {
  $.ajax({
    type: "POST",
    url: "stats",
    data: JSON.stringify(data["labels"]),
    contentType:"application/json; charset=utf-8",
    //dataType:"json",
    xhrFields: {
      responseType: "blob", // to avoid binary data being mangled on charset conversion
    },
    success: function (blob) {
      // check for a filename
      var filename = data["exportfn"];
      if (typeof window.navigator.msSaveBlob !== "undefined") {
        // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
        window.navigator.msSaveBlob(blob, filename);
      } else {
        var URL = window.URL || window.webkitURL;
        var downloadUrl = URL.createObjectURL(blob);

        if (filename) {
          // use HTML5 a[download] attribute to specify filename
          var a = document.createElement("a");
          // safari doesn't support this yet
          if (typeof a.download === "undefined") {
            window.location.href = downloadUrl;
          } else {
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
          }
        } else {
          window.location.href = downloadUrl;
        }

        setTimeout(function () {
          URL.revokeObjectURL(downloadUrl);
        }, 500); // cleanup
      }
    },
  });
}
