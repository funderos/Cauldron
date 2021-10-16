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

  // Psychological Features
  mean_IMO: "Intrinsic Regulation (IMO)",
  mean_INT: "Integrated Regulation (INT)",
  mean_IDE: "Identified Regulation (IDE)",
  mean_INJ: "Introjected Regulation (INJ)",
  mean_EXT: "External Regulation (EXT)",
  mean_AMO: "Non-regulation (AMO)",
  mean_IMI_enj: "Interest-Enjoyment (IMI)",
  mean_IMI_tens: "Pressure-Tension (IMI)",
  mean_PENS_rel: "Player Experience Need Satisfaction (PENS): Relatedness",
  mean_PENS_com: "Player Experience Need Satisfaction (PENS): Compentence",
  mean_PENS_aut: "Player Experience Need Satisfaction (PENS): Autonomy",
  mean_ACH_GOAL_perf_ap: "Achievement Goal: Performance Approach",
  mean_ACH_GOAL_perf_av: "Achievement Goal: Performance Avoidance",
  mean_ACH_GOAL_mast_ap: "Achievement Goal: Mastery Approach",
  mean_ACH_GOAL_mast_av: "Achievement Goal: Mastery Avoidance",
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
  ComponentRatio: "Component Ratio",
  Density: "Density",
  FragmentationIndex: "Fragmentation Index",
  Degree: "Degree",
  MeanTieStrength: "Mean Tie Strength",
  Components: "Number of Components",
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
      timeout: 1000,
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
