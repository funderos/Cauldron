function loadStatistics() {
  getStatArray().then((data) => {
    console.log(data);
    for (const key in data) {
      var elementId = "stat" + key.replaceAll(" ", "");
      var targetElement = document.getElementById(elementId);

      var boxPlot = targetElement,
        colors = Array(data.length).fill("#00000"),
        plotdata = [
          {
            x: data[key],
            type: "box",
            boxpoints: "all",
            jitter: 0.3,
            pointpos: 0,
            mode: "markers",
            marker:{color:colors},
            name: targetElement
              .getAttribute("name")
              .replaceAll("_", " "),
          },
        ],
        layout = {
          showlegend: false,
          hovermode: "closest",
        };

      Plotly.newPlot(elementId, plotdata, layout);

      boxPlot.on("plotly_hover", function (plotdata) {
        var pn = "",
          tn = "",
          colors = [];
        for (var i = 0; i < plotdata.points.length; i++) {
          pn = plotdata.points[i].pointNumber;
          tn = plotdata.points[i].curveNumber;
          colors = plotdata.points[i].data.marker.color;
        }
        colors[pn] = "#C54C82";

        var update = { marker: { color: colors} };
        Plotly.restyle(elementId, update, [tn]);
      });

      boxPlot.on("plotly_unhover", function (plotdata) {
        var pn = "",
          tn = "",
          colors = [];
        for (var i = 0; i < plotdata.points.length; i++) {
          pn = plotdata.points[i].pointNumber;
          tn = plotdata.points[i].curveNumber;
          colors = plotdata.points[i].data.marker.color;
        }
        colors[pn] = "#00000";

        var update = { marker: { color: colors} };
        Plotly.restyle(elementId, update, [tn]);
      });

      boxPlot.on('plotly_click', function(plotdata){
        var pn="";
        for(var i=0; i < plotdata.points.length; i++){
          pn = plotdata.points[i].pointNumber;
        };
        console.log(data['id'][pn]);
        document.getElementById('summonerid').value = data['id'][pn];
        showPlayer(true);
        openTabManually("linkPlayer", "playerDetails")
      });
    }
  });
}
