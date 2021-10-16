let data = null;
let labels = [];
let clusterParams = new Map();
//let loader = document.getElementById('clustering-loader');
let resultPlot = document.getElementById("clustering-results");

function setFeatureFields() {
  let chooser = document.getElementById("clustertype");
  let type = chooser.options[chooser.selectedIndex].value;
  document.getElementById("dimreduce-label").style.display = type == "elbow" ? "none" : "block";
  document.getElementById("kmk-label").style.display = type == "kmeans" ? "block" : "none";
  document.getElementById("dbe-label").style.display = type == "dbscan" ? "block" : "none";
  document.getElementById("spn-label").style.display = type == "spectral" ? "block" : "none";
  document.getElementById("ops-label").style.display = type == "optics" ? "block" : "none";
}

function selectAll(selected) {
  let form = document.getElementById("clustering-features");
  for (let i = 0; i < form.length; i++) {
    form.elements[i].checked = selected;
  }
}

function drawClusterPlot() {
  document.getElementById("post-cluster-buttons").style.display = "none";
  resultPlot.innerHTML = "<div class='loader'></div>"
  let chooser = document.getElementById("clustertype");
  let type = chooser.options[chooser.selectedIndex].value;

  labels = [];
  clusterParams.clear();
  let form = document.getElementById("clustering-features");
  for (let i = 0; i < form.length; i++) {
    let val = form.elements[i];
    if (val.type == "checkbox" && val.checked) {
      labels.push(val.id.substr(5));
    }
    if (val.type == "number" && val.value) {
      clusterParams.set(val.id, val.value);
    }
  }
  
  if (type == "elbow") {
    elbowPlot(true);
  } else {
    scatterPlot(type, true);
  }
}

function scatterPlot(clusterType, firstTry) {
  let form = document.getElementById("clustering-features");
  let chooser = document.getElementById("preprocessing");
  let preprocess =
    "&preprocess=" + chooser.options[chooser.selectedIndex].value;
  chooser = document.getElementById("dimreduce");
  let dimreduce = "&dimreduce=" + chooser.options[chooser.selectedIndex].value;
  let clusterParamString = "";
  clusterParams.forEach((value, key) => clusterParamString = clusterParamString + "&" + key + "=" + value);
 
  let queryString =
    "?labels=" +
    labels.join() +
    preprocess +
    dimreduce +
    "&clustertype=" +
    clusterType +
    clusterParamString;
  $.ajax({
    url: "cluster" + queryString,
    success: (results) => {
      data = results;
      let traces = [];
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

      document.getElementById("post-cluster-buttons").style.display = "flex";

      resultPlot.on("plotly_click", function (plotdata) {
        var pn = "";
        var label = "";
        for (let point of plotdata.points) {
          pn = point.pointNumber;
          label = point.data.name;
        }
        if (label && pn) {
          addPlayerToTable(data[label]["ids"][pn]).then(() =>
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
  let chooser = document.getElementById("preprocessing");
  let preprocess = "preprocess=" + chooser.options[chooser.selectedIndex].value;
  let queryString = "?labels=" + labels.join() + "&" + preprocess;
  $.ajax({
    url: "elbow" + queryString,
    success: function (data) {
      resultPlot.innerHTML = data.slice(data.indexOf("<svg"));
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
  loadStatistics(data, labels);
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
