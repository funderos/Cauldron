let tooltips = {
  // Player Details
  id: "Unique number identifying the player assigned during survey",
  name: "In-game username of the player",
  platform: "Region where the player is registered",
  Gender: "Gender information gathered through survey",
  profile: "Motivational Profile calculated with survey and statistics",
  Age: "Age information gathered through survey",
  level: "In-game Summoner Level",
  matchcount: "Number of played matches included in the dataset",

  // Psychological Features - descriptions partly taken from https://positivepsychology.com/self-determination-theory/ and https://www.sfu.ca/~jcnesbit/EDUC220/week7/week7.html
  mean_IMO: "Internal motivation (Interest, Enjoyment, Inherent satisfaction)",
  mean_INT: "Internal motivation (Congruence, Awareness, Synthesis with self)",
  mean_IDE: "Somewhat internal motivation (Personal importance, conscious valuing)",
  mean_INJ: "Somewhat external motivation (Self-control, Ego-involvement, Internal rewards and punishments)",
  mean_EXT: "External motivation (Compliance, External rewards and punishments)",
  mean_AMO: "Impersonal motivation (Nonintentional, Nonvaluing, Incompetence, Lack of control)",
  mean_IMI_enj: "Interest and enjoyment felt",
  mean_IMI_tens: "Pressure and tension felt",
  mean_PENS_rel: "Need to have a close, affectionate relationship with others",
  mean_PENS_com: "Need to be effective in dealing with environment",
  mean_PENS_aut: "Need to control the course of their lives",
  mean_ACH_GOAL_perf_ap: "Focus on the demonstration of competence relative to others",
  mean_ACH_GOAL_perf_av: "Focus on avoiding failure in front of others",
  mean_ACH_GOAL_mast_ap: "Focus on the development of competence for its own sake",
  mean_ACH_GOAL_mast_av: "Focus on avoiding situations in which she/he is unable to learn",
  mean_PASSION_hp: "Harmonious Passion",
  mean_PASSION_op: "Obsessive Passion",
  PANAS_score_PA: "Positive Affect",
  PANAS_score_NA: "Negative Affect",
  mean_Vitality: "Vitality",

  // Match Features
  kda: "Ratio which is calculated by dividing the sum of kills and assists by deaths of a player during a match",
  kp: "Ratio which is calculated by dividing the sum of kills and assists of a player by total team kills for a match",
  teamDamage:
    "Ratio which describes how many % of the damage dealt by the team are achieved by a player for a match",
  teamGold:
    "Ratio which describes how many % of the gold earned by the team are achieved by a player for a match",
  ckpm: "Ratio which is calculated by dividing the sum of kills and deaths of a player by total minutes played within a match",
  kpw: "Ratio which is calculated by dividing the total sum of kills of a player by total matches the player participated in the winning team",
  dpl: "Ratio which is calculated by dividing the total sum of deaths of a player by total matches the player participated in the losing team",
  winrate:
    "Ratio which is calculated by dividing the total sum won matches of a player by total matches the player participated in",

  // Network Features
  ComponentRatio: `By removing ego from the network, the network may split up from one component
  (the initial network) to multiple components (smaller, non-connected networks). For considering the size
  of the initial network, components are not just summed up but put in a relation to the number of alters.`,
  Density: `The density is defined by the actual ties divided by the number of theoretically possible ties. It is defined by the number
  of reachable nodes (multiple tie hops are are also considered) divided by the amount of possible alter-alter ties subtracted from 1.`,
  FragmentationIndex: "Concepts of density and component ratio combined",
  Degree: "Network size which is defined by the number of alters",
  MeanTieStrength: "Mean over all tie strengths which is defined by the number of matches played together for each tie",
  Components: "Number of Components when removing the ego from the network",
};

function setTooltipsforPlayerFeatures() {
  for (let [key, value] of Object.entries(tooltips)) {
    document.getElementById("tooltip" + key).setAttribute("data-tip", value);
  }
}

function addPlayerToTable(playerId, firstTry = true) {
  let checkExisting = document.getElementsByClassName(playerId.toString());
  if (checkExisting.length) return Promise.resolve();
  return new Promise((resolve, reject) => {
    $.ajax({
      dataType: "json",
      url: "network/" + playerId + "?mode=details",
      success: function (data) {
        for (key in data) {
          let value = data[key];
          if (!isNaN(value)) {
            let aFloat = value.toString().split(".");
            if (aFloat.length > 1)
              value = aFloat[0] + "." + aFloat[1].substr(0, 4);
          }
          if (key == "Gender") {
            switch (value) {
              case "A1":
                value = "female";
                break;
              case "A2":
                value = "male";
                break;
              case "A3":
                value = "non-binary";
                break;
              case "A4":
                value = "undisclosed";
                break;
              default:
                value = "invalid value";
            }
          }
          let row = document.getElementById("detail" + key);
          row.innerHTML =
            row.innerHTML +
            "<td class='" +
            playerId +
            "'" +
            ">" +
            value +
            "</td>";
        }
        let row = document.getElementById("detailshownetwork");
        row.innerHTML =
          row.innerHTML +
          "<td class='" +
          playerId +
          "'" +
          ">" +
          "<input type='button' class='btn btn-primary' value='Show!' onclick='drawNetwork(" +
          playerId +
          ")'></input>" +
          "</td>";
        row = document.getElementById("detailremove");
        row.innerHTML =
          row.innerHTML +
          "<td class='" +
          playerId +
          "'" +
          ">" +
          "<input type='button' class='btn btn-primary' value='-' onclick='removePlayerFromTable(" +
          playerId +
          ")'></input>" +
          "</td>";

        resolve();
      },
      error: function (data) {
        console.log(data);
        if (firstTry) {
          return addPlayerToTable(playerId, false);
        }
        reject();
      },
      timeout: 5000,
    });
  });
}

function removePlayerFromTable(playerId) {
  let column = document.getElementsByClassName(playerId.toString());
  while (column[0]) {
    column[0].parentNode.removeChild(column[0]);
  }
}

function showPlayer() {
  var chooser = document.getElementById("summonerid");
  var playerId = chooser.options[chooser.selectedIndex].value;
  return addPlayerToTable(playerId, true);
}

function toggleConnectionField() {
  var chooser = document.getElementById("visconnection");
  chooser.value = "all";
  chooser.disabled = document.getElementById("vismode").value == "extended";
}
