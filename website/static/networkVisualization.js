var nodes = null;
var edges = null;
var network = null;

function drawNetwork(playerid, firstTry = true) {
  openModal();
  nodes = [];
  edges = [];
  var chooser = document.getElementById('vismode');
  var vismode = chooser.options[chooser.selectedIndex].value;
  chooser = document.getElementById('visconnection');
  var viscon = chooser.options[chooser.selectedIndex].value;
  var componentParam = document.getElementById('viscomponents').checked ? "&viscom=true" : "&viscom=false";
  $.ajax({
    dataType: "json",
    url: "network/" + playerid + "?mode=" + vismode + "&viscon=" + viscon + componentParam,
    success: function(data){
      console.log(data)
      nodes = data["nodes"];
      nodes[nodes.length - 1]["cid"] = 1;
      nodes[nodes.length - 1]["label"] = nodes[nodes.length - 1]["label"].toString();
      edges = data["edges"];
      console.log(nodes.length);
      console.log(edges.length);
      if (nodes.length > 0 && edges.length > 0) {
        draw();
      }
    },
    error: function(data){
      console.log(data);
      if (firstTry) {
        drawNetwork(content, false)
      }
    },
    timeout: 1000
  });
}

function draw() {
  // Instantiate our network object.
  var container = document.getElementById('network-content');
  var loader = document.getElementById('network-loader');

  loader.style.display = "flex";
  container.style.display = "none";
  
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    layout: {
        improvedLayout: false
    },
    nodes: {
        shape: 'dot',
    }
  };
  network = new vis.Network(container, data, options);
  /*
  var clusterOptionsByData = {
    processProperties: function (clusterOptions, childNodes) {
      clusterOptions.label = "[" + childNodes.length + "]";
      return clusterOptions;
    },
    clusterNodeProperties: {
      borderWidth: 3,
      shape: "box",
      font: { size: 30 },
    },
    joinCondition: function(childNodeOptions) {
      return childNodeOptions.cid != 1;
    }
  };
  network.clusterByHubsize(4, clusterOptionsByData);
  */
  
  loader.style.display = "none";
  container.style.display = "flex";

  network.once("afterDrawing", () => {
    loader.style.display = "none";
    container.style.display = "flex";
  });


}