function loadStatistics() {
  getStatArray().then((data) => {
    console.log(data);
    for (const key in data) {
      var trace = {
        x: data[key],
        type: "box",
        boxpoints: "all",
        jitter: 0.3,
        pointpos: 0,
        name: key,
      };
      Plotly.newPlot("stat" + key.replaceAll(" ", ""), [trace]);
    }
  });
}
