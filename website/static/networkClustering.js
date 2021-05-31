function clusterData(firstTry) {
    let form = document.getElementById("clustering-features");
    let labels = "labels="
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
      url: 'cluster' + queryString,
      success: function(data){
        let htmlString = "<table style='width:100%'>"
        data.forEach(row => {
          htmlString += "<tr>"
          row.forEach(val => {
            htmlString = htmlString + "<th>" + val + "</th>";
          })
          htmlString += "</tr>"
        })
        htmlString += "</table>";
        let resultDiv = document.getElementById('clustering-results')
        resultDiv.innerHTML = htmlString;
      },
      error: function(data){
        if (firstTry) {
          clusterData(false)
        }
      },
      timeout: 1000
    });
  }

  function scatterPlot(firstTry) {
    let form = document.getElementById("clustering-features");
    let labels = "labels="
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
      url: 'cluster' + queryString,
      success: function(data){
        let htmlString = "<img src='data:image/svg+xml;utf8," + data.slice(data.indexOf("<svg")) + "'>"
        let resultDiv = document.getElementById('clustering-results')
        console.log(htmlString);
        resultDiv.innerHTML = data.slice(data.indexOf("<svg"));
      },
      error: function(data){
        if (firstTry) {
          scatterPlot(false)
        }
      },
      timeout: 1000
    });
  }

  function elbowPlot(firstTry) {
    let form = document.getElementById("clustering-features");
    let labels = "labels="
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
      url: 'elbow' + queryString,
      success: function(data){
        let htmlString = "<img src='data:image/svg+xml;utf8," + data.slice(data.indexOf("<svg")) + "'>"
        let resultDiv = document.getElementById('clustering-results')
        console.log(htmlString);
        resultDiv.innerHTML = data.slice(data.indexOf("<svg"));
      },
      error: function(data){
        if (firstTry) {
          elbowPlot(false)
        }
      },
      timeout: 1000
    });
  }