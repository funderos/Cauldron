function loadStatistics(clusters = null) {
  getStatArray().then((data) => {
    let traces = {};
    if (clusters) {
      for (const clusterkey in clusters) {
        if (clusterkey != "labels" && clusterkey != "exportfn") {
          traces[clusterkey] = data["id"].map((e, i) => clusters[clusterkey]["ids"].includes(e) ? i : undefined).filter(x => x);
        }
      }
    } else {
      traces[""] = Array.from(Array(data["id"].length).keys());
    }
    for (const key in data) {
      var elementId = "stat" + key.replaceAll(" ", "");
      var targetElement = document.getElementById(elementId);
      if (!targetElement) continue;

      let height = (Object.keys(traces).length * 250).toString() + "px";
      targetElement.setAttribute("style","width:1000px;height:" + height);
      targetElement.style.height = height;

      let plotdata = [];

      for (const tracekey in traces) {
        plotdata.push(
          {
            x: data[key].filter((e, i) => traces[tracekey].some(j => i === j)),
            type: "box",
            boxpoints: "all",
            jitter: 0.3,
            pointpos: 0,
            marker:{},
            name: tracekey,
            text: data["id"].filter((e, i) => traces[tracekey].some(j => i === j)),
            hovertemplate: '<b>%{text}</b>: %{x}'
          }
        )
      }
      
      var boxPlot = targetElement,
        //colors = Array(data.length).fill("#00000"),
        layout = {
          showlegend: false,
          hovermode: "closest",
        };

      Plotly.newPlot(elementId, plotdata, layout);

      boxPlot.on('plotly_click', function(plot){
        document.getElementById('summonerid').value = plot.points[0].text;
        showPlayer(true);
        openTabManually("linkPlayer", "playerDetails")
      });
    }
  });
}
