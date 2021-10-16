function loadStatistics(clusters = null, labels = []) {
  document.getElementById("statPlots").style.display = "none";
  document.getElementById("statLoader").style.display = "flex";
  document.getElementById("statDescOverall").style.display = "none";
  document.getElementById("statDescCluster").style.display = "none";
  closeAllCollapsibles();

  getStatArray().then((data) => {
    let traces = {};
    if (clusters) {
      document.getElementById("statDescCluster").style.display = "block";
      for (const clusterkey in clusters) {
        if (clusterkey != "labels" && clusterkey != "exportfn") {
          traces[clusterkey] = data["id"].map((e, i) => clusters[clusterkey]["ids"].includes(e) ? i : undefined).filter(x => x);
        }
      }
    } else {
      document.getElementById("statDescOverall").style.display = "block";
      traces[""] = Array.from(Array(data["id"].length).keys());
    }
    let promises = [];
    for (const key in data) {
      promises.push(new Promise (resolve => {
        let elementId = "stat" + key.replaceAll(" ", "");
        let targetElement = document.getElementById(elementId);
        if (!targetElement) {
          resolve();
          return;
        }
        let targetElementContainer = document.getElementById(elementId + "Container");
        if (labels.length && !labels.includes(key.replaceAll(" ", ""))) {
          targetElementContainer.style.display = "none";
        } else {
          targetElementContainer.style.display = "block";
        }
        let height = ((Object.keys(traces).length - 1) * 75 + 300).toString() + "px";
        targetElement.setAttribute("style","width:600px;height:" + height);
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
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)"
          };
  
        Plotly.newPlot(elementId, plotdata, layout);
  
        boxPlot.on('plotly_click', function(plot){
          openTabManually("linkPlayer", "playerDetails")
          addPlayerToTable(plot.points[0].text).then(() =>
            openTabManually("linkPlayer", "playerDetails")
          );
        });

        boxPlot.on('plotly_afterplot', function(){
          resolve();
        });
      }));
    }
    Promise.all(promises)
    .then(() => {
      document.getElementById("statLoader").style.display = "none";
      document.getElementById("statPlots").style.display = "block";
    })
  });
}

async function exportAllPlots(){
  let zip = new JSZip();
  let files = [];
  let filenames = [];
  let boxplots = document.getElementsByClassName("cauldron-boxplot");
  for (let boxplot of boxplots) {
    if (boxplot.parentElement.style.display == "block") {
      files.push(Plotly.toImage(boxplot, {format: 'png', width: 800, height: 600}));
      filenames.push(boxplot.id.substr(4) + ".png");
    }
  }
  let i = 0;
  Promise.all(files).then(dataUrls => {
    for (let dataUrl of dataUrls) {
      zip.file(filenames[i++], dataUrl.substr(22), {base64: true});
    }
    zip.generateAsync({type: "blob"}).then(function(content) {
      saveAs(content, "download.zip");
    });
  });
}