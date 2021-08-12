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

  function scatterPlot(clusterType, firstTry) {
    let form = document.getElementById("clustering-features");
    let labels = "labels="
    let clusterParams = "";
    let chooser = document.getElementById("preprocessing");
    let preprocess = "preprocess=" + chooser.options[chooser.selectedIndex].value;
    for (let i = 0; i < form.length; i++) {
        let val = form.elements[i];
        if (val.type == "checkbox" && val.checked) {
          labels = labels + val.id + ",";
        }
        if (val.type == "number" && val.value) {
          clusterParams = clusterParams + "&" + val.id + "=" + val.value;
        }
    }
    let queryString = "?" + labels.slice(0, -1) + "&" + preprocess + "&dimreduce=pca&clustertype=" + clusterType + clusterParams;
    $.ajax({
      url: 'cluster' + queryString,
      success: function(data){
        //let htmlString = "<img src='data:image/svg+xml;utf8," + data.slice(data.indexOf("<svg")) + "'>"
        let traces = []
        let resultPlot = document.getElementById("clustering-results");
        resultPlot.innerHTML = "";
        //Plotly.purge("clustering-results");

        for (const label in data) {
          traces.push({
            x: data[label]["x"], y: data[label]["y"], z: data[label]["z"],
            mode: "markers",
            marker: {
              size: 12,
              symbol: 'circle',
              line: {
              color: 'rgb(0, 0, 0)',
              width: 1}},
            name: label,
            type: "scatter3d"
          });
        }

        var layout = {margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0
          }};

        Plotly.newPlot("clustering-results", traces, layout);
        //let resultDiv = document.getElementById('clustering-results')
        //resultDiv.innerHTML = data.slice(data.indexOf("<svg"));

        resultPlot.on('plotly_click', function(plotdata){
          var pn="";
          var label ="";
          for(var i=0; i < plotdata.points.length; i++){
            pn = plotdata.points[i].pointNumber;
            label = plotdata.points[i].data.name;
          };
          if (label && pn)
          document.getElementById('summonerid').value = data[label]['ids'][pn];
          showPlayer(true);
          openTabManually("linkPlayer", "playerDetails")
        });
      },
      error: function(data){
        if (firstTry) {
          scatterPlot(clusterType, false)
        }
      },
      timeout: 5000
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