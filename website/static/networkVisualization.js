var nodes = null;
var activeParents = null;
var edges = null;
var network = null;

function drawNetwork(playerid, firstTry = true) {
  openModal();
  document.getElementById("network-loader").style.display = "flex";
  nodes = [];
  edges = [];
  activeParents = null;
  var chooser = document.getElementById("vismode");
  var vismode = chooser.options[chooser.selectedIndex].value;
  chooser = document.getElementById("visconnection");
  var viscon = chooser.options[chooser.selectedIndex].value;
  var componentParam = document.getElementById("viscomponents").checked
    ? "&viscom=true"
    : "&viscom=false";
  $.ajax({
    dataType: "json",
    url:
      "network/" +
      playerid +
      "?mode=" +
      vismode +
      "&viscon=" +
      viscon +
      componentParam,
    success: function (data) {
      console.log(data);
      nodes = data["nodes"];
      edges = data["edges"];
      if (vismode == "extended") {
        activeParents = [];
        nodes
          .filter((node) => !node.parents)
          .forEach(
            (innerNode) =>
              (innerNode["label"] =
                innerNode["label"] +
                ` [${
                  nodes.filter(
                    (child) =>
                      child["parents"] &&
                      child["parents"].includes(innerNode["id"])
                  ).length
                }]`)
          );
      }
      console.log(nodes.length);
      console.log(edges.length);
      if (nodes.length > 0 && edges.length > 0) {
        draw();
      }
    },
    error: function (data) {
      console.log(data);
      if (firstTry) {
        drawNetwork(playerid, false);
      }
    },
    timeout: 20000,
  });
}

function toggleParent(id) {
  let index = activeParents.indexOf(id);
  if (index === -1) {
    activeParents.push(id);
  } else {
    activeParents.splice(index, 1);
  }
}

function draw() {
  let that = this;
  // Instantiate our network object.
  var container = document.getElementById("network-content");
  var loader = document.getElementById("network-loader");

  loader.style.display = "flex";
  container.style.display = "flex";

  var data = {
    nodes: nodes.filter(
      (node) =>
        !node.parents ||
        node.parents.some((parent) => activeParents.includes(parent))
    ),
    edges: edges,
  };

  if (data.nodes.length > 200) {
    if (!confirm("The graph contains more than 200 nodes and may impact browser performance. Do you want to continue?")) {
      closeModal();
      return;
    }
  }

  var options = {
    layout: {
      improvedLayout: false,
    },
    nodes: {
      shape: "dot",
    },
  };

  network = new vis.Network(container, data, options);

  network.on("stabilizationIterationsDone", function () {
    loader.style.display = "none";
  });

  if (activeParents) {
    network.on("doubleClick", function (params) {
      that.toggleParent(params.nodes[0]);
      data.nodes = nodes.filter(
        (node) =>
          !node.parents ||
          node.parents.some((parent) => activeParents.includes(parent))
      );
      if (data.nodes.length > 200) {
        if (!confirm("The resulting graph contains more than 200 nodes and may impact browser performance. Do you want to continue?")) {
          that.toggleParent(params.nodes[0]);
          return;
        }
      }
      let parentNode = data.nodes.find((pn) => pn["id"] == params.nodes[0]);
      parentNode["x"] = params.event.center.x;
      parentNode["y"] = params.event.center.y;
      network.setData(data);
      network.redraw();
      loader.style.display = "flex";
    });
  }
}
