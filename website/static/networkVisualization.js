var nodes = null;
var edges = null;
var network = null;

function drawNetwork(content, firstTry) {
  openModal();
  nodes = [];
  edges = [];
  var chooser = document.getElementById('summonerid');
  var key = chooser.options[chooser.selectedIndex].value;
  $.ajax({
    dataType: "json",
    url: "network/" + key + "?content=" + content,
    success: function(data){
      console.log(data)
      nodes = data["nodes"];
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

function drawDemo(levels, firstTry) {
  var chooser = document.getElementById('summonerid');
  var key = chooser.options[chooser.selectedIndex].value;
  var infoDiv = document.getElementById('network-output')
  $.ajax({
    dataType: "json",
    url: 'network/' + key,
    success: function(data){
      console.log(data)
      let info = "";
      nodes = [];
      edges = [];
      for (key in data) {
        if (key.includes("nodes")) {
          if (key == "nodesEgo") nodes.push(data[key]);
          else if (levels > 1) nodes.push(...data[key]);
        } else if (key.includes("edges")) {
          if (levels > 1) edges.push(...data[key]);
        } else {
          info = info + key + ": " + data[key] + ", ";
        }
      }
      if (levels == 1) {
        nodes.push(...data["nodesAlters"]);
        edges.push(...data["edgesEgo"]);
        edges.push(...data["edgesAlters"]);
      }
      infoDiv.innerHTML = info.substring(0, info.length - 2)
      console.log(nodes.length);
      console.log(edges.length);
      if (nodes.length > 0 && edges.length > 0) {
        draw();
      }
    },
    error: function(data){
      console.log(data);
      if (firstTry) {
        drawDemo(false)
      }
    },
    timeout: 1000
  });
}

function draw() {
  // Instantiate our network object.
  var container = document.getElementById('network-content');
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
}